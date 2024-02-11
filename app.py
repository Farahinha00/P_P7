import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import tensorflow as tf
import joblib
from script_inf import make_inference
from urllib.request import urlretrieve

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

def init():
    global model, tokenise

    #download_file("https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121951-1176e6b9/tokenizer.pkl", filename1)
    #download_file("https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121943-79cc729e/mon_best_model.h5", filename2)

    tokenise = joblib.load(filename1)
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
    
#@app.post("/predict")
#async def predict(raw_data: str = Form(...)):
#    prediction = make_inference(raw_data, tokenise, model)
#    return {"Prédiction": prediction}

    
@app.post("/predict", response_class=HTMLResponse)
async def predict(raw_data: str = Form(...)):
    prediction = make_inference(raw_data, tokenise, model)
    if prediction < 0.4:
        sentiment = "good"
    elif prediction > 0.6:
        sentiment = "bad"
    else:
        sentiment = "neutral"

    response = f'The tweet "{raw_data}" is {sentiment}.'

    return response

