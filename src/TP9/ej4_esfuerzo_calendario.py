# TP9 - Ejercicio 4
# E = 8 * S^0.95
# td = 2.4 * E^0.33

import numpy as np
import matplotlib.pyplot as plt

def esfuerzo(S):
    return 8 * (S ** 0.95)

def tiempo_calendario(E):
    return 2.4 * (E ** 0.33)

S_ej = 1000
E_ej = esfuerzo(S_ej)
td_ej = tiempo_calendario(E_ej)
print(f"Para S={S_ej}: E={E_ej:.2f}, td={td_ej:.2f}")

# grafico E vs S [0,10000]
S = np.linspace(0, 10000, 500)
E = esfuerzo(S)

plt.figure(figsize=(8, 5))
plt.plot(S, E, color="#1f4e79", linewidth=2)
plt.title("Esfuerzo E en funcion del tamano S")
plt.xlabel("Tamano del proyecto S")
plt.ylabel("Esfuerzo E")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("ej4_esfuerzo_vs_tamano.png", dpi=150)
plt.close()

# grafico td vs E [1,500]
E_vals = np.linspace(1, 500, 500)
td = tiempo_calendario(E_vals)

plt.figure(figsize=(8, 5))
plt.plot(E_vals, td, color="#8b1e1e", linewidth=2)
plt.title("Tiempo calendario td en funcion del esfuerzo E")
plt.xlabel("Esfuerzo E")
plt.ylabel("Tiempo calendario td")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("ej4_td_vs_esfuerzo.png", dpi=150)
plt.close()

print("Graficos guardados")
