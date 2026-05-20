#!/usr/bin/python3
# * TP5 - Punto 1
from abc import ABC, abstractmethod


class Handler(ABC):

    def __init__(self):
        self._siguiente = None

    def encadenar(self, siguiente):
        self._siguiente = siguiente
        return siguiente

    def manejar(self, numero):
        if self._procesa(numero):
            return
        if self._siguiente is not None:
            self._siguiente.manejar(numero)
            return
        print(f"{numero:>3}: no consumido")

    @abstractmethod
    def _procesa(self, numero):
        ...


class HandlerPrimos(Handler):

    def _es_primo(self, n):
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        d = 3
        while d * d <= n:
            if n % d == 0:
                return False
            d += 2
        return True

    def _procesa(self, numero):
        if self._es_primo(numero):
            print(f"{numero:>3}: consumido por HandlerPrimos")
            return True
        return False


class HandlerPares(Handler):

    def _procesa(self, numero):
        if numero % 2 == 0:
            print(f"{numero:>3}: consumido por HandlerPares")
            return True
        return False


def _demo():
    cadena = HandlerPrimos()
    cadena.encadenar(HandlerPares())

    for n in range(1, 101):
        cadena.manejar(n)


if __name__ == "__main__":
    _demo()
