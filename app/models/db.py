import mysql.connector 
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


# Configuracion de la conexion a la base de datos
def get_connection():
    try:
        conecxion = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='torneo',
        port=3306
        )
        return conecxion
    
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
    
    
    
def verificar_usuario(correo,contrasena):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)  # Devuelve resultados como diccionario
    try:
        query = "SELECT id_usuario, contrasena FROM usuarios WHERE correo = %s"
        cursor.execute(query, (correo,))
        usuario = cursor.fetchone()  # Obtiene un solo resultado
        
        if usuario: 
            if check_password_hash(usuario['contrasena'],contrasena):
                return usuario  # Devuelve el usuario si la contraseña es valida
            else:
                print("Contraseña incorrecta")  # Mensaje de depuración
        else:
            print("Correo no encontrado")
            
        return None
    finally:
        cursor.close()
        conexion.close()
        
# Verifica si un correo ya está registrado
def obtener_usuario_por_correo(correo):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = "SELECT * FROM usuarios WHERE correo = %s"
        cursor.execute(query, (correo,))
        return cursor.fetchone()  # Retorna el usuario si existe, None si no
    finally:
        cursor.close()
        conexion.close()

# Inserta un nuevo usuario
def insertar_usuario(nombre, correo, contrasena):
    conexion = get_connection()
    cursor = conexion.cursor()
    try:
        # Encripta la contraseña antes de guardarla
        contrasena_hash = generate_password_hash(contrasena)
        query = "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, correo, contrasena_hash))
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()
    
# Función para insertar un equipo en la base de datos
def insertar_torneo(id_usuario,nombreTorneo,tipoTorneo,formatoTorneo,numeroEquipos,fechaInicio,fechaFin):
    conecxion = get_connection()
    cursor = conecxion.cursor()

    try:
        query = "INSERT INTO torneos (id_usuario,nombre,tipo_torneo,formato_torneo,numero_equipos,fecha_inicio,fecha_fin) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (id_usuario,nombreTorneo,tipoTorneo,formatoTorneo,numeroEquipos,fechaInicio,fechaFin))
        conecxion.commit()
    finally:
        cursor.close()
        conecxion.close()

def save_team_to_db(team_name,logo_path):
    conexion = get_connection()
    cursor = conexion.cursor()
   
    try:
        query = "INSERT INTO equipos (nombre, escudo) VALUES (%s, %s)"
        cursor.execute(query, (team_name, logo_path))
    finally:
        conexion.commit()
        conexion.close()     

#Obtener los equipos
def get_teams():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = "SELECT * FROM equipos"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
        
#Registrar los jugadores en los equipos
def insertar_jugadores(idEquipo,idJugador,nombre, posicion, fechaNac, edad,         nacionalidad, sexo):
    conexion = get_connection()
    cursor = conexion.cursor()
    try:
        query = "INSERT INTO jugadores (id_jugador,id_equipo,nombre,posicion,fecha_nacimiento,edad,nacionalidad,sexo) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)"
        cursor.execute(query, (idJugador,idEquipo,nombre, posicion, fechaNac, edad,nacionalidad, sexo))
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()
    