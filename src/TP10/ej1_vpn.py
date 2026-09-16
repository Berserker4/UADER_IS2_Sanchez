#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* TP10 - Ejercicio 1: VPN, rentabilidad y gestion profesional
#* Flujo: -1000/mes (vencido), beneficio 18000 al entregar, r = 1% mensual
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
"""Calcula VPN y rentabilidad de escenarios del TP10 ej.1."""

from __future__ import annotations

R = 0.01
COSTO_MENSUAL = 1000.0
BENEFICIO = 18000.0


def pv(monto: float, t: int, rate: float = R) -> float:
    return monto / (1.0 + rate) ** t


def pv_anualidad(cuota: float, n: int, rate: float = R) -> float:
    return cuota * (1.0 - (1.0 + rate) ** (-n)) / rate


def escenario(meses: int, costo_mensual: float = COSTO_MENSUAL) -> dict:
    inv = pv_anualidad(costo_mensual, meses)
    ben = pv(BENEFICIO, meses)
    vpn = ben - inv
    return {
        "meses": meses,
        "costo_mensual": costo_mensual,
        "vp_inversion": inv,
        "vp_beneficio": ben,
        "vpn": vpn,
        "rentabilidad": vpn / inv,
    }


def main() -> None:
    plan = escenario(12)
    delay3 = escenario(15)
    delay6 = escenario(18)
    pm = escenario(12, COSTO_MENSUAL * 1.05)

    # Desafio: 15 meses, mismo VPN que el plan, max costo mensual
    ann15 = (1.0 - (1.0 + R) ** (-15)) / R
    c_max = (pv(BENEFICIO, 15) - plan["vpn"]) / ann15
    check = escenario(15, c_max)

    print("=== TP10 Ejercicio 1 ===")
    for nombre, esc in [
        ("a) Plan 12 meses", plan),
        ("b) Extension 15 meses", delay3),
        ("d) Retraso 6 meses (18)", delay6),
        ("e) Gestion PM +5%", pm),
    ]:
        print(
            f"{nombre}: VPN={esc['vpn']:.2f} | "
            f"VP_inv={esc['vp_inversion']:.2f} | "
            f"rent={esc['rentabilidad']*100:.2f}%"
        )

    print(
        f"c) Rentabilidad plan={plan['rentabilidad']*100:.2f}% | "
        f"ext15={delay3['rentabilidad']*100:.2f}%"
    )
    print(
        f"e) Conveniente PM? VPN_PM={pm['vpn']:.2f} > VPN_ext15={delay3['vpn']:.2f} "
        f"-> {pm['vpn'] > delay3['vpn']}"
    )
    print(f"f) Costo mensual max 15m (mismo VPN plan): {c_max:.2f}")
    print(f"   check VPN={check['vpn']:.2f} (objetivo {plan['vpn']:.2f})")


if __name__ == "__main__":
    main()
