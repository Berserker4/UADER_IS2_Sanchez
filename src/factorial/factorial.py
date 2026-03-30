#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import re
import sys

def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

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

if len(sys.argv) < 2:
   raw = input(
       "Ingrese número, rango a-b, -hasta (1..N), o desde- (N..60), ej. -10 o 50-: "
   )
else:
   raw = sys.argv[1]

tipo, *resto = parse_entrada(raw)

if tipo == "rango":
    lo, hi = resto
    for num in range(lo, hi + 1):
        print("Factorial ", num, "! es ", factorial(num))
else:
    num = resto[0]
    print("Factorial ", num, "! es ", factorial(num)) 
