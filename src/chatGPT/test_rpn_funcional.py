#!/usr/bin/env python3
"""
Tests funcionales (caja negra) del ejecutable rpn.py.

Se invoca el script real con subprocess (mismo criterio que un usuario en terminal).
No importan detalles internos; solo salida, codigo de salida y stderr.

Casos de prueba (test cases) documentados:
  TC-F01  Suma basica 3+4 por argumentos -> stdout 7.0, codigo 0
  TC-F02  Expresion larga tipo calculadora HP -> 14.0, codigo 0
  TC-F03  Entrada por stdin (pipe) -> 5.0, codigo 0
  TC-F04  Division por cero -> stderr con mensaje, codigo 1
  TC-F05  Memoria STO/RCL compacto -> 42.0, codigo 0
  TC-F06  Constante pi (token p) -> valor cercano a pi, codigo 0
  TC-F07  Error: solo operador + sin operandos -> codigo 1
"""
import math
import subprocess
import sys
import unittest
from pathlib import Path

RPN = Path(__file__).resolve().parent / "rpn.py"
PY = sys.executable


def _run_argv(*args):
    return subprocess.run(
        [PY, str(RPN)] + list(args),
        capture_output=True,
        text=True,
        cwd=str(RPN.parent),
    )


def _run_stdin(text: str):
    return subprocess.run(
        [PY, str(RPN)],
        input=text,
        capture_output=True,
        text=True,
        cwd=str(RPN.parent),
    )


class TestFuncionalCajaNegra(unittest.TestCase):
    """Pruebas funcionales: binario rpn.py como proceso externo."""

    def test_tc_f01_suma_basica_argv(self):
        """TC-F01: 3 4 + por linea de comandos."""
        p = _run_argv("3", "4", "+")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "7.0")

    def test_tc_f02_expresion_hp(self):
        """TC-F02: 5 1 2 + 4 * + 3 -"""
        p = _run_argv("5", "1", "2", "+", "4", "*", "+", "3", "-")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "14.0")

    def test_tc_f03_stdin(self):
        """TC-F03: expresion por stdin."""
        p = _run_stdin("2 3 +\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "5.0")

    def test_tc_f04_division_cero(self):
        """TC-F04: 3 0 / debe fallar."""
        p = _run_argv("3", "0", "/")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("division", p.stderr.lower())

    def test_tc_f05_memoria_sto_rcl(self):
        """TC-F05: guardar y recuperar memoria 03."""
        p = _run_argv("42", "STO3", "RCL3")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "42.0")

    def test_tc_f06_constante_pi(self):
        """TC-F06: token p empuja pi."""
        p = _run_argv("p")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertAlmostEqual(float(p.stdout.strip()), math.pi)

    def test_tc_f07_operador_sin_operandos(self):
        """TC-F07: + solo -> error."""
        p = _run_argv("+")
        self.assertNotEqual(p.returncode, 0)
        self.assertTrue(p.stderr.strip() or p.stdout)


if __name__ == "__main__":
    unittest.main()
