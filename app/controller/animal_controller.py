import joblib
import numpy as np
import pandas as pd

import os 

from flask import jsonify, make_response, render_template, request
from sklearn.ensemble import RandomForestClassifier

import service.animal_service as service

# Carregando o modelo de ML
model = joblib.load('./resource/modelo_rf.joblib')


def index():
    return render_template('index.html')


def predict():
    # Salvando a imagem enviada no formulario
    image_file = request.files['upload-file']
    image_path = './resource/uploads/' + image_file.filename
    image_file.save(image_path)
    
    # Extraindo o nparray das caracteristicas da imagem
    if image_file.filename.endswith('.jpg') or image_file.filename.endswith('.png'):
        seg_image = service.segmentar_imagem(image_path)

        if seg_image is not None:
            features = service.extrair_caracteristicas(seg_image, image_file.filename)

            if features is not None:
                # Criando o DataFrame com as caracteristicas
                df = pd.DataFrame([features])
                df.columns = ['circularidade_almofada', 'qtde_regioes', 'area', 'perimetro']

    # Apagando a imagem do diretório
    os.remove(image_path)

    # Predizendo a classe do animal
    predicted_class = model.predict(df)

    # Pegando os dados do animal pela classe
    animal_predicted = service.get_animal(predicted_class[0])

    return jsonify(prediction=animal_predicted)