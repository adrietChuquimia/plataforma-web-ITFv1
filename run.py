from flask import Flask
from app import create_app

app = Flask(__name__)
app.secret_key = "ITF20241RAVPVEFV1A2025" 

app = create_app()

if __name__ == "__main__":
    app.run()
