import tensorflow as tf
import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model
from keras.layers import Dense, Embedding, LSTM, Dropout, Flatten, SimpleRNN
import joblib


def tokenize_data(data,tokenizer,maxlen=None):
    X = tokenizer.texts_to_sequences(data)
    return pad_sequences(X,maxlen=maxlen)

def model_predict(texts):
    # Assure-toi que 'texts' est prétraité de la même manière que les données d'entraînement
    processed_texts = tokenize_data(texts,tokenizer,maxlen=50)
    return best_model.predict(processed_texts)

def make_inference(input_data):
    # Prédiction à l'aide du modèle
    processed_data = tokenize_data([input_data],tokenizer,maxlen=50)
    prediction = best_model.predict(processed_data)

    # Affichage des résultats de la prédiction
    print("Prédiction brute du modèle : ", prediction)
    
    explainer = LimeTextExplainer(class_names=['bad', 'good'])
    exp = explainer.explain_instance(input_data, model_predict, num_features=10)
    exp.show_in_notebook(text=True)
    
    return prediction, exp


