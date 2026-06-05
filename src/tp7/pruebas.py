# TP7
"""Casos de prueba para getJason refactorizado (TP7)."""
import subprocess
import sys


def ejecutar(args):
    comando = [sys.executable, 'getJason.py'] + args
    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        cwd='.',
    )
    return resultado.returncode, resultado.stdout.strip(), resultado.stderr.strip()


CASOS_OK = [
    ([], 0, 'api-token-banco-xxx-001', ''),
    (['token2'], 0, 'api-token-banco-xxx-002', ''),
    (['api_key'], 0, 'clave-microservicios-2026', ''),
    (['-v'], 0, 'getJason version 1.1', ''),
    (['--version'], 0, 'getJason version 1.1', ''),
    (['--legacy', 'endpoint'], 0, 'https://api.bancoxxx.com/v1', ''),
]

CASOS_ERROR = [
    (['clave!'], 1, '', 'Error:'),
    (['-v', 'token1'], 1, '', 'Error:'),
    (['--foo'], 1, '', 'Error:'),
    (['a', 'b', 'c'], 1, '', 'Error:'),
    (['clave_inexistente'], 1, '', 'Error:'),
]


def main():
    ok = 0
    fail = 0
    print('=' * 60)
    print('  TP7 - Pruebas getJason')
    print('=' * 60)

    for args, codigo_esperado, salida_esperada, error_contiene in CASOS_OK + CASOS_ERROR:
        codigo, salida, error = ejecutar(args)
        arg_txt = ' '.join(args) if args else '(default)'
        salida_ok = salida == salida_esperada
        codigo_ok = codigo == codigo_esperado
        error_ok = error_contiene in error if error_contiene else True
        pasa = salida_ok and codigo_ok and error_ok
        estado = 'OK' if pasa else 'FAIL'
        if pasa:
            ok += 1
        else:
            fail += 1
        print(f'\n[{estado}] getJason.py {arg_txt}')
        print(f'  Esperado codigo : {codigo_esperado}  Obtenido : {codigo}')
        print(f'  Esperado salida : {salida_esperada!r}')
        print(f'  Obtenido salida : {salida!r}')
        if error:
            print(f'  stderr          : {error}')

    print('\n' + '=' * 60)
    print(f'  Resultado: {ok} OK, {fail} FAIL')
    print('=' * 60)
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
