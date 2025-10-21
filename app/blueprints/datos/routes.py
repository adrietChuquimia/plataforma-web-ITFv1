from flask import Blueprint, render_template, current_app, jsonify
import json, os

piezas_bp = Blueprint("piezas", __name__)

# Ruta para el diccionario en HTML
@piezas_bp.route("/piezas")
def mostrar_piezas():
    with open("conocimiento.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    return render_template("diccionario.html", piezas=datos)

# Ruta para devolver los datos como JSON 
@piezas_bp.route("/componentes")
def obtener_componentes():
    with open("conocimiento.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    return jsonify(datos)
