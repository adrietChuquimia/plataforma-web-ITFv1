# app/firebase_admin_setup.py
import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase():
    if firebase_admin._apps:
        return firebase_admin.get_app()

    # 1) Intentar variable de entorno RAW
    firebase_json = os.getenv("FIREBASE_KEY")

    # 2) Si no existe, intentar variable en base64 (opcional)
    firebase_b64 = os.getenv("FIREBASE_KEY_B64")

    # 3) Si no existe ninguna variable, fallback a archivo local
    if firebase_json:
        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado desde FIREBASE_KEY (env).")
        return firebase_admin.get_app()
    elif firebase_b64:
        decoded = base64.b64decode(firebase_b64).decode("utf-8")
        cred_dict = json.loads(decoded)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado desde FIREBASE_KEY_B64 (env).")
        return firebase_admin.get_app()
    else:
        # Usar archivo local (solo desarrollo)
        if os.path.exists("firebase_llave.json"):
            cred = credentials.Certificate("firebase_llave.json")
            firebase_admin.initialize_app(cred)
            print("Firebase inicializado desde firebase_llave.json (local).")
            return firebase_admin.get_app()
        else:
            raise RuntimeError(
                "No se encontró credencial de Firebase. "
                "Define FIREBASE_KEY (o FIREBASE_KEY_B64) o agrega firebase_llave.json localmente."
            )

# Inicializar al importar
initialize_firebase()
firebase_auth = auth
