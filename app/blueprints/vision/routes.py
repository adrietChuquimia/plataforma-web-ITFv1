import io
import base64
import json
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image
from flask import Blueprint, request, jsonify, render_template
from huggingface_hub import hf_hub_download

REPO_ID = "Adriet1/visionv1"
H5_FILENAME = "keras_model.h5"

MODEL_PATH = hf_hub_download(repo_id=REPO_ID, filename=H5_FILENAME)
model = tf.keras.models.load_model(MODEL_PATH)
print("Modelo cargado desde:", MODEL_PATH)

vision_bp = Blueprint('vision', __name__)

COMPONENTES_JSON = "conocimiento.json"
with open(COMPONENTES_JSON, "r", encoding="utf-8") as f:
    conocimiento = json.load(f)
class_names = list(conocimiento.keys())

def base64_to_image(b64_string):
    """Convierte Base64 a imagen numpy lista para el modelo"""
    img_data = base64.b64decode(b64_string)
    img = Image.open(io.BytesIO(img_data)).convert('RGB')
    return np.array(img)

def preprocesar_imagen(img, size=(224, 224)):
    # Ajuste de brillo/contraste
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.convertScaleAbs(img, alpha=1.1, beta=10)  # ligera mejora
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Mantener proporción y padding
    h, w = img.shape[:2]
    scale = min(size[0]/h, size[1]/w)
    nh, nw = int(h*scale), int(w*scale)
    img_resized = cv2.resize(img, (nw, nh))
    top = (size[0] - nh) // 2
    bottom = size[0] - nh - top
    left = (size[1] - nw) // 2
    right = size[1] - nw - left
    img_padded = cv2.copyMakeBorder(img_resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0,0,0])

    # Normalización Teachables Machine
    img_padded = img_padded.astype("float32") / 255.0
    img_padded = np.expand_dims(img_padded, axis=0)
    return img_padded

def interpretar_prediccion(predicciones, umbral_confianza=0.8):
    predicciones = predicciones.flatten()
    idx_max = np.argmax(predicciones)
    pieza = class_names[idx_max]
    confianza = float(predicciones[idx_max])

    if confianza < umbral_confianza:
        pieza = "Desconocido"
        info = ["No se identificó componente, fuera de las clases entrenadas"]
    else:
        info = conocimiento.get(pieza, ["No hay información disponible"])

    return {
        "pieza": pieza,
        "probabilidad": round(confianza * 100, 2),
        "informacion": info
    }

@vision_bp.route('/vision')
def vision():
    return render_template('vision.html')

@vision_bp.route('/predict', methods=["POST"])
def predict():
    try:
        data = request.get_json()
        img_b64 = data.get("imagen")
        if not img_b64:
            return jsonify({"error": "No se recibió la imagen"}), 400
        
        img = base64_to_image(img_b64)
        img = preprocesar_imagen(img)
        predicciones = model.predict(img)
        resultado = interpretar_prediccion(predicciones, umbral_confianza=0.8)
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
