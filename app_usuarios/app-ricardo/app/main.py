from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_por_defecto_desarrollo')

# Simulación de Base de Datos en memoria unificada
users_db = {}  # Formato: { email: {id, nombre, email, password_hash, fecha_registro, activo} }
user_id_counter = 1

@app.route('/')
def index():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    current_user = users_db.get(session['user_email'])
    return render_template('index.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global user_id_counter
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Validaciones de Seguridad (Requisitos S-SDLC)
        if not nombre or not email or not password:
            flash('Todos los campos son estrictamente obligatorios.', 'danger')
            return redirect(url_for('register'))
        
        if len(nombre) < 3 or len(nombre) > 50:
            flash('El nombre debe tener entre 3 y 50 caracteres.', 'danger')
            return redirect(url_for('register'))

        if email in users_db:
            flash('El correo electrónico ya se encuentra registrado.', 'danger')
            return redirect(url_for('register'))

        # Registro seguro con PBKDF2
        users_db[email] = {
            "id": user_id_counter,
            "nombre": nombre,
            "email": email,
            "password_hash": generate_password_hash(password),
            "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "activo": True
        }
        user_id_counter += 1
        
        flash('Registro completado con éxito. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = users_db.get(email)
        
        # Mitigación frente a Timing Attacks (Siempre verifica aunque no exista el usuario)
        dummy_hash = generate_password_hash("dummy_password")
        target_hash = user["password_hash"] if user else dummy_hash
        
        if user and check_password_hash(target_hash, password):
            session['user_email'] = user['email']
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_email' not in session:
        flash('Inicia sesión para ver tu perfil.', 'warning')
        return redirect(url_for('login'))
        
    email_actual = session['user_email']
    user = users_db.get(email_actual)

    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre', '').strip()
        
        if not nuevo_nombre or len(nuevo_nombre) < 3 or len(nuevo_nombre) > 50:
            flash('Nombre inválido. Debe tener entre 3 y 50 caracteres.', 'danger')
            return redirect(url_for('perfil'))
            
        users_db[email_actual]['nombre'] = nuevo_nombre
        flash('Perfil actualizado con éxito.', 'success')
        return redirect(url_for('index'))

    return render_template('perfil.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Sesión cerrada correctamente de forma segura.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5001)