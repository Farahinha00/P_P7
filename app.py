from fastapi import FastAPI
import tensorflow as tf
import joblib
from azureml.core.model import Model
from azureml.core import Workspace
from script_inf import make_inference  # Assurez-vous que script_inf.py est dans le même dossier
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
app = FastAPI()

storage_account_key = "+37I7IMHXMh1MDLcA/Q32/mV8LL4pk5Ls0unKB0bS2cohC7nze3Z7y5CPWYyZvAaRvUPAKupPZDp+ASt35N8vQ=="
storage_account_name = "ocp73883544777"
connection_string = "DefaultEndpointsProtocol=https;AccountName=ocp73883544777;AccountKey=z0v5e/JORvhKJFS/YD9AbYq5LOUz940m9IuCvVcddTP5JnCQA/F5cTtrJKll8gg16qBlexJenvzY+AStJe83Og==;EndpointSuffix=core.windows.net"
container_name = "azureml"

def uploadToBlobStorage(file_path,file_name):
   blob_service_client = BlobServiceClient.from_connection_string(connection_string)
   blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
   with open(file_path,”rb”) as data:
      blob_client.upload_blob(data)
      print(f”Uploaded {file_name}.”)

# calling a function to perform upload
uploadToBlobStorage('mon_best_model','best_model_path')
uploadToBlobStorage('tokenizer','tokenizer_path')

# Déclaration des variables globales
model = None
tokenise = None
#ws = Workspace.from_config()




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
