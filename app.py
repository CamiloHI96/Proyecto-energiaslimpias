from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)
app.secret_key = 'camilo123'

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta secundaria
@app.route('/index.html')
def inicio():
    return render_template('index.html')

if __name__ == '__main__':
    #server para subir a Render
    serve(app, host='0.0.0.0', port=5000)
    #trabajar en entorno local
    #app.run(debug=True, host='0.0.0.0', port=5000)