"""Ejecuta una sesión de test (unitario o funcional) contra una versión del programa."""
import subprocess
import sys

ESPERADO = {1: 0, 2: 1, 3: 7, 27: 111, 1999: 50}

# (id, descripcion, n)
UNITARIOS = [
    ("T1", "collatz(1) == 0", 1, ("val", 0)),
    ("T2", "collatz(2) == 1", 2, ("val", 1)),
    ("T3", "collatz(3) == 7", 3, ("val", 7)),
    ("T4", "collatz(27) == 111", 27, ("val", 111)),
    ("T5", "collatz(0) -> ValueError", 0, ("err", None)),
    ("T6", "collatz(2000) -> ValueError", 2000, ("err", None)),
    ("T7", "collatz(1999) == 50", 1999, ("val", 50)),
    ("T8", "collatz(-5) -> ValueError", -5, ("err", None)),
]
# (id, descripcion, stdin, esperado)
FUNCIONALES = [
    ("T9", "entrada 20", "20\n", ("ok", "El número de iteraciones para 20 es 7")),
    ("T10", "entrada 2000", "2000\n", ("error", None)),
    ("T11", "entrada -5", "-5\n", ("error", None)),
    ("T12", "entrada abc", "abc\n", ("error", None)),
    ("T13", "entrada 1999", "1999\n", ("ok", "El número de iteraciones para 1999 es 50")),
    ("T14", "entrada 3.5", "3.5\n", ("error", None)),
    ("T15", "entrada vacía", "", ("error", None)),
    ("T16", "1999 en < 1 s", "1999\n", ("ok", "El número de iteraciones para 1999 es 50")),
]

LOADER = (
    "import importlib.util,sys;"
    "s=importlib.util.spec_from_file_location('m',sys.argv[1]);"
    "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
)


def importar(path):
    r = subprocess.run([sys.executable, "-I", "-c", LOADER, path],
                       capture_output=True, text=True, timeout=10)
    return r.returncode == 0, (r.stderr.strip().splitlines() or [""])[-1]


def unitarios(path):
    ok_imp, msg = importar(path)
    if not ok_imp:
        print(f"  INTENTO DE EJECUCIÓN FALLIDO al importar: {msg}")
        return 1, 0, 0
    fallos = pasan = 0
    for tid, desc, n, (kind, val) in UNITARIOS:
        code = LOADER + (
            "\ntry:\n r=m.collatz(%d)\nexcept ValueError:\n print('VALUEERROR')\n"
            "else:\n print('VAL',r)\n" % n)
        try:
            r = subprocess.run([sys.executable, "-I", "-c", code, path],
                               capture_output=True, text=True, timeout=5)
            out = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-60:]
            good = (kind == "err" and out == "VALUEERROR") or (
                kind == "val" and out == f"VAL {val}")
        except subprocess.TimeoutExpired:
            out, good = "TIMEOUT (bucle infinito)", False
        print(f"  {tid:4} {desc:32} {'PASS' if good else 'FAIL  -> ' + out}")
        pasan += good
        fallos += not good
    return fallos, pasan, len(UNITARIOS)


def funcionales(path):
    fallos = pasan = 0
    for tid, desc, stdin, (kind, val) in FUNCIONALES:
        try:
            r = subprocess.run([sys.executable, "-I", path], input=stdin,
                               capture_output=True, text=True, timeout=5)
            if kind == "ok":
                good = r.returncode == 0 and val in r.stdout and "Traceback" not in r.stderr
            else:
                good = (r.returncode != 0 and r.stderr.startswith("Error:")
                        and "Traceback" not in r.stderr)
            out = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or [""])[-1]
        except subprocess.TimeoutExpired:
            good, out = False, "TIMEOUT"
        print(f"  {tid:4} {desc:20} {'PASS' if good else 'FAIL  -> ' + out[:70]}")
        pasan += good
        fallos += not good
    return fallos, pasan, len(FUNCIONALES)


if __name__ == "__main__":
    tipo, path = sys.argv[1], sys.argv[2]
    f, p, t = (unitarios if tipo == "unit" else funcionales)(path)
    print(f"  => defectos: {f}  | casos ejecutados OK: {p}/{t}")
