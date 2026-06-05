# TP7  # pylint: disable=invalid-name
"""
getJason - Recuperador de claves desde sitedata.json (Banco XXX).

copyright UADER-FCyT-IS2 (c) 2024 todos los derechos reservados.

Uso:
    python getJason.py [-v] [clave]
    python getJason.py [--legacy] [clave]

    -v, --version   Muestra la version del programa (1.1)
    --legacy        Usa la rama legada (Branching by abstraction / TP6)
    clave           Clave a recuperar (default: token1)
"""
import sys
from pathlib import Path

from reader import ErrorPrograma, crear_lector

VERSION = '1.1'
CLAVE_DEFAULT = 'token1'
ARCHIVO_JSON = 'sitedata.json'


def _mostrar_ayuda():
    print(__doc__)


def _validar_argumentos(argumentos):
    """
    Valida argumentos de linea de comandos.
    Devuelve (modo, clave, usar_singleton).
    modo: 'version' | 'ayuda' | 'ejecutar'
    """
    if not argumentos:
        return 'ejecutar', CLAVE_DEFAULT, True

    if len(argumentos) > 2:
        raise ErrorPrograma(
            'Demasiados argumentos. Uso: getJason.py [-v] [--legacy] [clave]'
        )

    usar_singleton = True
    clave = CLAVE_DEFAULT
    pendientes = list(argumentos)

    while pendientes:
        actual = pendientes.pop(0)
        if actual in ('-v', '--version'):
            if pendientes:
                raise ErrorPrograma('La opcion -v no admite argumentos adicionales')
            return 'version', None, True
        if actual in ('-h', '--help'):
            return 'ayuda', None, True
        if actual == '--legacy':
            usar_singleton = False
            continue
        if actual.startswith('-'):
            raise ErrorPrograma(f"Opcion desconocida: '{actual}'")
        if clave != CLAVE_DEFAULT:
            raise ErrorPrograma('Solo se permite una clave como argumento')
        clave = actual

    if not clave:
        raise ErrorPrograma('La clave no puede estar vacia')
    if not clave.replace('_', '').isalnum():
        raise ErrorPrograma(
            f"Clave invalida '{clave}': solo letras, numeros y guion bajo"
        )

    return 'ejecutar', clave, usar_singleton


def main(argumentos=None):
    """Punto de entrada: nunca propaga excepciones del sistema al usuario."""
    if argumentos is None:
        argumentos = sys.argv[1:]

    try:
        modo, clave, usar_singleton = _validar_argumentos(argumentos)

        if modo == 'version':
            print(f'getJason version {VERSION}')
            return 0
        if modo == 'ayuda':
            _mostrar_ayuda()
            return 0

        archivo = str(Path(__file__).resolve().parent / ARCHIVO_JSON)
        lector = crear_lector(usar_singleton=usar_singleton, archivo_json=archivo)
        valor = lector.obtener(clave)
        print(valor)
        return 0

    except ErrorPrograma as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        print(f'Error del programa: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
