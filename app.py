from flask import Flask, render_template, request, session
import csv
from waitress import serve

app = Flask(__name__)
app.secret_key = 'camilo123'

def limpiar_encabezados(encabezados):
    return [encabezado.strip() for encabezado in encabezados]

def cargar_datos_renovables(ruta_csv):
    datos = []
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            print(f"Encabezados del archivo CSV: {lector.fieldnames}")  # Imprime los encabezados
            for fila in lector:
                datos.append({
                    'entity': fila['Entity'],
                    'code': fila['Code'],
                    'year': int(fila['Year']),
                    'renewables': float(fila['Renewables (% equivalent primary energy)'])  # Nombre ajustado
                })
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    return datos

RUTA_CSV = 'static/archivo/data.csv'
datos_renovables = cargar_datos_renovables(RUTA_CSV)

@app.route('/', methods=['GET', 'POST'])
def index():
    porcentaje_renovable = None
    error = None

    if request.method == 'POST':
        try:
            consumo_total = float(request.form['consumo_total'])
            if consumo_total <= 0:
                error = 'El consumo total debe ser un valor positivo'
            else:
                producto_total_renovable = sum(energia['renewables'] for energia in datos_renovables)
                if producto_total_renovable >= consumo_total:
                    porcentaje_renovable = (consumo_total / producto_total_renovable) * 100
                else:
                    porcentaje_renovable = 100

            session['porcentaje_renovable'] = porcentaje_renovable
            session['error'] = error
        except ValueError:
            error = 'Por favor ingrese un valor valido para el consumo total'

    porcentaje_renovable = session.get('porcentaje_renovable', None)
    error = session.get('error', None)

    return render_template('index.html', porcentaje_renovable=porcentaje_renovable, error=error)

if __name__ == '__main__':
    #server para subir a Render
    #serve(app, host='0.0.0.0', port=5000)
    #trabajar en entorno local
    app.run(debug=True, host='0.0.0.0', port=5000)