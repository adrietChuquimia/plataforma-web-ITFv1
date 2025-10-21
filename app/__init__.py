from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'ITF20241RAVPVEFV1A2025'

    # Importar y registrar Blueprint principal
    from app.blueprints.main.routes import main
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.trivia.trivia import trivia_bp
    from app.blueprints.datos.routes import piezas_bp
    from app.blueprints.modelo3d.routes import mod3d_bp
    from app.blueprints.vision.routes import vision_bp
    from app.blueprints.tnk.routes import tnk_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(trivia_bp)
    app.register_blueprint(piezas_bp)
    app.register_blueprint(mod3d_bp)
    app.register_blueprint(vision_bp)
    app.register_blueprint(tnk_bp)

    return app
