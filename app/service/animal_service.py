from model import animal
from data.config import engine, Session

import cv2
import numpy as np

db = Session()


def pre_processar_imagem(img_path):
    # Carregando imagem
    image = cv2.imread(img_path)

    # Equalizando imagem com metodo clahe
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_planes = list(cv2.split(lab))
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5,5))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    clahe_equalized = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    # Convertendo imagem para escala de cinza
    gray = cv2.cvtColor(clahe_equalized, cv2.COLOR_RGB2GRAY)

    # Equalizando o histograma da imagem cinza
    eq = cv2.equalizeHist(gray)

    # Redimensionando a imagem
    resized = redimensionar_imagem(eq)

    # Aplicando blur de mediana
    median_blurred = cv2.medianBlur(resized, 5)

    # Aplicando blur gaussiano
    gaussian_blurred = cv2.GaussianBlur(median_blurred, (5, 5), 0)
    
    return gaussian_blurred


def redimensionar_imagem(image, i=''):
    # Obtendo o tamanho original da imagem
    original_height, original_width = image.shape[:2]
    
    # Definindo o novo tamanho da imagem
    new_width = 220
    ratio = new_width / original_width
    new_height = int(original_height * ratio)

    # Definindo qual o metodo de interpolacao vai ser usado
    if (original_width > 220):
        i = cv2.INTER_AREA
    elif (original_width <= 220):
        i = cv2.INTER_LANCZOS4

    return cv2.resize(image, (new_width, new_height), interpolation=i)


def segmentar_imagem(image_path, threshold=90):
    # Aplicando o pre-processamento na imagem
    image = pre_processar_imagem(image_path)
    
    # Criaando uma mascara inicialmente preta
    mask = np.zeros_like(image, dtype=np.uint8)

    # Aplicando limiar simples
    mask[image < threshold] = 255

    # Aplicando pos processamento na mascara para remoção de ruidos
    final_mask = pos_processar_imagem(mask)

    return final_mask


def pos_processar_imagem(mask):
    # Aplicando abertura morfologica
    kernel = np.ones((3, 3), np.uint8) 
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
    
    return opened


def extrair_caracteristicas(image, filename):
    # Criando uma mascara com base na imagem original
    result = np.zeros_like(image)

    # Encontrando contornos na imagem
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 600]

    # Calculando a area total da pegada e perimetro total da pegada
    total_area = sum(cv2.contourArea(cnt) for cnt in filtered_contours)
    total_perimeter = sum(cv2.arcLength(cnt, True) for cnt in filtered_contours)

    # Inicializando a contagem de centroides
    centroid_count = 0  
    
    for cnt in filtered_contours:
        M = cv2.moments(cnt)

        if M['m00'] != 0:
            # Identificando os centroides de cada regiao
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(result, (cx, cy), 5, (0, 0, 255), -1)
    
            # Incrementando a contagem de centroides
            centroid_count += 1  

    # Encontrando o circulo que melhor se ajusta a almofada
    (x, y), radius = cv2.minEnclosingCircle(filtered_contours[0])
    center = (int(x), int(y))
    radius = int(radius)

    # Desenhando o circulo externo
    cv2.circle(result, center, radius, (0, 255, 0), 2)

    # Calculando a area do circulo ajustado
    area_circulo_ajustado = np.pi * radius**2

    # Calculando a circularidade
    circularidade = cv2.contourArea(filtered_contours[0]) / area_circulo_ajustado

    return {
        'circularidade_almofada': circularidade,
        'qtde_regioes': centroid_count,
        'area': total_area,
        'perimetro': total_perimeter
    }


def get_animal(id):
    try:
        db_record = db.query(animal.Animal).filter(animal.Animal.animal_id == int(id)).first()
        return db_record.to_json()
    except Exception as e:
        print(e)
        return 'Não foi possível obter o animal.'