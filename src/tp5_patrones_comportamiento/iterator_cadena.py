#!/usr/bin/python3
# * TP5 - Punto 2
import sys


class IteradorDirecto:

    def __init__(self, cadena):
        self._cadena = cadena
        self._pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._pos >= len(self._cadena):
            raise StopIteration
        ch = self._cadena[self._pos]
        self._pos += 1
        return ch


class IteradorReverso:

    def __init__(self, cadena):
        self._cadena = cadena
        self._pos = len(cadena) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._pos < 0:
            raise StopIteration
        ch = self._cadena[self._pos]
        self._pos -= 1
        return ch


class Cadena:

    def __init__(self, texto):
        self._texto = texto

    def directo(self):
        return IteradorDirecto(self._texto)

    def reverso(self):
        return IteradorReverso(self._texto)


def _demo(texto):
    c = Cadena(texto)
    print(f"Cadena origen : '{texto}'")

    print("Recorrido directo:")
    for ch in c.directo():
        print(f"  {ch}")

    print("Recorrido reverso:")
    for ch in c.reverso():
        print(f"  {ch}")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "Patrones"
    _demo(arg)
