import mysql.connector 
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


# Configuracion de la conexion a la base de datos
def get_connection():
    try:
        conexion = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        #database='kickoff',
        database='torneo',
        port=3306
        )
        return conexion
    
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
def insertar_usuario(nombre, correo, contrasena,rol):
    conexion = get_connection()
    cursor = conexion.cursor()
    id_usuario = None
    try:
        # Encripta la contraseña antes de guardarla
        contrasena_hash = generate_password_hash(contrasena)
        query = "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, correo, contrasena_hash))
        
        #Insertar el rol del usuario
        query_rol = "INSERT INTO roles (id_usuario, rol) VALUES (%s, %s)"
        id_usuario = cursor.lastrowid
        cursor.execute(query_rol, (id_usuario,rol))

        # Confirmar los cambios
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()
    
# Función para insertar un equipo en la base de datos
def insertar_torneo(id_usuario, nombreTorneo, tipoTorneo, formatoTorneo, numeroEquipos, fechaInicio, fechaFin):
    conexion = get_connection()
    cursor = conexion.cursor()
    id_torneo = None

    try:
        query = """
            INSERT INTO torneos (id_usuario, nombre, tipo_torneo, formato_torneo, numero_equipos, fecha_inicio, fecha_fin) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_usuario, nombreTorneo, tipoTorneo, formatoTorneo, numeroEquipos, fechaInicio, fechaFin))
        conexion.commit()

        # Obtenemos el ID del torneo recién insertado
        id_torneo = cursor.lastrowid
    finally:
        cursor.close()
        conexion.close()
    
    return id_torneo  # Devolvemos el ID del torneo creado


def save_team_to_db(team_name, logo_path, id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        # Insertar equipo
        query_equipo = "INSERT INTO equipos (nombre, escudo) VALUES (%s, %s)"
        cursor.execute(query_equipo, (team_name, logo_path))
        id_equipo = cursor.lastrowid  # Obtenemos el ID del equipo recién creado

        # Vincular equipo al torneo
        query_torneo_equipo = "INSERT INTO torneo_equipos (id_torneo, id_equipo) VALUES (%s, %s)"
        cursor.execute(query_torneo_equipo, (id_torneo, id_equipo))

        conexion.commit()
    finally:
        cursor.close()
        conexion.close()
    

#Obtener el tipo de usuario

def get_user_role(id_usuario):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = "SELECT r.rol FROM roles r JOIN usuarios u ON r.id_usuario = u.id_usuario WHERE u.id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()
    

#Obtener Torneos por Usuario
def get_tournaments(id_usuario):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = """
            SELECT t.id_torneo, t.nombre, t.tipo_torneo, t.formato_torneo, 
                   t.numero_equipos, t.fecha_inicio, t.fecha_fin 
            FROM torneos t 
            WHERE t.id_usuario = %s
        """
        cursor.execute(query, (id_usuario,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()



#Obtener los equipos
def get_teams(id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = """
            SELECT e.id_equipo, e.nombre, e.escudo 
            FROM equipos e 
            JOIN torneo_equipos t_e ON e.id_equipo = t_e.id_equipo 
            WHERE t_e.id_torneo = %s
        """
        cursor.execute(query, (id_torneo,))
        equipos = cursor.fetchall()
        
        # Reemplazar barras invertidas en la ruta de la imagen
        for equipo in equipos:
            equipo['escudo'] = equipo['escudo'].replace("\\", "/")
        
        return equipos
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
    
    
#Obtener el numero de equipos
def get_numero_equipos(id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = "SELECT numero_equipos FROM torneos WHERE id_torneo = %s"
        cursor.execute(query,(id_torneo,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()
        
        
#Obtener los jugadores
def get_jugadores(id_equipo):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = "SELECT id_jugador, nombre, posicion, fecha_nacimiento, edad, nacionalidad, sexo FROM jugadores WHERE id_equipo = %s"
        cursor.execute(query,(id_equipo,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
        
#Funcion guardar partidos

def save_match(id_torneo, id_equipo_local, id_equipo_visitante, fecha, hora ):
    conexion = get_connection()
    cursor = conexion.cursor()

    # Crear la consulta SQL para insertar los datos
    query = """
        INSERT INTO partidos (id_torneo, id_equipo_local, id_equipo_visitante, fecha, hora)
        VALUES (%s, %s, %s, %s, %s )
    """

    # Ejecutar la consulta con los valores proporcionados
    cursor.execute(query, (id_torneo, id_equipo_local, id_equipo_visitante,  fecha, hora ))

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()
