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


#Eliminar torneo

def delete_tournament(id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        # Eliminar partidos del torneo
        query_torneo_partido = "DELETE FROM partidos WHERE id_torneo = %s"
        cursor.execute(query_torneo_partido, (id_torneo,))
        conexion.commit()
        
        #Eliminar la ubicaciones del torneo
        query_torneo_ubicacion = "DELETE FROM ubicaciones WHERE id_torneo = %s"
        cursor.execute(query_torneo_ubicacion, (id_torneo,))
        conexion.commit()
        
        #Eliminar los arbitros del torneo
        query_torneo_arbitro = "DELETE FROM arbitros WHERE id_torneo = %s"
        cursor.execute(query_torneo_arbitro, (id_torneo,))
        conexion.commit()
          
        # Eliminar equipos del torneo
        query_torneo_equipo = "DELETE FROM torneo_equipos WHERE id_torneo = %s"
        cursor.execute(query_torneo_equipo, (id_torneo,))
        conexion.commit()
        
        # Eliminar torneo
        query_torneo = "DELETE FROM torneos WHERE id_torneo = %s"
        cursor.execute(query_torneo, (id_torneo,))
        conexion.commit()
        
    finally:
        cursor.close()
        conexion.close()
        


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
            ORDER BY e.nombre ASC
        """
        cursor.execute(query, (id_torneo,))
        equipos = cursor.fetchall()
        
        # # Reemplazar barras invertidas en la ruta de la imagen
        # for equipo in equipos:
        #     equipo['escudo'] = equipo['escudo'].replace("\\", "/")
        
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
def save_matches(id_torneo, partidos):
    conexion = get_connection()
    cursor = conexion.cursor()

    # consulta SQL para insertar los datos
    query = """
        INSERT INTO partidos (id_torneo, id_equipo_local, id_equipo_visitante, id_arbitro, fecha, hora, id_ubicacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # lista de valores a insertar
    values = [
        (
            id_torneo,
            partido['idLocal'],
            partido['idVisitante'],
            partido['arbitro'],
            partido['fecha'],
            partido['hora'],
            partido['ubicacion']
        )
        for partido in partidos
    ]

    try:
        # Ejecutar múltiples inserciones
        cursor.executemany(query, values)

        # Confirmar los cambios
        conexion.commit()
    except Exception as e:
        # En caso de error, deshacer los cambios
        conexion.rollback()
        print(f"Error al guardar partidos: {e}")
        raise
    finally:
        # Cerrar la conexión
        cursor.close()
        conexion.close()

    
    
#Guardar las ubicaciones
def save_ubicacion(id_torneo,lugar,cancha):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    # consulta SQL para insertar los datos
    query = """
        INSERT INTO ubicaciones (lugar,cancha,id_torneo)
        VALUES (%s, %s, %s)
    """
    # Ejecutar la consulta con los valores proporcionados
    cursor.execute(query, (lugar,cancha,id_torneo,))
    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()



#Guardar los arbitros
def save_arbitro(id_arbitro,nombre,experiencia,id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    # consulta SQL para insertar los datos
    query = """
        INSERT INTO arbitros (id_arbitro,nombre,experiencia,id_torneo)
        VALUES (%s, %s, %s, %s)
    """
    # Ejecutar la consulta con los valores proporcionados
    cursor.execute(query, (id_arbitro,nombre,experiencia,id_torneo))
    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()


    
#Obtener las ubicaciones
def get_ubicaciones(id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = "SELECT id_ubicacion, lugar, cancha FROM ubicaciones WHERE id_torneo = %s"
        cursor.execute(query,(id_torneo,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

#Obtener los arbitros
def get_arbitros(id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = "SELECT id_arbitro, nombre, experiencia FROM arbitros WHERE id_torneo = %s"
        cursor.execute(query,(id_torneo,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
        
#Obtener los partidos
def get_partidos(id_torneo):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = """ SELECT 
                        p.id_partido, 
                        p.id_torneo, 
                        el.nombre AS equipo_local, 
                        ev.nombre AS equipo_visitante, 
                        p.fecha,
                        p.hora,
                        a.nombre AS arbitro, 
                        u.lugar, 
                        u.cancha 
                    FROM partidos p
                    JOIN arbitros a ON p.id_arbitro = a.id_arbitro
                    JOIN ubicaciones u ON p.id_ubicacion = u.id_ubicacion
                    JOIN equipos el ON p.id_equipo_local = el.id_equipo
                    JOIN equipos ev ON p.id_equipo_visitante = ev.id_equipo
                    WHERE p.id_torneo = %s

                """
        cursor.execute(query,(id_torneo,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
        
#Eliminar equipo si hay mas de 6 equipos en el torneo sino no.
def delete_team(self, id_torneo, id_equipo):
    numero_equipos = self.get_numero_equipos(id_torneo)['numero_equipos']
    if numero_equipos > 6:
        conexion = get_connection()
        cursor = conexion.cursor()
        try:
            query = "DELETE FROM equipos WHERE id_equipo = %s"
            cursor.execute(query, (id_equipo,))
            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error al eliminar el equipo: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
                

