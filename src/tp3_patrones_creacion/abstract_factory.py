#!/usr/bin/python3
# *-------------------------------------------------------------------------*
# * TP3 - Punto 7                                                           *
# *-------------------------------------------------------------------------*
import sys
from abc import ABC, abstractmethod


class Boton(ABC):
    @abstractmethod
    def dibujar(self):
        ...


class Checkbox(ABC):
    @abstractmethod
    def dibujar(self):
        ...


class BotonWindows(Boton):
    def dibujar(self):
        return "[ Boton estilo Windows ]"


class CheckboxWindows(Checkbox):
    def dibujar(self):
        return "[X] Checkbox estilo Windows"


class BotonLinux(Boton):
    def dibujar(self):
        return "( Boton estilo Linux )"


class CheckboxLinux(Checkbox):
    def dibujar(self):
        return "(*) Checkbox estilo Linux"


class FabricaGUI(ABC):
    """Abstract Factory: define la creacion de la familia completa de widgets."""

    @abstractmethod
    def crear_boton(self):
        ...

    @abstractmethod
    def crear_checkbox(self):
        ...


class FabricaWindows(FabricaGUI):
    def crear_boton(self):
        return BotonWindows()

    def crear_checkbox(self):
        return CheckboxWindows()


class FabricaLinux(FabricaGUI):
    def crear_boton(self):
        return BotonLinux()

    def crear_checkbox(self):
        return CheckboxLinux()


class Aplicacion:
    """Cliente: usa la fabrica abstracta sin conocer las clases concretas."""

    def __init__(self, fabrica):
        self.boton = fabrica.crear_boton()
        self.checkbox = fabrica.crear_checkbox()

    def render(self):
        print(self.boton.dibujar())
        print(self.checkbox.dibujar())


def _seleccionar_fabrica(plataforma):
    plataforma = plataforma.strip().lower()
    if plataforma in ("windows", "win"):
        return FabricaWindows()
    if plataforma in ("linux", "lin"):
        return FabricaLinux()
    raise ValueError(f"Plataforma no soportada: {plataforma!r}")


def _demo(plataforma=None):
    if plataforma is None:
        for p in ("windows", "linux"):
            print(f"--- {p.upper()} ---")
            Aplicacion(_seleccionar_fabrica(p)).render()
    else:
        Aplicacion(_seleccionar_fabrica(plataforma)).render()


if __name__ == "__main__":
    _demo(sys.argv[1] if len(sys.argv) > 1 else None)
