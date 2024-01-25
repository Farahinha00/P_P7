from fastapi import FastAPI
import tensorflow as tf
import joblib
from azureml.core.model import Model
from azureml.core import Workspace
from script_inf import make_inference  # Assurez-vous que script_inf.py est dans le même dossier

app = FastAPI()

# Déclaration des variables globales
model = None
tokenise = None
ws = Workspace.from_config() 
def init():
    global model
    global tokenise

    # Obtenez le chemin des modèles stockés dans Azure ML
    best_model_path = Model.get_model_path(model_name='best_model', version=1, _workspace=ws)
    tokenizer_path = Model.get_model_path(model_name='tokenizer', version=1, _workspace=ws)

    try:
        # Chargez le tokenizer
        tokenise = joblib.load(tokenizer_path)
    except Exception as e:
        print(f"Erreur lors du chargement du tokenizer : {e}")
        
    try:
        # Chargez le modèle Keras
        model = tf.keras.models.load_model(best_model_path)
    except Exception as e:
        print(f"Erreur lors du chargement du modèle Keras : {e}")

# Événement de démarrage pour exécuter la fonction init
@app.on_event("startup")
async def startup_event():
    init()

@app.post("/predict/{raw_data}")
async def predict(raw_data: str):
    # Effectuer l'inférence
    prediction = make_inference(raw_data,tokenise,model)

    # Retourner la prédiction
    return {"Prédiction"}
