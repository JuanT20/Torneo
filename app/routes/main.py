from flask import Blueprint, render_template, request, jsonify, redirect, url_for,session,current_app
from utils.funtions import allowed_file,save_logo,generar_fixtures
from models.db import insertar_torneo,verificar_usuario,insertar_usuario,save_team_to_db,get_teams,insertar_jugadores,get_tournaments
import os



app_routes = Blueprint('app_routes', __name__)  # Creamos una instancia de Flask

# Inicio Ruta principal: Landing Page
@app_routes.route('/')
def landing():
    return render_template('index.html')

# Fin Ruta principal: Landing Page

#Inicio Ruta Login
@app_routes.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        data = request.get_json()
        
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        # print(data)
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
        id_usuario = usuario['id_usuario']
        
       
 # Verificar si el usuario ya tiene torneos
        torneos = get_tournaments(id_usuario)  # Asume que esta función devuelve los torneos de un usuario
        
        # Ajustar la URL de redirección dependiendo de si tiene torneos o no
        if torneos:
            redirect_url = '/dashboard'  # Si tiene torneos, redirigir al dashboard
        else:
            redirect_url = '/register-torneo'  # Si no tiene torneos, redirigir a la creación de torneos
        
        # Respuesta exitosa
        return jsonify({'mensaje': 'Login correcto', 'redirect_url': redirect_url}), 200
#Fin Ruta Login

#Inicio Ruta Logout   
@app_routes.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    return jsonify({'mensaje': 'Sesión cerrada correctamente'}), 200

#Fin Ruta Logout

#Inicio Ruta singUp
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
#Fin Ruta singUp

# Inicio Ruta Dashboard
@app_routes.route('/dashboard')
def dashboard():
    # Verifica si el usuario está autenticado
    if 'id_usuario' not in session:
        return jsonify({'error': 'No has iniciado sesión'}), 401
    
    id_usuario = session['id_usuario']
    torneos = get_tournaments(id_usuario)  # Obtén los torneos del usuario logueado

    return render_template('dashboard.html', id_usuario=id_usuario, torneos=torneos)


# Fin Ruta Dashboard

