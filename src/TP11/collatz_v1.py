"""Conjetura de Collatz: cuenta las iteraciones necesarias para llegar a 1."""

import sys

MAX_VALIDO = 1999


def collatz(num: int) -> int:
    """Devuelve la cantidad de iteraciones de Collatz necesarias para llegar a 1.

    Args:
        num: entero positivo de partida, entre 1 y MAX_VALIDO.

    Raises:
        ValueError: si num no es un entero entre 1 y MAX_VALIDO.
    """
    if isinstance(num, bool) or not isinstance(num, int):
        raise ValueError("el número debe ser un entero")
    if num < 1 or num > MAX_VALIDO:
        raise ValueError(f"el número debe estar entre 1 y {MAX_VALIDO}")
    iteraciones = 0
    while num != 1:
        if num % 2 == 0:
            num = num // 2
        else:
            num = 3 * num + 1
        iteraciones += 1
    return iteraciones


def main() -> int:
    """Pide un número por teclado e imprime sus iteraciones de Collatz."""
    try:
        texto = input("Ingrese un entero positivo (1-1999): ")
        partida = int(texto.strip())
        iteraciones = collatz(partida)
    except (ValueError, EOFError) as exc:
        print(f"Error: entrada inválida ({exc})", file=sys.stderr)
        return 1
    print(f"El número de iteraciones para {partida} es {iteraciones}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
