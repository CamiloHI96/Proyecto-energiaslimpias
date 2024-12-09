from flask import Flask, render_template, request, session
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import os

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
<<<<<<< HEAD
                    'renewables': float(fila['Renewables (% equivalent primary energy)'])
=======
                    'renewables': float(fila['Renewables (% equivalent primary energy)'])  # Nombre ajustado
>>>>>>> 0b5f456b41434aa6d76018f89c3533603c769ada
                })
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    return datos

RUTA_CSV = 'static/archivo/data.csv'
datos_renovables = cargar_datos_renovables(RUTA_CSV)

DATA_DIR ="static/archivo"
FILES = {
    "Wind": ("08 wind-generation.csv","Electricity from wind (TWh)"),
    "Solar": ("12 solar-energy-consumption.csv","Electricity from solar (TWh)"),
    "Hidropower": ("05 hydropower-consumption.csv","Electricity from hydro (TWh)"),
    "Biofuels": ("16 biofuel-production.csv","Biofuels Production - TWh - Total"),
    "Geothermal": ("17 installed-geothermal-capacity.csv","Geothermal Capacity")
}

def load_data():
    data={}
    for key,(file_name, column) in FILES.items():
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            total_production = df[column].sum()
            data[key] = total_production
    return data

@app.route('/', methods=['GET', 'POST'])

def index():
    porcentaje_renovable = None
    error = None
<<<<<<< HEAD
    
    data = load_data()
    plt.subplots(figsize=(3,2))
    df = pd.DataFrame(list(data.items()), columns=['Fuente', 'Producción (TWh)'])
    
    fig, ax= plt.subplots(figsize=(5,4))
    ax.bar(df['Fuente'], df['Producción (TWh)'], color=['blue', 'orange', 'green', 'red', 'purple'])
    
    ax.set_title('Producción de Energía Renovable por Fuente', fontsize= 12)
    ax.set_xlabel('Fuente de Energía', fontsize= 12)
    ax.set_ylabel('Producción (TWh)', fontsize= 12)
    
    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url=base64.b64encode(img.getvalue()).decode('utf-8')
    
=======

>>>>>>> 0b5f456b41434aa6d76018f89c3533603c769ada
    if request.method == 'POST':
        try:
            consumo_total = float(request.form['consumo_total'])
            if consumo_total <= 0:
                error = "El consumo total debe ser un valor positivo."
            else:
<<<<<<< HEAD
                produccion_total_renovable = sum(energia['renewables'] for energia in datos_renovables)
                if produccion_total_renovable >= consumo_total:
                    porcentaje_renovable = (consumo_total/produccion_total_renovable)*100
                else:
                    porcentaje_renovable = 100
            
        except ValueError:
            error ="Por Favor ingrese un valor válido para el consumo total."
    
    return render_template('index.html',porcentaje_renovable = porcentaje_renovable,error=error,graph_url = graph_url)
=======
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
>>>>>>> 0b5f456b41434aa6d76018f89c3533603c769ada

if __name__ == '__main__':
    #server para subir a Render
    #serve(app, host='0.0.0.0', port=5000)
    #trabajar en entorno local
    app.run(debug=True, host='0.0.0.0', port=5000)