#Inicio Ruta register-torneo
@app_routes.route('/register-torneo', methods=['GET', 'POST'])
def addTorneos():
    if request.method == 'GET':
        return render_template('registerTorneo.html')
    
    if request.method == 'POST':
        data = request.get_json()

        # Extraemos datos
        nombreTorneo = data.get('nombreTorneo')
        tipoTorneo = data.get('tipoTorneo')
        formatoTorneo = data.get('formatoTorneo')
        numeroEquipos = data.get('numeroEquipos')
        fechaInicio = data.get('fechaInicio')
        fechaFin = data.get('fechaFin')

        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return jsonify({'error': 'Usuario no autenticado'}), 401

        if not all([nombreTorneo, tipoTorneo, formatoTorneo, numeroEquipos, fechaInicio, fechaFin]):
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        try:
            id_torneo = insertar_torneo(
                id_usuario, nombreTorneo, tipoTorneo, formatoTorneo, numeroEquipos, fechaInicio, fechaFin
            )
            
            # Redirigimos al registro de equipos con el ID del torneo
            return jsonify({'mensaje': 'Registro correcto', 'redirect_url': f'/register-equipos?id_torneo={id_torneo}'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#Fin Ruta register-torneo

#Inicio Ruta register-equipos
@app_routes.route('/register-equipos', methods=['GET', 'POST'])
def addEquipos():
    if request.method == 'GET':
        id_torneo = request.args.get('id_torneo')
        # print(f"ID del torneo recibido: {id_torneo}") 
        if not id_torneo:
            return jsonify({'error': 'ID del torneo no especificado'}), 400
        
        return render_template('registroEquipos.html', id_torneo=id_torneo)

    if request.method == 'POST':
        id_torneo = request.form.get('id_torneo')  # ID del torneo desde el formulario
        # print(f"ID del torneo recibido: {id_torneo}")  # Debug
        equipos = request.form.to_dict()
        archivos = request.files

        try:
            for key, value in equipos.items():
                if key.startswith("equipo"):
                    equipo_index = key.replace("equipo", "")
                    team_name = value
                    team_logo = archivos.get(f"escudo{equipo_index}")

                    # Verificar si se subió un archivo válido
                    if team_logo and allowed_file(team_logo.filename):
                        logo_path = save_logo(team_logo, current_app.config['UPLOAD_FOLDER'])
                    else:
                        logo_path = os.path.join('static', 'img', 'escudos', 'default-escudo.svg')

                    # Guardar equipo y vincularlo al torneo
                    save_team_to_db(team_name, logo_path, id_torneo)

            return jsonify({'success': True, 'redirect_url': f'/equipos?id_torneo={id_torneo}'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

#Fin Ruta register-equipos
    
        
# Inicio Ruta equipos
@app_routes.route('/equipos', methods=['GET'])
def equipos():
    # Obtener el ID del torneo desde los parámetros de la URL
    id_torneo = request.args.get('id_torneo')
    
    if not id_torneo:
        return jsonify({'error': 'ID del torneo no proporcionado'}), 400

    try:
        equipos = get_teams(id_torneo)  # Pasar el id_torneo a la función
        return render_template('equipos.html', equipos=equipos, id_torneo=id_torneo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# FinRuta equipos

#Inicio Ruta register-jugadores

@app_routes.route('/register-jugadores', methods=['GET', 'POST'])
def addJugadores():
    if request.method == 'GET':
         # Obtener el ID del equipo desde la URL
        id_equipo = request.args.get('id_equipo')  
        if not id_equipo:
            return "ID del equipo no proporcionado", 400  # Error si falta el ID

        return render_template('registroJugadores.html', id_equipo=id_equipo)
    
    if request.method == 'POST':
        data = request.get_json()  # Recibir datos en formato JSON

        # Extraer datos del JSON
        idEquipo = data.get('idEquipo')
        idJugador = data.get('idJugador')
        nombre = data.get('nombre')
        posicion = data.get('posicion')
        fechaNac = data.get('fechaNac')
        edad = data.get('edad')
        nacionalidad = data.get('nacionalidad')
        sexo = data.get('sexo')

        # Validaciones básicas
        if not idEquipo or not idJugador or not nombre or not posicion or not fechaNac or not edad or not nacionalidad or not sexo:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        try:
            # Llamar a la función para insertar en la base de datos
            insertar_jugadores(idEquipo, idJugador, nombre, posicion, fechaNac, edad, nacionalidad, sexo)
            return jsonify({'mensaje': 'Registro correcto'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
#Fin Ruta register-jugadores

#Inicio ruta Fixtures

@app_routes.route('/fixtures', methods=['GET'])
def fixtures():
    id_torneo = request.args.get('id_torneo')

    if not id_torneo:
        return jsonify({'error': 'ID del torneo no proporcionado'}), 400

    if not id_torneo.isdigit():
        return jsonify({'error': 'ID del torneo debe ser un número'}), 400

    try:
        id_torneo = int(id_torneo)
        equipos = get_teams(id_torneo)  # Obtener equipos del torneo desde la base de datos

        if not equipos:
            return jsonify({'error': 'No hay equipos registrados para este torneo'}), 404

        # Generar los fixtures
        fixtures = generar_fixtures(equipos)  # Debe devolver un listado de rondas con partidos estructurados
        # Formato esperado:
        # [
        #     {
        #         "ronda": 1,
        #         "partidos": [
        #             {"local": "Equipo A", "visitante": "Equipo B", "fecha": "2024-11-26", "hora": "15:00", "ubicacion": "Estadio 1", "arbitros": "Árbitro 1"},
        #             {"local": "Equipo C", "visitante": "Equipo D", "fecha": "2024-11-27", "hora": "18:00", "ubicacion": "Estadio 2", "arbitros": "Árbitro 2"}
        #         ]
        #     },
        #     ...
        # ]

        return render_template('fixtures.html', fixtures=fixtures, id_torneo=id_torneo)
    except ValueError:
        return jsonify({'error': 'Error al procesar los datos del torneo'}), 400
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500


#Fin ruta Fixtures




