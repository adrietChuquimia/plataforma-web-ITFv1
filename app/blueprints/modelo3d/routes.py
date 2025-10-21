from huggingface_hub import hf_hub_download
import os
from flask import Blueprint, render_template, current_app

mod3d_bp = Blueprint('mod3d', __name__)

@mod3d_bp.route("/mod3d", endpoint="mod3d")
def mod3d():
    # Lista de archivos .glb en HF Hub
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

    REPO_ID = "Adriet1/modelos3d"  # Reemplaza con tu repo HF Hub

    static_models_folder = os.path.join(current_app.static_folder, "modelos")
    os.makedirs(static_models_folder, exist_ok=True)

    for archivo in archivos_glb:
        dst_glb = os.path.join(static_models_folder, archivo)
        # Solo descarga si no existe
        if not os.path.exists(dst_glb):
            # Descarga y devuelve la ruta temporal del archivo
            src_glb = hf_hub_download(repo_id=REPO_ID, filename=archivo)
            # Copia al folder static para que HTML pueda usarlo
            with open(src_glb, "rb") as f_src:
                with open(dst_glb, "wb") as f_dst:
                    f_dst.write(f_src.read())

    return render_template("modelo3d.html")
