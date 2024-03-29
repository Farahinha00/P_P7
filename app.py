import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import tensorflow as tf
from time import sleep

from script_inf import make_inference
from urllib.request import urlretrieve
import pickle
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from logging import getLogger, INFO
from dotenv import load_dotenv
from opentelemetry.trace import get_tracer_provider
import logging

load_dotenv()

configure_azure_monitor(
    connection_string=os.getenv("InstrumentationKey=bfb9f0a9-76e7-4661-a709-022dacea56fc;IngestionEndpoint=https://francecentral-1.in.applicationinsights.azure.com/;LiveEndpoint=https://francecentral.livediagnostics.monitor.azure.com/")
)

tracer = trace.get_tracer(__name__,
                          tracer_provider=get_tracer_provider())
logger = getLogger(__name__)

def load_with_pickle(filename):
    with open(filename, 'rb') as file:  # 'rb' pour lire en mode binaire
        return pickle.load(file)

app = FastAPI()

model = None
tokenise = None
# Define the URL and the filename
url1 = "https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121951-1176e6b9/tokenizer.pkl"
filename1 = "tokenizer"
# Define the URL and the filename
url2 = "https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121943-79cc729e/mon_best_model.h5"
filename2 = "mon_best_model"
# Download the file
urlretrieve(url2, filename2)
urlretrieve(url1, filename1)


def download_file(url, filename):
    if not os.path.exists(filename):
        urlretrieve(url, filename)
        while not os.path.exists(filename) or os.path.getsize(filename) == 0:
            sleep(1)  # Attendre 1 seconde avant de vérifier à nouveau

def init():
    global model, tokenise

    download_file("https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121951-1176e6b9/tokenizer.pkl", filename1)
    download_file("https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121943-79cc729e/mon_best_model.h5", filename2)

    tokenise = load_with_pickle(filename1)
    model = tf.keras.models.load_model(filename2)

# Événement de démarrage pour exécuter la fonction init
@app.on_event("startup")
async def startup_event():
    init()

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <body>
            <form action="/predict" method="post">
                <input type="text" name="raw_data" />
                <input type="submit" />
            </form>
        </body>
    </html>
    """
    

    
@app.post("/predict", response_class=HTMLResponse)
async def predict(raw_data: str = Form(...)):
    with tracer.start_as_current_span("predict"):
        prediction = make_inference(raw_data, tokenise, model)
        if prediction < 0.5:
            sentiment = "good"
        else:
            sentiment = "bad"
        logging.info(f"Received '{raw_data}' and predicted as '{sentiment}'")
    response = f"""
    <html>
        <body>
            The tweet "{raw_data}" is {sentiment}.<br>
            <form action="/report" method="post">
                <input type="hidden" name="raw_data" value="{raw_data}" />
                <input type="submit" value="Not Confirm" />
            </form>
        </body>
    </html>
    """
    return response


@app.post("/report")
async def report(raw_data: str = Form(...)):
    # Logique d'envoi d'alerte à Azure Application Insights
    logging.warning(f"Non-confirm prediction reported for: '{raw_data}'")
    # Vous pouvez ici ajouter des détails supplémentaires pour Azure Insights si nécessaire
    return {"message": "Report received, thank you for your feedback!"}


