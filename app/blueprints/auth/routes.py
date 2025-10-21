from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import auth_bp
from .firebase_admin_setup import firebase_auth
import requests
from firebase_admin import auth, credentials
import firebase_admin

API_KEY = "AIzaSyBIPRxWiudVylifIv2tKYYNjPrtGa2CIPA"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Llamada a Firebase REST API
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if "error" in data:
            flash("Correo o contraseña incorrectos", "danger")
            return render_template('login.html')

        # Verificar si el usuario está activo
        try:
            user = auth.get_user_by_email(email)
            if user.disabled:
                flash("Tu cuenta está desactivada. Contacta al administrador.", "danger")
                return render_template('login.html')
        except Exception as e:
            flash("Error al verificar estado del usuario", "danger")
            return render_template('login.html')

        session['uid'] = data["localId"]
        session['email'] = email

        if email.startswith("ADM") or email.startswith("adm"):
            session['admin'] = True
            flash("Bienvenido al panel de administración", "success")
            return redirect(url_for('auth.dashboard'))
        else:
            flash(f"Bienvenido {email}", "success")
            return render_template('menuEst.html', email=email)

    return render_template('login.html')

# Ruta para CERRAR SESIÓN 
@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("Has cerrado sesión", "success")
    return redirect(url_for('auth.login'))

# Ruta para CREAR USUARIO
@auth_bp.route('/create_user', methods=['POST'])
def create_user():
    if not session.get('admin'):
        flash("Acceso denegado", "danger")
        return redirect(url_for('auth.login'))
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        flash("Email y contraseña son requeridos", "danger")
        return redirect(url_for('auth.dashboard'))
    
    try:
        user = auth.create_user(
            email=email, 
            password=password,
            disabled=False  
        )
        flash(f"Usuario {email} creado correctamente", "success")
    except auth.EmailAlreadyExistsError:
        flash("El correo ya está registrado", "danger")
    except Exception as e:
        flash(f"Error al crear usuario: {str(e)}", "danger")
    
    return redirect(url_for('auth.dashboard'))

# Ruta para ELIMINAR USUARIO
@auth_bp.route('/delete_user/<uid>', methods=['POST'])
def delete_user(uid): 
    if not session.get('admin'):
        flash("Acceso denegado", "danger")
        return redirect(url_for('auth.login'))
    
    try:
        # Verificar que no se elimine a sí mismo
        if session.get('uid') == uid:
            flash("No puedes eliminar tu propia cuenta", "danger")
            return redirect(url_for('auth.dashboard'))
            
        user = auth.get_user(uid)
        auth.delete_user(uid)
        flash(f"Usuario {user.email} eliminado correctamente", "success")
    except Exception as e:
        flash(f"Error al eliminar usuario: {str(e)}", "danger")
    
    return redirect(url_for('auth.dashboard'))

# Ruta para CAMBIAR CONTRASEÑA
@auth_bp.route('/change_password/<uid>', methods=['POST'])
def change_password(uid):
    if not session.get('admin'):
        flash("Acceso denegado", "danger")
        return redirect(url_for('auth.login'))
    
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not new_password or not confirm_password:
        flash("Ambas contraseñas son requeridas", "danger")
        return redirect(url_for('auth.dashboard'))
    
    if new_password != confirm_password:
        flash("Las contraseñas no coinciden", "danger")
        return redirect(url_for('auth.dashboard'))
    
    if len(new_password) < 6:
        flash("La contraseña debe tener al menos 6 caracteres", "danger")
        return redirect(url_for('auth.dashboard'))
    
    try:
        user = auth.get_user(uid)
        auth.update_user(uid, password=new_password)
        flash(f"Contraseña cambiada para {user.email}", "success")
    except Exception as e:
        flash(f"Error al cambiar contraseña: {str(e)}", "danger")
    
    return redirect(url_for('auth.dashboard'))

# Ruta para ACTIVAR/DESACTIVAR USUARIO
@auth_bp.route('/toggle_user_status/<uid>', methods=['POST'])
def toggle_user_status(uid):
    if not session.get('admin'):
        flash("Acceso denegado", "danger")
        return redirect(url_for('auth.login'))
    
    try:
        # Verificar que no se desactive a sí mismo
        if session.get('uid') == uid:
            flash("No puedes desactivar tu propia cuenta", "danger")
            return redirect(url_for('auth.dashboard'))
            
        user = auth.get_user(uid)
        new_status = not user.disabled  # Cambiar el estado actual
        
        auth.update_user(uid, disabled=new_status)
        
        status_text = "desactivado" if new_status else "activado"
        flash(f"Usuario {user.email} {status_text} correctamente", "success")
        
    except Exception as e:
        flash(f"Error al cambiar estado del usuario: {str(e)}", "danger")
    
    return redirect(url_for('auth.dashboard'))

# Función para obtener usuarios
def get_all_users():
    users = []
    try:
        # Verificar que Firebase esté inicializado
        firebase_admin.get_app()
        
        # Listar usuarios 
        users_page = auth.list_users(max_results=1000)
        users = list(users_page.users)        
        
        while users_page.has_next_page:
            users_page = auth.list_users(
                page_token=users_page.next_page_token,
                max_results=1000
            )
            additional_users = list(users_page.users)
            users.extend(additional_users)
        
    except ValueError as e:
        raise Exception("Firebase no está inicializado correctamente")
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        raise    
    
    return users

# DASHBOARD 
@auth_bp.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        flash("Acceso denegado - Solo administradores", "danger")
        return redirect(url_for('auth.login'))
    
    try:
        # Cargar usuarios al acceder al dashboard
        users = get_all_users()
        users_count = len(users)
        
        # Separar usuarios activos e inactivos
        active_users = sum(1 for user in users if not user.disabled)
        inactive_users = users_count - active_users
        
    except Exception as e:
        users = []
        users_count = active_users = inactive_users = 0
        flash(f"Error al cargar usuarios: {str(e)}", "danger")
    
    return render_template('admin_dashboard.html', 
                         users=users, 
                         users_count=users_count,
                         active_users=active_users,
                         inactive_users=inactive_users,
                         current_admin_uid=session.get('uid'))

# Ruta para RECARGAR USUARIOS (AJAX)
@auth_bp.route('/reload_users')
def reload_users():
    """Ruta para forzar la recarga de usuarios"""
    if not session.get('admin'):
        return redirect(url_for('auth.login'))
    
    try:
        users = get_all_users()
        flash(f"Lista actualizada: {len(users)} usuarios encontrados", "success")
    except Exception as e:
        flash(f"Error al actualizar lista: {str(e)}", "danger")
    
    return redirect(url_for('auth.dashboard'))

# obtener usuarios (para AJAX)
@auth_bp.route('/api/users')
def api_get_users():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        users = get_all_users()
        users_data = []
        
        for user in users:
            users_data.append({
                'uid': user.uid,
                'email': user.email or 'Sin email',
                'disabled': user.disabled,
                'creation_timestamp': user.user_metadata.creation_timestamp,
                'last_sign_in_timestamp': getattr(user.user_metadata, 'last_sign_in_timestamp', None)
            })
        
        return jsonify({
            'users': users_data,
            'count': len(users_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

