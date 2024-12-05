from flask import Flask, render_template

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
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)