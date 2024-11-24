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
        file.save(file_path)
        print ("File saved successfully")
        return file_path
    except Exception as e:
        print(f"Error al guardar el escudo: {e}")
        return None


# #Algoritmo para crear los fixtures
# def generar_fixtures(equipos):
#     num_equipos = len(equipos)

#     # Si el número de equipos es impar, añadimos un "descanso"
#     if num_equipos % 2 != 0:
#         equipos.append("Descanso")

#     total_rondas = len(equipos) - 1
#     partidos_por_ronda = len(equipos) // 2
#     fixtures = []

#     for ronda in range(total_rondas):
#         partidos = []

#         for i in range(partidos_por_ronda):
#             equipo_local = equipos[i]
#             equipo_visitante = equipos[len(equipos) - 1 - i]
#             partidos.append({"local": equipo_local, "visitante": equipo_visitante})

#         fixtures.append({"ronda": ronda + 1, "partidos": partidos})

#         # Rotar los equipos (excepto el primero que permanece fijo)
#         ultimo = equipos.pop()
#         equipos.insert(1, ultimo)

#     return fixtures

# # Ejemplo de uso
# equipos = ["Equipo 1", "Equipo 2", "Equipo 3", "Equipo 4"]
# calendario = generar_fixtures(equipos)

# # Imprimir el calendario generado
# for ronda in calendario:
#     print(f"Ronda {ronda['ronda']}:")
#     for partido in ronda['partidos']:
#         print(f"{partido['local']} vs {partido['visitante']}")
#     print()
