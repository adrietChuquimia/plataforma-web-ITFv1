from flask import Flask
from app import create_app

app = Flask(__name__)
app.secret_key = "ITF20241RAVPVEFV1A2025" 

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)