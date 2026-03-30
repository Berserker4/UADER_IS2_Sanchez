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
    # Casos base: negativo (no definido clásico), 0! = 1.
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        # Producto n·(n-1)·…·2; se reduce num en cada paso.
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

def parse_entrada(s):
    """Entero, rango a-b, '-hasta' (1..N), o 'desde-' (N..60). Valores siempre vía int()."""
    s = s.strip()
    # Formato explícito "desde-hasta" con dos enteros no negativos.
    m = re.match(r"^(\d+)-(\d+)$", s)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        return "rango", min(a, b), max(a, b)
    # "-N": rango sin límite inferior → factorial de 1 hasta N inclusive.
    m = re.match(r"^-(\d+)$", s)
    if m:
        hasta = int(m.group(1))
        return "rango", 1, hasta
    # "N-": rango sin límite superior fijo en consigna → desde N hasta 60 inclusive.
    m = re.match(r"^(\d+)-$", s)
    if m:
        desde = int(m.group(1))
        return "rango", desde, 60
    # Un solo entero (puede ser negativo si no matchea los patrones anteriores).
    n = int(s)
    return "uno", n

# Argumento en línea de comandos o, si falta, entrada por teclado.
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
