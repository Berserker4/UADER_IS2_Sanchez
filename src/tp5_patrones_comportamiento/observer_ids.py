#!/usr/bin/python3
# * TP5 - Punto 3
import random
import string


class Emisor:

    def __init__(self):
        self._observadores = []

    def suscribir(self, observador):
        self._observadores.append(observador)

    def desuscribir(self, observador):
        self._observadores.remove(observador)

    def emitir(self, identificador):
        print(f"\n[Emisor] -> {identificador}")
        for obs in self._observadores:
            obs.recibir(identificador)


class Observador:

    def __init__(self, identificador):
        self.id = identificador

    def recibir(self, identificador):
        if identificador == self.id:
            print(f"  Observador {self.id}: coincidencia! mi ID fue emitido.")


def _id_aleatorio():
    return "".join(random.choices(string.ascii_uppercase, k=4))


def _demo():
    random.seed(42)

    obs1 = Observador("ABCD")
    obs2 = Observador("XYZW")
    obs3 = Observador("UADR")
    obs4 = Observador("IS22")

    emisor = Emisor()
    for o in (obs1, obs2, obs3, obs4):
        emisor.suscribir(o)

    ids_objetivo = [obs1.id, obs2.id, obs3.id, obs4.id]
    ids_aleatorios = [_id_aleatorio() for _ in range(4)]
    secuencia = ids_objetivo + ids_aleatorios
    random.shuffle(secuencia)

    for identificador in secuencia:
        emisor.emitir(identificador)


if __name__ == "__main__":
    _demo()
