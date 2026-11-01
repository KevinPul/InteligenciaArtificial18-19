import numpy as np

# 1. Definir los datos de entrada (X) y las respuestas correctas (Y)
# Entradas: [0,0], [0,1], [1,0], [1,1]
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
# Respuestas (Compuerta AND)
Y = np.array([0, 0, 0, 1])

# 2. Inicializar parámetros
pesos = np.zeros(2)  # Dos pesos inicializados en 0 (uno para cada entrada)
sesgo = 0.0          # Valor base inicializado en 0
tasa_aprendizaje = 0.1 # Qué tan grandes serán los ajustes en cada error
epocas = 10          # Número máximo de iteraciones sobre los datos

# 3. Definir la Función de Activación (Escalón)
def funcion_escalon(suma):
    return 1 if suma > 0 else 0

# 4. Bucle de Entrenamiento
print("--- Iniciando Entrenamiento ---")
for epoca in range(epocas):
    errores = 0
    for i in range(len(X)):
        # Multiplicar entradas por pesos, sumar todo y agregar el sesgo
        suma_ponderada = np.dot(X[i], pesos) + sesgo
        
        # Pasar por la función de activación
        prediccion = funcion_escalon(suma_ponderada)
        
        # Calcular el error (Real - Predicción)
        error = Y[i] - prediccion
        
        # Si hay un error, actualizar pesos y sesgo
        if error != 0:
            pesos += tasa_aprendizaje * error * X[i]
            sesgo += tasa_aprendizaje * error
            errores += 1
            
    print(f"Época {epoca+1}: {errores} errores cometidos.")
    
    # Si pasa por todos los datos sin equivocarse, el modelo ya aprendió
    if errores == 0:
        print("¡El Perceptrón aprendió el patrón perfectamente!\n")
        break

# 5. Ejecutar y verificar resultados finales
print("--- Pruebas Finales ---")
for i in range(len(X)):
    suma_final = np.dot(X[i], pesos) + sesgo
    resultado = funcion_escalon(suma_final)
    print(f"Entrada: {X[i]} -> Predice: {resultado} (Debería ser: {Y[i]})")