import os
from werkzeug.utils import secure_filename

#Funcion para guardar los escudos de los esquipos
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_logo(file,upload_folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder,filename)
    #os.makedirs(upload_folder,exist_ok=True)
    # file.save(file_path)
    # return file_path
    try:
        print(f"Escudo guardado en: {os.path.join('img', 'escudos', filename)}")

        file.save(file_path)
        print ("File saved successfully")
        return os.path.join('img', 'escudos', filename)
    except Exception as e:
        print(f"Error al guardar el escudo: {e}")
        return None


#Funcio para hacer los cruces
def generar_fixtures(equipos):
    num_equipos = len(equipos)

    # Si el número de equipos es impar, añadimos un "descanso"
    if num_equipos % 2 != 0:
        equipos.append({"nombre": "Descanso"})

    total_rondas = len(equipos) - 1
    partidos_por_ronda = len(equipos) // 2
    fixtures = []

    for ronda in range(total_rondas):
        partidos = []

        for i in range(partidos_por_ronda):
            equipo_local = equipos[i]
            equipo_visitante = equipos[len(equipos) - 1 - i]
            partidos.append({
                "local": equipo_local["nombre"],
                "id_local": equipo_local.get("id_equipo"),
                "visitante": equipo_visitante["nombre"],
                "id_visitante": equipo_visitante.get("id_equipo")
            })

        fixtures.append({"ronda": ronda + 1, "partidos": partidos})
        

        # Rotar los equipos (excepto el primero que permanece fijo)
        ultimo = equipos.pop()
        equipos.insert(1, ultimo)

    return fixtures

# def generar_fixtures(equipos):
#     num_equipos = len(equipos)
#     combinaciones_anteriores = set()  # Para almacenar los cruces ya realizados

#     if num_equipos % 2 != 0:
#         equipos.append({"nombre": "Descanso"})

#     total_rondas = len(equipos) - 1
#     partidos_por_ronda = len(equipos) // 2
#     fixtures = []

#     for ronda in range(total_rondas):
#         partidos = []

#         for i in range(partidos_por_ronda):
#             equipo_local = equipos[i]
#             equipo_visitante = equipos[len(equipos) - 1 - i]

#             # Generar un identificador único para el cruce
#             cruce = (equipo_local["id_equipo"], equipo_visitante["id_equipo"]) if equipo_local["id_equipo"] < equipo_visitante["id_equipo"] else (equipo_visitante["id_equipo"], equipo_local["id_equipo"])

#             # Verificar si el cruce ya ha sido realizado
#             if cruce in combinaciones_anteriores:
#                 continue  # Si el cruce ya se ha realizado, saltamos a la siguiente combinación

#             combinaciones_anteriores.add(cruce)

#             partidos.append({
#                 "local": equipo_local["nombre"],
#                 "id_local": equipo_local.get("id_equipo"),
#                 "visitante": equipo_visitante["nombre"],
#                 "id_visitante": equipo_visitante.get("id_equipo")
#             })

#         fixtures.append({"ronda": ronda + 1, "partidos": partidos})

#         ultimo = equipos.pop()
#         equipos.insert(1, ultimo)

#     return fixtures
