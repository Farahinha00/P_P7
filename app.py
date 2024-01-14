from fastapi import FastAPI
import tensorflow as tf
import joblib
import requests
from script_inf import make_inference  # Assure-toi que script_inf.py est dans le même dossier

app = FastAPI()

# Charger le modèle et le tokenizer
best_model = tf.keras.models.load_model('https://ocp7.blob.core.windows.net/common/mon_best_model.h5')
tokenizer = joblib.load('https://ocp7.blob.core.windows.net/common/tokenizer.pkl')

@app.get("/predict/{raw_data}")
async def predict(raw_data: str):
    # Effectuer l'inférence
    prediction = make_inference(raw_data)

    # Retourner la prédiction
    return {"Prédiction": prediction}
