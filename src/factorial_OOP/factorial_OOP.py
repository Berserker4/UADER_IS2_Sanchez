#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial_OOP.py                                                        *
#* Variante orientada a objetos sobre factorial.py                         *
#*-------------------------------------------------------------------------*
import re
import sys


class Factorial:
    """Cálculo de factorial en un rango [min, max] mediante run(min, max)."""

    def __init__(self):
        pass

    def _calc(self, num):
        # Misma lógica que factorial.py: casos base y producto iterativo.
        if num < 0:
            print("Factorial de un número negativo no existe")
            return 0
        if num == 0:
            return 1
        fact = 1
        n = num
        while n > 1:
            fact *= n
            n -= 1
        return fact

    def run(self, min_n, max_n):
        """Calcula e imprime el factorial de cada entero entre min_n y max_n (inclusive)."""
        lo = min(min_n, max_n)
        hi = max(min_n, max_n)
        for num in range(lo, hi + 1):
            print("Factorial ", num, "! es ", self._calc(num))


def parse_entrada(s):
    """Entero, rango a-b, '-hasta' (1..N), o 'desde-' (N..60). Valores siempre vía int()."""
    s = s.strip()
    m = re.match(r"^(\d+)-(\d+)$", s)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        return "rango", min(a, b), max(a, b)
    m = re.match(r"^-(\d+)$", s)
    if m:
        hasta = int(m.group(1))
        return "rango", 1, hasta
    m = re.match(r"^(\d+)-$", s)
    if m:
        desde = int(m.group(1))
        return "rango", desde, 60
    n = int(s)
    return "uno", n


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raw = input(
            "Ingrese número, rango a-b, -hasta (1..N), o desde- (N..60), ej. -10 o 50-: "
        )
    else:
        raw = sys.argv[1]

    tipo, *resto = parse_entrada(raw)
    app = Factorial()

    if tipo == "rango":
        lo, hi = resto
        app.run(lo, hi)
    else:
        n = resto[0]
        app.run(n, n)
