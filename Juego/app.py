from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = 'databaseTorneo.db'

# Función para conectar a la base de datos
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(DATABASE)
    return g.sqlite_db

# Cerrar la base de datos cuando termine la aplicación
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Ruta para mostrar el formulario
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

# Ruta para agregar un usuario a la base de datos
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    # Capturar los datos del formulario
    nombre = request.form['nombre']
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    
    # Conectar a la base de datos
    db = get_db()
    cursor = db.cursor()

    try:
        # Insertar los datos en la tabla 'usuarios'
        cursor.execute("INSERT INTO usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)", 
                       (nombre, correo, contrasena))
        db.commit()  # Confirmar los cambios en la base de datos
        
        return redirect(url_for('formulario'))  # Redirigir a la página del formulario

    except Exception as e:
        return f"Error al agregar usuario: {e}"  # Mostrar el error en caso de fallo

# Ruta para verificar los usuarios en la base de datos
@app.route('/usuarios')
def ver_usuarios():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios;")
    usuarios = cursor.fetchall()
    return f"Usuarios registrados: {usuarios}"

if __name__ == '__main__':
    app.run(debug=True)
