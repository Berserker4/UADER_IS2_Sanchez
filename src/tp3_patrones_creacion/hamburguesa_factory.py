#!/usr/bin/python3
# *-------------------------------------------------------------------------*
# * TP3 - Punto 3                                                           *
# *-------------------------------------------------------------------------*
import sys
from abc import ABC, abstractmethod


class Hamburguesa(ABC):
    """Producto abstracto: define la interfaz comun de toda hamburguesa."""

    nombre = "Hamburguesa"

    @abstractmethod
    def metodo_entrega(self):
        """Cada subclase indica como llega al cliente."""
        raise NotImplementedError

    def servir(self):
        print(f"{self.nombre} -> entrega: {self.metodo_entrega()}")


class HamburguesaMostrador(Hamburguesa):
    nombre = "Hamburguesa de mostrador"

    def metodo_entrega(self):
        return "se entrega en mostrador (consumo en local)"


class HamburguesaRetiro(Hamburguesa):
    nombre = "Hamburguesa para retirar"

    def metodo_entrega(self):
        return "el cliente la retira por el local (take away)"


class HamburguesaDelivery(Hamburguesa):
    nombre = "Hamburguesa con delivery"

    def metodo_entrega(self):
        return "se envia por delivery a domicilio"


class FabricaHamburguesa:
    """Factory Method: instancia el producto adecuado segun el tipo pedido."""

    _registro = {
        "mostrador": HamburguesaMostrador,
        "retiro": HamburguesaRetiro,
        "delivery": HamburguesaDelivery,
    }

    @classmethod
    def crear(cls, tipo):
        clave = tipo.strip().lower()
        if clave not in cls._registro:
            opciones = ", ".join(cls._registro)
            raise ValueError(f"Tipo de entrega invalido: {tipo!r}. Opciones: {opciones}")
        return cls._registro[clave]()


def _demo(tipo=None):
    if tipo is None:
        for t in ("mostrador", "retiro", "delivery"):
            FabricaHamburguesa.crear(t).servir()
    else:
        FabricaHamburguesa.crear(tipo).servir()


if __name__ == "__main__":
    _demo(sys.argv[1] if len(sys.argv) > 1 else None)
