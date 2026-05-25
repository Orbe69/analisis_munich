import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('immo_data.csv')


munich = df[df['regio2'] == 'München']
munich = munich[['totalRent', 'baseRent', 'livingSpace', 'noRooms', 'regio3']]

print(munich.isnull().sum())

munich = munich[munich['livingSpace'] > 10]
munich = munich[munich['livingSpace'] < 300]
munich = munich[munich['baseRent'] > 100]
munich = munich[munich['baseRent'] < 10000]

print(f"Pisos después de limpiar: {len(munich)}")

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np

# Preparar features
munich['precio_m2'] = munich['baseRent'] / munich['livingSpace']
por_barrio = munich.groupby('regio3')['precio_m2'].mean().sort_values(ascending = False)
munich = pd.get_dummies(munich, columns=['regio3'])
barrio_cols = [col for col in munich.columns if col.startswith('regio3_')]
X = munich[['livingSpace', 'noRooms'] + barrio_cols]
y = munich['baseRent']

# Dividir en train y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Datos de entrenamiento: {len(X_train)}")
print(f"Datos de test: {len(X_test)}")

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Predecir en test
y_pred = modelo.predict(X_test)

# Evaluar
error = mean_absolute_error(y_test, y_pred)
print(f"Error medio absoluto: {error:.2f} €")


por_barrio.plot(kind = 'bar', figsize = (14, 6), color = 'steelblue')
plt.title('Precio medio por m2 por barrio en München')
plt.xlabel('Barrio')
plt.ylabel('€/m2')
plt.xticks(rotation = 45, ha = 'right')
plt.tight_layout()
plt.savefig('barrios_munich.png')
print("Gráfico guardado")

import folium

coordenadas = {
    'Altstadt': [48.1374, 11.5755],
    'Lehel': [48.1341, 11.5912],
    'Maxvorstadt': [48.1503, 11.5680],
    'Schwabing': [48.1642, 11.5836],
    'Schwabing_West': [48.1580, 11.5650],
    'Haidhausen': [48.1270, 11.6050],
    'Ludwigsvorstadt_Isarvorstadt': [48.1280, 11.5650],
    'Neuhausen': [48.1550, 11.5280],
    'Milbertshofen': [48.1850, 11.5680],
    'Untergiesing': [48.1050, 11.5680],
    'Nymphenburg': [48.1580, 11.5050],
    'Sendling': [48.1150, 11.5450],
    'Bogenhausen': [48.1450, 11.6180],
    'Pasing': [48.1480, 11.4620],
    'Hadern': [48.1050, 11.4850],
    'Lochhausen': [48.1680, 11.4180],
    'Aubing': [48.1580, 11.4350],
    'Moosach': [48.1780, 11.5180],
    'Thalkirchen': [48.0950, 11.5480],
    'Laim': [48.1380, 11.5050],
}

mapa = folium.Map(location = [48.1351, 11.5820], zoom_start = 11)

for barrio, precio in por_barrio.items():
    if barrio in coordenadas:
        folium.CircleMarker(
            location = coordenadas[barrio],
            radius = precio/3,
            popup = f"{barrio}: {precio: .2f} €/m2",
            color = 'steelblue',
            fill = True,
            fill_opacity = 0.7
        ).add_to(mapa)

mapa.save('mapa_munich.html')
print("Mapa guardado")

# Predecir precio de un piso concreto
piso = pd.DataFrame({
    'livingSpace': [60],
    'noRooms': [2]
})

for col in barrio_cols:
    piso[col] = 0

piso['regio3_Pasing'] = 1

precio_predicho = modelo.predict(piso)
print(f"Precio predicho para 80m², 3 habitaciones en Schwabing: {precio_predicho[0]:.2f} €")






