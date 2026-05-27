# TP6
import subprocess
import sys


CASOS = [
    ("getJason.pyc", [], "api-token-banco-xxx-001"),
    ("getJason.pyc", ["token2"], "api-token-banco-xxx-001"),
    ("getJason.pyc", ["api_key"], "api-token-banco-xxx-001"),
    ("getJason.py", [], "api-token-banco-xxx-001"),
    ("getJason.py", ["token2"], "api-token-banco-xxx-002"),
    ("getJason.py", ["api_key"], "clave-microservicios-2026"),
    ("getJason.py", ["endpoint"], "https://api.bancoxxx.com/v1"),
]


def ejecutar(script, args):
    cmd = [sys.executable, script] + args
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def main():
    ok = 0
    fail = 0
    print("=" * 70)
    print("  TP6 - Casos de prueba getJason")
    print("=" * 70)

    for script, args, esperado in CASOS:
        codigo, salida, error = ejecutar(script, args)
        arg_txt = " ".join(args) if args else "(default token1)"
        pasa = codigo == 0 and salida == esperado
        estado = "OK" if pasa else "FAIL"
        if pasa:
            ok += 1
        else:
            fail += 1
        print(f"\n[{estado}] {script} {arg_txt}")
        print(f"  Esperado : {esperado}")
        print(f"  Obtenido : {salida}")
        if error:
            print(f"  Error    : {error}")

    print("\n" + "=" * 70)
    print(f"  Resultado: {ok} OK, {fail} FAIL de {ok + fail} casos")
    print("=" * 70)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
