#!/usr/bin/python3
# * TP4 - Punto 4 : Patron Decorator                                        *
import sys
from abc import ABC, abstractmethod


class Componente(ABC):
    """Interfaz comun: cualquier elemento decorable expone valor()."""

    @abstractmethod
    def valor(self):
        ...

    def mostrar(self):
        print(f"  -> {self.valor()}")


class Numero(Componente):
    """Componente concreto: simplemente envuelve un numero."""

    def __init__(self, n):
        self._n = n

    def valor(self):
        return self._n


class OperacionDecorator(Componente):
    """Decorator abstracto: mantiene la referencia al componente envuelto."""

    def __init__(self, componente):
        self._componente = componente

    def valor(self):
        return self._componente.valor()


class Sumar2(OperacionDecorator):
    def valor(self):
        return self._componente.valor() + 2


class Multiplicar2(OperacionDecorator):
    def valor(self):
        return self._componente.valor() * 2


class Dividir3(OperacionDecorator):
    def valor(self):
        return self._componente.valor() / 3


def _demo(n):
    print(f"Numero base: {n}")

    base = Numero(n)
    print("Sin decoradores:")
    base.mostrar()

    print("Con +2:")
    Sumar2(Numero(n)).mostrar()

    print("Con +2 y luego *2:")
    Multiplicar2(Sumar2(Numero(n))).mostrar()

    print("Con +2, *2 y luego /3 (decorators anidados):")
    Dividir3(Multiplicar2(Sumar2(Numero(n)))).mostrar()


if __name__ == "__main__":
    valor = float(sys.argv[1]) if len(sys.argv) > 1 else 5
    _demo(valor)
