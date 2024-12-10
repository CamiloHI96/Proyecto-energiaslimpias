from flask import Flask, render_template, request
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import os
from waitress import serve

app = Flask(__name__) 
app.secret_key = 'camilo123'

def cargar_datos_renovables(ruta_csv):
    datos=[]
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                datos.append({
                    'entity': fila['Entity'],
                    'code': fila['Code'],
                    'year': int(fila['Year']),
                    'renewables': float(fila['Renewables (% equivalent primary energy)'])
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

    #---------------------------------TORTA---------------------------------------------------------------------------------
    df_renewables = pd.read_csv('static/archivo/04 share-electricity-renewables.csv')
    df_wind = pd.read_csv('static/archivo/11 share-electricity-wind.csv')
    df_solar = pd.read_csv('static/archivo/15 share-electricity-solar.csv')
    df_hydro = pd.read_csv('static/archivo/07 share-electricity-hydro.csv')

    year = df_renewables['Year'].max()
    renewables_data = df_renewables[df_renewables['Year'] == year]
    wind_data = df_wind[df_wind['Year'] == year]
    solar_data = df_solar[df_solar['Year'] == year]
    hydro_data = df_hydro[df_hydro['Year'] == year]

    df = pd.merge(renewables_data[['Entity', 'Renewables (% electricity)']], wind_data[['Entity', 'Wind (% electricity)']], on='Entity')
    df = pd.merge(df, solar_data[['Entity', 'Solar (% electricity)']], on='Entity')
    df = pd.merge(df, hydro_data[['Entity', 'Hydro (% electricity)']], on='Entity')

    wind_percentage = df['Wind (% electricity)'].values[0]
    solar_percentage = df['Solar (% electricity)'].values[0]
    hydro_percentage = df['Hydro (% electricity)'].values[0]
    
    total_renewables = wind_percentage+solar_percentage+hydro_percentage

    data = {
        'Energia Renovable' : ['Eolica', 'Solar', 'Hidroelectrica'],
        'Participacion' : [wind_percentage, solar_percentage, hydro_percentage]
    }
    df_graph = pd.DataFrame(data)
    fig, ax = plt.subplots()
    ax.set_title('Participacion de Energias Renovables', fontsize=14)
    ax.pie(df_graph['Participacion'], labels=df_graph['Energia Renovable'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url2 = base64.b64encode(img.getvalue()).decode('utf-8')
    #-----------------------------------------------------------------------------------------------------------------------
    
    if request.method == 'POST':
        try:
            consumo_total = float(request.form['consumo_total'])
            if consumo_total <= 0:
                error = "El consumo total debe ser un valor positivo."
            else:
                produccion_total_renovable = sum(energia['renewables'] for energia in datos_renovables)
                if produccion_total_renovable >= consumo_total:
                    porcentaje_renovable = (consumo_total/produccion_total_renovable)*100
                else:
                    porcentaje_renovable = 100
            
        except ValueError:
            error ="Por Favor ingrese un valor válido para el consumo total."
    
    return render_template('index.html',porcentaje_renovable = porcentaje_renovable,error=error,graph_url = graph_url, graph_url2 = graph_url2)

# Comprobamos si estamos en Render o en entorno local
if __name__ == '__main__':
    # Verificar si la variable de entorno RENDER_ENV está definida
    if os.getenv('RENDER_ENV') == 'true':
        # Usar el servidor de Waitress en Render
        print("Running on Render")
        serve(app, host='0.0.0.0', port=5000)
    else:
        # Usar el servidor de Flask en entorno local
        print("Running locally")
        app.run(debug=True, host='0.0.0.0', port=5000)
