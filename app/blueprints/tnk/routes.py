from flask import Blueprint, render_template

tnk_bp = Blueprint('tnk', __name__)

@tnk_bp.route("/tnk", endpoint="tnk")
def tnk():
    return render_template("gracias.html")