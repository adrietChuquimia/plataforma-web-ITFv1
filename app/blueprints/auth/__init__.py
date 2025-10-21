from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

from . import routes  # Importa las rutas después de definir el blueprint
