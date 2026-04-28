#!/usr/bin/python3
# *-------------------------------------------------------------------------*
# * TP3 - Punto 5                                                           *
# *-------------------------------------------------------------------------*
from abc import ABC, abstractmethod


class Avion:
    """Producto compuesto: se arma incrementalmente por el Builder."""

    def __init__(self):
        self.body = None
        self.turbinas = []
        self.alas = []
        self.tren_aterrizaje = None

    def __str__(self):
        partes = [
            f"body={self.body}",
            f"turbinas={self.turbinas}",
            f"alas={self.alas}",
            f"tren={self.tren_aterrizaje}",
        ]
        return "Avion(" + ", ".join(partes) + ")"


class AvionBuilder(ABC):
    """Builder abstracto: define los pasos de construccion de un avion."""

    def __init__(self):
        self.avion = Avion()

    def reset(self):
        self.avion = Avion()
        return self

    @abstractmethod
    def agregar_body(self):
        ...

    @abstractmethod
    def agregar_turbinas(self):
        ...

    @abstractmethod
    def agregar_alas(self):
        ...

    @abstractmethod
    def agregar_tren_aterrizaje(self):
        ...

    def obtener(self):
        producto = self.avion
        self.reset()
        return producto


class AvionComercialBuilder(AvionBuilder):
    """Builder concreto: arma un avion comercial estandar."""

    def agregar_body(self):
        self.avion.body = "Fuselaje comercial"
        return self

    def agregar_turbinas(self):
        self.avion.turbinas = ["Turbina turbofan #1", "Turbina turbofan #2"]
        return self

    def agregar_alas(self):
        self.avion.alas = ["Ala izquierda", "Ala derecha"]
        return self

    def agregar_tren_aterrizaje(self):
        self.avion.tren_aterrizaje = "Tren triciclo retractil"
        return self


class Director:
    """Encapsula el orden de construccion y oculta los pasos al cliente."""

    def __init__(self, builder):
        self.builder = builder

    def construir(self):
        return (
            self.builder.reset()
            .agregar_body()
            .agregar_turbinas()
            .agregar_alas()
            .agregar_tren_aterrizaje()
            .obtener()
        )


def _demo():
    builder = AvionComercialBuilder()
    director = Director(builder)
    avion = director.construir()
    print(avion)
    # Validacion del enunciado: cantidades correctas de partes.
    assert avion.body is not None
    assert len(avion.turbinas) == 2
    assert len(avion.alas) == 2
    assert avion.tren_aterrizaje is not None
    print("OK: 1 body, 2 turbinas, 2 alas y 1 tren de aterrizaje.")


if __name__ == "__main__":
    _demo()
