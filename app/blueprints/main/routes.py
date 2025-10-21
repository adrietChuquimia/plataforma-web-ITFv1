from flask import Blueprint, session, redirect, url_for, render_template

main = Blueprint('main', __name__)

@main.route("/", endpoint="inicio")
def inicio():
    return render_template("index.html")

@main.route("/mecanica", endpoint="mecanica")
def mecanica():
    return render_template("MEC.html")

@main.route("/autotronica", endpoint="autotronica")
def autotronica():
    return render_template("AUT.html")

#Llamada al menu de estudiantes 
@main.route('/menuest')
def menuest():
    return render_template('menuEst.html')