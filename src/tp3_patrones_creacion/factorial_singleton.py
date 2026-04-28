#!/usr/bin/python3
# *-------------------------------------------------------------------------*
# * TP3 - Punto 1                                                           *
# *-------------------------------------------------------------------------*
import sys


class FactorialSingleton:
    """Singleton: una unica instancia compartida para calcular factoriales."""

    _instancia = None

    def __new__(cls):
        # Se reutiliza la instancia si ya fue creada (patron Singleton).
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._invocaciones = 0
        return cls._instancia

    def calcular(self, num):
        """Devuelve num! ; los negativos no tienen factorial definido."""
        if num < 0:
            raise ValueError("Factorial de un numero negativo no existe")
        self._invocaciones += 1
        fact = 1
        for k in range(2, num + 1):
            fact *= k
        return fact

    @property
    def invocaciones(self):
        """Cantidad de veces que se llamo a calcular() en la instancia unica."""
        return self._invocaciones


class ClienteA:
    """Cliente de ejemplo que pide factoriales al singleton."""

    def __init__(self):
        self.fact = FactorialSingleton()

    def pedir(self, n):
        return self.fact.calcular(n)


class ClienteB:
    """Otro cliente; debe compartir la instancia con ClienteA."""

    def __init__(self):
        self.fact = FactorialSingleton()

    def pedir(self, n):
        return self.fact.calcular(n)


def _demo(n):
    a = ClienteA()
    b = ClienteB()
    print(f"ClienteA: {n}! = {a.pedir(n)}")
    print(f"ClienteB: {n}! = {b.pedir(n)}")
    # La verificacion clave del Singleton: misma identidad de objeto.
    print(f"Misma instancia compartida? {a.fact is b.fact}")
    print(f"Total de invocaciones registradas: {a.fact.invocaciones}")


if __name__ == "__main__":
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    _demo(arg)
