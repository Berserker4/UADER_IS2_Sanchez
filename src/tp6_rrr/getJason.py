# TP6
"""
Recupera valores de claves desde sitedata.json.

Uso:
    python getJason.py [clave]

    clave: nombre de la clave a recuperar (default: token1)
"""
import json
import sys


def getJason(clave='token1', json_file='sitedata.json'):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if clave not in data:
        raise KeyError(f"La clave '{clave}' no existe en {json_file}")
    return data[clave]


if __name__ == '__main__':
    clave = sys.argv[1] if len(sys.argv) > 1 else 'token1'
    print(getJason(clave))
