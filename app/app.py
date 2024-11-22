from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/dashboard')
def inicio():
    return render_template('dashboard.html')

@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')

@app.route('/addTeams')
def addTeams():
    return render_template('equipos.html')

if __name__ == '__main__':
    app.run(debug=True)