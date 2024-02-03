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


# Déclaration des variables globales
model = None
tokenise = None
#ws = Workspace.from_config()


def init():
    global model
    global tokenise

    # Obtenez le chemin des modèles stockés dans Azure ML
 #   best_model_path = Model.get_model_path(model_name='mon_best_model', version=1, _workspace=ws)
#    tokenizer_path = Model.get_model_path(model_name='tokenizer', version=1, _workspace=ws)

    try:
#        # Chargez le tokenizer
        tokenise = joblib.load(tokenizer)
    except Exception as e:
        print(f"Erreur lors du chargement du tokenizer : {e}")
        
    try:
        # Chargez le modèle Keras
        model = tf.keras.models.load_model(mon_best_model)
    except Exception as e:
        print(f"Erreur lors du chargement du modèle Keras : {e}")


# Événement de démarrage pour exécuter la fonction init

#@app.get("/")
#async def root():
#    return {"message": "Hello World"}
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
@app.on_event("startup")
async def startup_event():
    init()
@app.post("/predict")
async def predict(raw_data: str = Form(...)):
    prediction = make_inference(raw_data, tokenise, model)
    return {"Prédiction": prediction}
#@app.post("/predict/{raw_data}")
#async def predict(raw_data: str):
#    # Effectuer l'inférence
 #   prediction = make_inference(raw_data, tokenise, model)

    # Retourner la prédiction
#    return {"Prédiction": prediction}

