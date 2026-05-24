import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('immo_data.csv')

munich = df[df['regio2'] == 'München']
munich = munich[['totalRent', 'baseRent', 'livingSpace', 'noRooms', 'regio3']]

munich['precio_m2'] = munich['baseRent'] / munich['livingSpace']
por_barrio = munich.groupby('regio3')['precio_m2'].mean().sort_values(ascending = False)

por_barrio.plot(kind = 'bar', figsize = (14, 6), color = 'steelblue')
plt.title('Precio medio por m2 por barrio en München')
plt.xlabel('Barrio')
plt.ylabel('€/m2')
plt.xticks(rotation = 45, ha = 'right')
plt.tight_layout()
plt.savefig('barrios_munich.png')
print("Gráfico guardado")





