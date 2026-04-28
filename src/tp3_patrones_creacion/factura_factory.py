#!/usr/bin/python3
# *-------------------------------------------------------------------------*
# * TP3 - Punto 4                                                           *
# *-------------------------------------------------------------------------*
import sys
from abc import ABC, abstractmethod


class Factura(ABC):
    """Producto abstracto que representa una factura emitida."""

    letra = "?"
    condicion = "indefinida"

    def __init__(self, importe):
        if importe < 0:
            raise ValueError("El importe no puede ser negativo")
        self.importe = importe

    @abstractmethod
    def leyenda(self):
        """Texto especifico que distingue cada tipo de factura."""

    def emitir(self):
        print(f"FACTURA {self.letra} - {self.condicion}")
        print(f"  Importe total: $ {self.importe:.2f}")
        print(f"  {self.leyenda()}")


class FacturaResponsable(Factura):
    letra = "A"
    condicion = "IVA Responsable Inscripto"

    def leyenda(self):
        return "Discrimina IVA. Habilitada para credito fiscal del receptor."


class FacturaNoInscripto(Factura):
    letra = "B"
    condicion = "IVA No Inscripto"

    def leyenda(self):
        return "No discrimina IVA en el detalle. Operacion a consumidor final."


class FacturaExento(Factura):
    letra = "C"
    condicion = "IVA Exento"

    def leyenda(self):
        return "Operacion exenta de IVA segun normativa vigente."


class FabricaFactura:
    """Factory Method: instancia la factura segun la condicion del cliente."""

    _registro = {
        "responsable": FacturaResponsable,
        "no_inscripto": FacturaNoInscripto,
        "exento": FacturaExento,
    }

    @classmethod
    def crear(cls, condicion, importe):
        clave = condicion.strip().lower().replace(" ", "_")
        if clave not in cls._registro:
            opciones = ", ".join(cls._registro)
            raise ValueError(
                f"Condicion impositiva invalida: {condicion!r}. Opciones: {opciones}"
            )
        return cls._registro[clave](importe)


def _demo(importe):
    for cond in ("responsable", "no_inscripto", "exento"):
        FabricaFactura.crear(cond, importe).emitir()
        print("-" * 40)


if __name__ == "__main__":
    arg = float(sys.argv[1]) if len(sys.argv) > 1 else 12500.0
    _demo(arg)
