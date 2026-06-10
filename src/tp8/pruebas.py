# TP8
"""Casos de prueba del sistema de pagos (TP8)."""
import subprocess
import sys
from pathlib import Path

from pagos import ComandoPago, SistemaPagos


def ejecutar_getjason(args):
    comando = [sys.executable, 'getJason.py'] + args
    resultado = subprocess.run(comando, capture_output=True, text=True, cwd='.')
    return resultado.returncode, resultado.stdout.strip(), resultado.stderr.strip()


def probar_getjason():
    ok = 0
    casos = [
        ([], 0, 'api-token-banco-xxx-001'),
        (['token2'], 0, 'api-token-banco-xxx-002'),
        (['-v'], 0, 'getJason version 1.2'),
    ]
    for args, codigo_esperado, salida_esperada in casos:
        codigo, salida, _ = ejecutar_getjason(args)
        if codigo == codigo_esperado and salida == salida_esperada:
            ok += 1
    return ok, len(casos)


def probar_pagos():
    archivo = str(Path(__file__).resolve().parent / 'sitedata.json')
    sistema = SistemaPagos(archivo)
    ok = 0
    total = 0

    esperados = [
        ('P001', 'token1', 500.0),
        ('P002', 'token2', 500.0),
        ('P003', 'token1', 500.0),
        ('P004', 'token2', 500.0),
        ('P005', 'token2', 500.0),
        ('P006', 'token2', 500.0),
    ]

    for numero, token_esperado, monto in esperados:
        total += 1
        comando = ComandoPago(numero, monto, sistema)
        resultado = sistema.ejecutar_comando(comando)
        if (
            resultado.numero_pedido == numero
            and resultado.token == token_esperado
            and resultado.monto == monto
        ):
            ok += 1

    total += 1
    saldos = sistema.saldos()
    if saldos['token1'] == 0.0 and saldos['token2'] == 0.0:
        ok += 1

    total += 1
    if sistema.total_pagos() == 6:
        ok += 1

    return ok, total


def main():
    ok_j, tot_j = probar_getjason()
    ok_p, tot_p = probar_pagos()
    ok = ok_j + ok_p
    total = tot_j + tot_p

    print('=' * 60)
    print('  TP8 - Pruebas')
    print('=' * 60)
    print(f'  getJason.py : {ok_j}/{tot_j} OK')
    print(f'  pagos.py    : {ok_p}/{tot_p} OK')
    print('=' * 60)
    print(f'  Total: {ok}/{total} OK')
    print('=' * 60)
    return 0 if ok == total else 1


if __name__ == '__main__':
    sys.exit(main())
