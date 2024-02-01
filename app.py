from fastapi import FastAPI
import tensorflow as tf
import joblib
from azureml.core.model import Model
from azureml.core import Workspace
from script_inf import make_inference  # Assurez-vous que script_inf.py est dans le même dossier
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
app = FastAPI()

# Déclaration des variables globales
model = None
tokenise = None
#ws = Workspace.from_config()

# Initialize a BlobServiceClient using a connection string
connect_str = "+37I7IMHXMh1MDLcA/Q32/mV8LL4pk5Ls0unKB0bS2cohC7nze3Z7y5CPWYyZvAaRvUPAKupPZDp+ASt35N8vQ=="
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Access a specific container
container_name = "ocp73883544777"
container_client = blob_service_client.get_container_client(container_name)

# Access a blob within the container
blob_name = "mon_best_model.h5"
blob_client = container_client.get_blob_client(blob_name)

# Download the blob's content
with open("best_model", "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())

#def init():
#    global model
#    global tokenise

    # Obtenez le chemin des modèles stockés dans Azure ML
#    best_model_path = Model.get_model_path(model_name='mon_best_model', version=1, _workspace=ws)
#    tokenizer_path = Model.get_model_path(model_name='tokenizer', version=1, _workspace=ws)

#    try:
#        # Chargez le tokenizer
#        tokenise = joblib.load(tokenizer_path)
#    except Exception as e:
#        print(f"Erreur lors du chargement du tokenizer : {e}")
#        
#    try:
#        # Chargez le modèle Keras
#        model = tf.keras.models.load_model(best_model_path)
#    except Exception as e:
#        print(f"Erreur lors du chargement du modèle Keras : {e}")


# Événement de démarrage pour exécuter la fonction init
# @app.on_event("startup")
# async def startup_event():
#     init()
@app.get("/")
async def root():
    return {"message": "Hello World"}
#@app.post("/predict/{raw_data}")
# async def predict(raw_data: str):
    # Effectuer l'inférence
 #    prediction = make_inference(raw_data,tokenise,model)

    # Retourner la prédiction
   #return {"Prédiction"}
