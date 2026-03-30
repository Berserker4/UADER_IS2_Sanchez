#!/usr/bin/env python3
"""
Conjetura de Collatz (mapa estándar): pares → n/2; impares → 3n+1.
Para cada n en [1, 10000] cuenta iteraciones hasta alcanzar 1 (ciclo 4-2-1).
Gráfico: abscisa = iteraciones, ordenada = n inicial.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Red de seguridad (no debería alcanzarse para n positivo con el mapa 3n+1 en rango típico).
_MAX_PASOS = 10_000_000


def siguiente_collatz(n: int) -> int:
    """Un paso: par → n/2; impar → 3n+1 (conjetura de Collatz clásica)."""
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def iteraciones_hasta_uno(n: int) -> int:
    """Pasos hasta llegar a 1 (secuencia que entra en el ciclo repetitivo 4-2-1)."""
    if n < 1:
        return 0
    pasos = 0
    while n != 1:
        n = siguiente_collatz(n)
        pasos += 1
        if pasos > _MAX_PASOS:
            raise RuntimeError(f"Sin convergencia a 1 en {_MAX_PASOS} pasos (n inicial={n})")
    return pasos


def main():
    inicio = 1
    fin = 10000
    ns = list(range(inicio, fin + 1))
    iters = [iteraciones_hasta_uno(n) for n in ns]

    plt.figure(figsize=(10, 6))
    plt.scatter(iters, ns, s=2, alpha=0.35, c="tab:blue", edgecolors="none")
    plt.xlabel("Número de iteraciones hasta alcanzar 1 (mapa par/2, impar 3n+1)")
    plt.ylabel("n inicial de la secuencia")
    plt.title("Collatz (3n+1): iteraciones vs. n de comienzo (n = 1..10000)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    salida = Path(__file__).with_name("collatz_plot.png")
    plt.savefig(salida, dpi=150)
    plt.close()
    print(f"Gráfico guardado en: {salida.resolve()}")
    print(
        f"Muestra: n=1 -> {iteraciones_hasta_uno(1)} iter; "
        f"n=27 -> {iteraciones_hasta_uno(27)} iter"
    )


if __name__ == "__main__":
    main()
