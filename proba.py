import random
import matplotlib.pyplot as plt

# Definir una función de suavizado
def smooth(data, window_size):
    smoothed = []
    for i in range(len(data)):
        start = max(0, i - window_size)
        end = min(len(data), i + window_size)
        smoothed.append(sum(data[start:end]) / (end - start))
    return smoothed

# Generar una serie de números aleatorios
x_random = [random.random() for _ in range(50)]

# Aplicar un filtro de suavizado
x = smooth(x_random, 30)

# Graficar la variable x
plt.figure(figsize=(10, 6))
plt.plot(x)
plt.title('Variable x que cambia suavemente y de manera aleatoria')
plt.xlabel('Tiempo (t)')
plt.ylabel('x(t)')
plt.grid(True)
plt.show()
