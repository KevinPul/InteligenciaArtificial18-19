import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression

# Se carga el dataset de california_housing
california = fetch_california_housing(as_frame=True)

# Se extraen los primeros 50 registros
X = california.data['MedInc'].values[:50]
Y = california.target.values[:50]

# Se preparan los datos para la grafica
X_reshaped = X.reshape(-1, 1)

# Se crea y entrena el modelo de regresion lineal
modelo = LinearRegression()
modelo.fit(X_reshaped, Y)

# Se hacen las predicciones
Y_pred = modelo.predict(X_reshaped)

# Se crea la grafica
plt.scatter(X, Y, color='blue', label='Datos reales (50 casas)')
plt.plot(X, Y_pred, color='red', label='Línea de Regresión')
plt.title('Regresión Lineal: Ingreso vs Valor de la Vivienda')
plt.xlabel('Ingreso Medio del Vecindario (MedInc)')
plt.ylabel('Valor Medio de la Casa')
plt.legend()
plt.show()