Proyecto de Energías Renovables y Limpias – Flask

Aplicación web en Python + Flask que analiza y visualiza datos globales sobre energías renovables.
El sistema procesa archivos CSV, genera múltiples gráficos interactivos y calcula el porcentaje de consumo cubierto por energías renovables a partir de los datos cargados.

URL RENDER = https://proyecto-energiaslimpias.onrender.com/

Este proyecto permite:

Cargar datasets relacionados con energías renovables.

Mostrar gráficos de barras, pastel, líneas y áreas.

Comparar fuentes de energía como:

Solar

Eólica

Hidroeléctrica

Geotérmica

Biocombustibles

Calcular qué porcentaje del consumo total podría abastecerse con energías limpias.

Mostrar tablas de información cargadas desde archivos CSV.

Características Principales

✔ Procesamiento automático de datos desde múltiples CSV
✔ Gráficas generadas con Matplotlib
✔ Uso de Flask-Caching para mejor rendimiento
✔ Cálculo dinámico del porcentaje renovable
✔ Interfaz HTML basada en Jinja2
✔ Servidor de producción con Waitress
✔ Preparado para deploy (Render, etc.)


Gráficos Incluidos
📌 1. Gráfico de Barras

Comparación de la producción total entre fuentes renovables.

📌 2. Gráfico de Pastel

Porcentaje de participación de solar, eólica e hidroeléctrica en el último año disponible.

📌 3. Gráfico de Líneas

Comparación de capacidad instalada entre energía solar y eólica a lo largo del tiempo.

📌 4. Gráfico de Área

Comparación entre consumo de energía renovable y energía convencional global.

Cálculo del Porcentaje Renovable

El usuario ingresa un consumo total y la app estima:

porcentaje = (consumo / producción_renovable_total) * 100

🛠 Tecnologías
Tecnología	Uso
Python	Lenguaje principal
Flask	Backend web
Matplotlib	Gráficos
Pandas	Carga y manipulación de datos
Flask-Caching	Caché
Waitress	Servidor producción
HTML + Jinja	Interfaz