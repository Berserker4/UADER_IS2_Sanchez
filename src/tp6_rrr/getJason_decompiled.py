# uncompyle6 version 3.9.3
# Python bytecode version base 3.11 (3495)
# Decompiled from: Python 3.11.8
# Embedded file name: _legacy_source.py

import json
import sys


def getJason(json_file='sitedata.json'):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data['token1']


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    print(getJason())
