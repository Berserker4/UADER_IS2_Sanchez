#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* TP10 - Ejercicio 2: equilibrio financiero proveedor / patrocinante
#* Costo 1000/mes x 12, pago 14000 al entregar, r = 1% mensual
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
"""Escenarios de pago neutros para el proveedor (mismo VPN)."""

from __future__ import annotations

R = 0.01
COSTO = 1000.0
PAGO_BASE = 14000.0


def pv(monto: float, t: int, rate: float = R) -> float:
    return monto / (1.0 + rate) ** t


def pv_anualidad(cuota: float, n: int, rate: float = R) -> float:
    return cuota * (1.0 - (1.0 + rate) ** (-n)) / rate


def main() -> None:
    costo12 = pv_anualidad(COSTO, 12)
    pago12 = pv(PAGO_BASE, 12)
    npv0 = pago12 - costo12

    # a) pago en mes 14 (sin staff extra)
    pago_a = PAGO_BASE * (1.0 + R) ** 2

    # b) entrega mes 6, pago en mes 12
    costo6 = pv_anualidad(COSTO, 6)
    pago_b = (npv0 + costo6) * (1.0 + R) ** 12

    # c) entrega y pago en mes 6
    pago_c = (npv0 + costo6) * (1.0 + R) ** 6

    print("=== TP10 Ejercicio 2 ===")
    print(f"Equilibrio base: VP_costo={costo12:.2f} VP_pago={pago12:.2f} NPV={npv0:.2f}")
    print(f"a) Pago neutro en mes 14: {pago_a:.2f}")
    print(f"b) Entrega mes 6 / pago mes 12: {pago_b:.2f}")
    print(f"c) Entrega y pago mes 6: {pago_c:.2f}")
    print("Checks NPV:")
    print(f"  a -> {pv(pago_a, 14) - costo12:.2f}")
    print(f"  b -> {pv(pago_b, 12) - costo6:.2f}")
    print(f"  c -> {pv(pago_c, 6) - costo6:.2f}")


if __name__ == "__main__":
    main()
