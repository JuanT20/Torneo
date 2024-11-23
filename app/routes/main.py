from flask import Blueprint, render_template, request, jsonify, redirect, url_for,session

from models.db import insertar_torneo,verificar_usuario,insertar_usuario


app_routes = Blueprint('app_routes', __name__)  # Creamos una instancia de Flask

# Ruta principal: Landing Page
@app_routes.route('/')
def landing():
    return render_template('index.html')


@app_routes.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        data = request.get_json()
        
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        print(data)
         # Validaciones de campos
        if not correo or not correo.strip():
            return jsonify({'error': 'El correo es obligatorio'}), 400
        
        if not contrasena or not contrasena.strip():
            return jsonify({'error': 'La contraseña es obligatoria'}), 400
        
        # Validar el correo y la contraseña
        
        # Lógica para verificar el usuario en la base de datos
        usuario = verificar_usuario(correo, contrasena)
        
        if not usuario:
            return jsonify({'error': 'Correo o contraseña incorrectos'}), 401
        
         # Si el usuario es válido, almacena su información en la sesión
        session['id_usuario'] = usuario['id_usuario']  # Guarda el id_usuario en la sesión
        
       

         # Respuesta exitosa
        return jsonify({'mensaje': 'Login correcto', 'redirect_url': '/register-torneo'}), 200
    
@app_routes.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    return jsonify({'mensaje': 'Sesión cerrada correctamente'}), 200

@app_routes.route('/singUp', methods=['GET', 'POST'])
def singUp():
    
    if request.method == 'GET':
        return render_template('singUp.html')

    if request.method == 'POST':
        data = request.get_json()
        
        nombre = data.get('nombre')
        correo = data.get('correo')
        contrasena = data.get('password')
        
         # Validaciones de campos
        if not nombre or not nombre.strip():
            return jsonify({'error': 'El nombre es obligatorio'}), 400
        
        if not correo or not correo.strip():
            return jsonify({'error': 'El correo es obligatorio'}), 400
        
        if not contrasena or not contrasena.strip():
            return jsonify({'error': 'La contraseña es obligatoria'}), 400
        
        try:
            insertar_usuario(nombre, correo, contrasena)
            return jsonify({'mensaje': 'Usuario registrado correctamente', 'redirect_url': '/login'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app_routes.route('/dashboard')
def dashboard():
    # Verifica si el usuario está autenticado
    if 'id_usuario' not in session:
        return jsonify({'error': 'No has iniciado sesión'}), 401
    
    id_usuario = session['id_usuario']
    return render_template('dashboard.html', id_usuario=id_usuario)

@app_routes.route('/register-torneo', methods=['GET','POST'])
def addTorneos():
    if request.method == 'GET':
        return render_template('registerTorneo.html')
    
    if request.method == 'POST':
        
        data = request.get_json() #Recibimos los datos en formato Json
      
        # Extraemos los datos correctamente desde el JSON
        nombreTorneo = data.get('nombreTorneo')
        tipoTorneo = data.get('tipoTorneo')
        formatoTorneo = data.get('formatoTorneo')
        numeroEquipos = data.get('numeroEquipos')
        fechaInicio = data.get('fechaInicio')
        fechaFin = data.get('fechaFin')
        
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return jsonify({'error:', 'Usuario no autenticado'}), 401
        
        if not nombreTorneo or not tipoTorneo or not formatoTorneo or not numeroEquipos or not fechaInicio or not fechaFin:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400
        
        # if not nombreTorneo or nombreTorneo.strip() == '':
        #     return jsonify({'error': 'El nombre del torneo es obligatorio'}), 400
        
        try:
            insertar_torneo(id_usuario,nombreTorneo, tipoTorneo, formatoTorneo, numeroEquipos, fechaInicio, fechaFin)
            return jsonify({'mensaje': f'Torneo "{nombreTorneo}" registrado correctamente'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    
  



