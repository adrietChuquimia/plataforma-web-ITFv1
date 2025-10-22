import os
from flask import Blueprint, render_template, current_app

mod3d_bp = Blueprint('mod3d', __name__)

@mod3d_bp.route("/mod3d", endpoint="mod3d")
def mod3d():
# Lista de modelo
    archivos_glb = [
        "1950Jeep.glb",
        "1960Dodge Charger.glb",
        "1972_Bursley_Defiance.glb",
        "1980Toyota AE86.glb",
        "1994 Nissan 180MX.glb",
        "2000Mazda RX-7.glb",
        "2010CAR Model.glb",
        "2020Nissan GTR.glb",
        "engine.glb"
    ]
    # Ruta completa a la carpeta de modelos dentro de /static
    static_models_folder = os.path.join(current_app.static_folder, "modelos")
    os.makedirs(static_models_folder, exist_ok=True)

    # Opcional: verifica que los archivos existan localmente
    modelos_faltantes = [f for f in archivos_glb if not os.path.exists(os.path.join(static_models_folder, f))]
    if modelos_faltantes:
        print(f"Los siguientes modelos no se encuentran en '{static_models_folder}': {modelos_faltantes}")
    # Renderiza la plantilla que carga los modelos desde /static/modelos/
    return render_template("modelo3d.html", modelos=archivos_glb)
