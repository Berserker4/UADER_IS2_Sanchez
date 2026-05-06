#!/usr/bin/python3
# * TP4 - Punto 2 : Patron Bridge                                           *
from abc import ABC, abstractmethod


class TrenLaminador(ABC):
    """Implementor: define el contrato de cualquier tren laminador."""

    @abstractmethod
    def laminar(self, espesor_pulg, ancho_m):
        """Produce una plancha; retorna la longitud (en metros) generada."""


class Tren5m(TrenLaminador):
    """Tren laminador que entrega planchas de 5 metros."""

    LARGO = 5

    def laminar(self, espesor_pulg, ancho_m):
        print(f"  [Tren5m] laminando plancha de {espesor_pulg}\" x {ancho_m}m -> {self.LARGO}m")
        return self.LARGO


class Tren10m(TrenLaminador):
    """Tren laminador que entrega planchas de 10 metros."""

    LARGO = 10

    def laminar(self, espesor_pulg, ancho_m):
        print(f"  [Tren10m] laminando plancha de {espesor_pulg}\" x {ancho_m}m -> {self.LARGO}m")
        return self.LARGO


class Lamina:
    """Abstraccion generica de una lamina; delega la produccion al tren."""

    def __init__(self, espesor_pulg, ancho_m, tren):
        self._espesor = espesor_pulg
        self._ancho = ancho_m
        self._tren = tren

    def cambiar_tren(self, tren):
        """Permite redirigir la lamina a otro tren laminador."""
        self._tren = tren

    def producir(self):
        print(f"Lamina {self._espesor}\" x {self._ancho}m  ->  {type(self._tren).__name__}")
        largo = self._tren.laminar(self._espesor, self._ancho)
        print(f"  Resultado: plancha de {largo} m\n")
        return largo


def _demo():
    lamina = Lamina(espesor_pulg=0.5, ancho_m=1.5, tren=Tren5m())
    lamina.producir()

    lamina.cambiar_tren(Tren10m())
    lamina.producir()


if __name__ == "__main__":
    _demo()
