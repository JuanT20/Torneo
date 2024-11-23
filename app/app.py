from flask import Flask
from routes.main import app_routes  # Importa las rutas


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'





    # Registro de rutas
    app.register_blueprint(app_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
