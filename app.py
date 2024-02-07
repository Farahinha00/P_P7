from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import tensorflow as tf
import joblib
from script_inf import make_inference  # Assurez-vous que script_inf.py est dans le même dossier
#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from urllib.request import urlretrieve
app = FastAPI()

# Define the URL and the filename
url1 = "https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121951-1176e6b9/tokenizer.pkl"
filename1 = "tokenizer"
# Define the URL and the filename
url2 = "https://ocp73883544777.blob.core.windows.net/azureml/LocalUpload/240118T121943-79cc729e/mon_best_model.h5"
filename2 = "mon_best_model"
# Download the file
urlretrieve(url2, filename2)
urlretrieve(url1, filename1)

# Déclaration des variables globales
model = None
tokenise = None
#ws = Workspace.from_config()


def init():
    global model
    global tokenise

    try:
#        # Chargez le tokenizer
        tokenise = joblib.load(filename1)
    except Exception as e:
        print(f"Erreur lors du chargement du tokenizer : {e}")
        
    try:
        # Chargez le modèle Keras
        model = tf.keras.models.load_model(filename2)
    except Exception as e:
        print(f"Erreur lors du chargement du modèle Keras : {e}")


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
    prediction = make_inference(raw_data, tokenise, model)[0][0]  # assuming make_inference returns a prediction in this format
    if prediction < 0.4:
        sentiment = "good"
    elif prediction > 0.6:
        sentiment = "bad"
    else:
        sentiment = "neutral"

    response = f'The tweet "{raw_data}" is {sentiment}.'

    return response

