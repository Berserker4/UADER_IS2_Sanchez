#!/usr/bin/python3
# *-------------------------------------------------------------------------*
# * TP3 - Punto 2                                                           *
# *-------------------------------------------------------------------------*
import sys


class CalculadoraImpuestos:
    """Singleton: tasas centralizadas y un unico calculador compartido."""

    _instancia = None

    IVA = 0.21
    IIBB = 0.05
    MUNICIPAL = 0.012

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def calcular(self, base_imponible):
        """Devuelve la suma de IVA + IIBB + Municipales sobre la base."""
        if base_imponible < 0:
            raise ValueError("La base imponible no puede ser negativa")
        iva = base_imponible * self.IVA
        iibb = base_imponible * self.IIBB
        muni = base_imponible * self.MUNICIPAL
        return iva + iibb + muni

    def detalle(self, base_imponible):
        """Desglose util para auditar el calculo."""
        return {
            "base": base_imponible,
            "iva": base_imponible * self.IVA,
            "iibb": base_imponible * self.IIBB,
            "municipal": base_imponible * self.MUNICIPAL,
            "total_impuestos": self.calcular(base_imponible),
        }


class Venta:
    """Cliente: una venta usa el singleton para conocer sus impuestos."""

    def __init__(self, descripcion, base):
        self.descripcion = descripcion
        self.base = base
        self.calc = CalculadoraImpuestos()

    def total(self):
        return self.base + self.calc.calcular(self.base)


def _demo(base):
    v1 = Venta("Servicio profesional", base)
    v2 = Venta("Venta de bien", base * 2)
    print(f"{v1.descripcion}: base={v1.base:.2f}  total={v1.total():.2f}")
    print(f"{v2.descripcion}: base={v2.base:.2f}  total={v2.total():.2f}")
    print(f"Misma calculadora? {v1.calc is v2.calc}")
    print("Detalle v1:", v1.calc.detalle(v1.base))


if __name__ == "__main__":
    arg = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
    _demo(arg)
