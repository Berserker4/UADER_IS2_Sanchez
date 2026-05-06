#!/usr/bin/python3
# * TP4 - Punto 3 : Patron Composite                                        *
from abc import ABC, abstractmethod


class Componente(ABC):
    """Interfaz comun para piezas individuales y para compuestos."""

    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def mostrar(self, nivel=0):
        """Imprime el componente con sangria proporcional al nivel."""


class Pieza(Componente):
    """Hoja: pieza individual, no admite hijos."""

    def mostrar(self, nivel=0):
        print("  " * nivel + f"- Pieza: {self.nombre}")


class Compuesto(Componente):
    """Composite generico que mantiene una lista de hijos (piezas o sub-compuestos)."""

    def __init__(self, nombre):
        super().__init__(nombre)
        self._hijos = []

    def agregar(self, componente):
        self._hijos.append(componente)
        return self

    def quitar(self, componente):
        self._hijos.remove(componente)

    def mostrar(self, nivel=0):
        print("  " * nivel + f"+ {type(self).__name__}: {self.nombre}")
        for hijo in self._hijos:
            hijo.mostrar(nivel + 1)


class SubConjunto(Compuesto):
    """Composite especifico: subconjunto de piezas."""


class Producto(Compuesto):
    """Composite raiz: producto principal."""


def _construir_producto():
    """Producto principal con 3 sub-conjuntos de 4 piezas cada uno."""
    producto = Producto("Producto Principal")

    for i in range(1, 4):
        sub = SubConjunto(f"Sub-conjunto {i}")
        for j in range(1, 5):
            sub.agregar(Pieza(f"Pieza {i}.{j}"))
        producto.agregar(sub)

    return producto


def _demo():
    print("=== Configuracion inicial ===")
    producto = _construir_producto()
    producto.mostrar()

    print("\n=== Se agrega un sub-conjunto opcional con 4 piezas ===")
    opcional = SubConjunto("Sub-conjunto OPCIONAL")
    for j in range(1, 5):
        opcional.agregar(Pieza(f"Pieza OPC.{j}"))
    producto.agregar(opcional)
    producto.mostrar()


if __name__ == "__main__":
    _demo()
