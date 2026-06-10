# TP8  # pylint: disable=invalid-name
"""
getJason - Recuperador de claves desde sitedata.json (Banco XXX).

copyright UADER-FCyT-IS2 (c) 2024 todos los derechos reservados.

Uso:
    python getJason.py [-v] [clave]
    python pagos.py              Ejecuta demo del sistema de pagos (TP8)

    -v, --version   Muestra la version del programa (1.2)
    clave           Clave a recuperar (default: token1)
"""
import sys
from pathlib import Path

from reader import ErrorPrograma, GetJasonSingleton

VERSION = '1.2'
CLAVE_DEFAULT = 'token1'
ARCHIVO_JSON = 'sitedata.json'


def _validar_argumentos(argumentos):
    if not argumentos:
        return 'ejecutar', CLAVE_DEFAULT

    if len(argumentos) > 1:
        raise ErrorPrograma(
            'Demasiados argumentos. Uso: getJason.py [-v] [clave]'
        )

    actual = argumentos[0]
    if actual in ('-v', '--version'):
        return 'version', None
    if actual in ('-h', '--help'):
        return 'ayuda', None
    if actual.startswith('-'):
        raise ErrorPrograma(f"Opcion desconocida: '{actual}'")
    if not actual.replace('_', '').isalnum():
        raise ErrorPrograma(
            f"Clave invalida '{actual}': solo letras, numeros y guion bajo"
        )
    return 'ejecutar', actual


def main(argumentos=None):
    """Punto de entrada CLI con errores controlados."""
    if argumentos is None:
        argumentos = sys.argv[1:]

    try:
        modo, clave = _validar_argumentos(argumentos)

        if modo == 'version':
            print(f'getJason version {VERSION}')
            return 0
        if modo == 'ayuda':
            print(__doc__)
            return 0

        archivo = str(Path(__file__).resolve().parent / ARCHIVO_JSON)
        lector = GetJasonSingleton(archivo)
        print(lector.obtener(clave))
        return 0

    except ErrorPrograma as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        print(f'Error del programa: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
