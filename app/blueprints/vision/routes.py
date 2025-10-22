import io
import base64
import json
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image
from flask import Blueprint, request, jsonify, render_template
from huggingface_hub import hf_hub_download

# DESCARGA DEL MODELO DESDE HUGGING FACE HUB

# Repo y nombre de archivo en HF Hub
REPO_ID = "Adriet1/vision"  # reemplaza con tu usuario y repo
H5_FILENAME = "keras_model.h5"

# Descarga el archivo .h5 y obtiene la ruta local
MODEL_PATH = hf_hub_download(repo_id=REPO_ID, filename=H5_FILENAME)

# Cargar modelo con TensorFlow/Keras
model = tf.keras.models.load_model(MODEL_PATH)
print("Modelo cargado desde:", MODEL_PATH)

# CONFIGURACIÓN DEL BLUEPRINT
vision_bp = Blueprint('vision', __name__)

# Cargar base de conocimiento
COMPONENTES_JSON = "conocimiento.json"
with open(COMPONENTES_JSON, "r", encoding="utf-8") as f:
    conocimiento = json.load(f)

# Clases en el mismo orden que el modelo
class_names = list(conocimiento.keys())

# FUNCIONES AUX
def base64_to_image(b64_string):
    """Convierte Base64 a imagen numpy lista para el modelo"""
    img_data = base64.b64decode(b64_string)
    img = Image.open(io.BytesIO(img_data)).convert('RGB')
    return np.array(img)

def preprocesar_imagen(img, size=(224, 224)):
    """Redimensiona y normaliza la imagen para el modelo"""
    img = cv2.resize(img, size)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def interpretar_prediccion(predicciones, umbral_confianza=0.85):
    """Aplica reglas sobre la predicción para dar salida confiable"""
    idx_max = np.argmax(predicciones)
    pieza = class_names[idx_max]
    confianza = float(np.max(predicciones))
    
    info = []
    mensaje = ""
    
    # Regla: clase desconocida
    if confianza < 0.4:
        pieza = "Desconocido"
        info = ["No se identificó componente, fuera de las clases entrenadas"]
        mensaje = "Clase desconocida"
    
    # Regla: confianza dudosa
    elif confianza < umbral_confianza and confianza >= 0.4:
        info = [f"Sospecho que es un {pieza}, pero la predicción no es lo suficientemente confiable para mostrar información detallada."]
        mensaje = "Predicción dudosa"
    
    # Regla: confianza suficiente
    else:
        info = conocimiento.get(pieza, ["No hay información disponible"])
        mensaje = "Predicción confiable"
    
    # Regla: top-2 comparativa
    top2_idx = np.argsort(predicciones[0])[-2:]
    if len(top2_idx) == 2 and confianza >= umbral_confianza:
        diferencia = predicciones[0][top2_idx[1]] - predicciones[0][top2_idx[0]]
        if abs(diferencia) < 0.2:
            info.append(f"Nota: Podría ser {class_names[top2_idx[1]]} o {class_names[top2_idx[0]]}, la confianza no es absoluta.")

    return {
        "pieza": pieza,
        "probabilidad": round(confianza * 100, 2),
        "informacion": info,
        "mensaje": mensaje
    }

# RUTAS DEL BLUEPRINT
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

        # Convertir Base64 -> imagen
        img = base64_to_image(img_b64)

        # Preprocesar para el modelo
        img = preprocesar_imagen(img)

        # Predicción
        predicciones = model.predict(img)
        resultado = interpretar_prediccion(predicciones, umbral_confianza=0.8)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
