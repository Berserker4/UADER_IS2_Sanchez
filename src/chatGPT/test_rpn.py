#!/usr/bin/env python3
"""
Pruebas unittest para rpn.py (cobertura objetivo >= 90%).
Errores: se validan con assertRaises y con bloques try/except segun consigna.
"""
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Carga rpn.py del mismo directorio
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rpn  # noqa: E402


class TestEjemplosEnunciado(unittest.TestCase):
    def test_suma_basica(self):
        self.assertEqual(rpn.evaluate("3 4 +"), 7.0)

    def test_expresion_hp(self):
        self.assertEqual(rpn.evaluate("5 1 2 + 4 * + 3 -"), 14.0)

    def test_dos_tres_cuatro(self):
        self.assertEqual(rpn.evaluate("2 3 4 * +"), 14.0)


class TestErroresTryExcept(unittest.TestCase):
    """Errores cubiertos con try/except explicito (ademas de assertRaises)."""

    def test_division_por_cero_try(self):
        try:
            rpn.evaluate("3 0 /")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("division", str(e).lower())

    def test_uno_sobre_x_cero_try(self):
        try:
            rpn.evaluate("0 1/x")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("division", str(e).lower())

    def test_pila_insuficiente_try(self):
        try:
            rpn.evaluate("+")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("pila", str(e).lower())

    def test_fin_pila_distinto_de_uno_try(self):
        try:
            rpn.evaluate("1 2")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("exactamente un valor", str(e).lower())

    def test_token_invalido_try(self):
        try:
            rpn.evaluate("noexiste")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("token", str(e).lower())

    def test_sqrt_negativo_try(self):
        try:
            rpn.evaluate("-1 sqrt")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("sqrt", str(e).lower())

    def test_log_dom_try(self):
        try:
            rpn.evaluate("-1 log")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("log", str(e).lower())

    def test_asin_dom_try(self):
        try:
            rpn.evaluate("2 asin")
            self.fail("debio lanzar RPNError")
        except rpn.RPNError as e:
            self.assertIn("asin", str(e).lower())


class TestErroresAssertRaises(unittest.TestCase):
    def test_sto_sin_slot(self):
        with self.assertRaises(rpn.RPNError):
            rpn.evaluate("STO")

    def test_rcl_sin_slot(self):
        with self.assertRaises(rpn.RPNError):
            rpn.evaluate("RCL")


class TestPilaYConstantes(unittest.TestCase):
    def test_dup_swap_drop_clear(self):
        self.assertEqual(rpn.evaluate("1 dup +"), 2.0)
        self.assertEqual(rpn.evaluate("1 2 swap -"), 1.0)
        self.assertEqual(rpn.evaluate("5 3 drop"), 5.0)
        self.assertEqual(rpn.evaluate("9 8 clear 7"), 7.0)

    def test_constantes(self):
        import math

        self.assertAlmostEqual(rpn.evaluate("p"), math.pi)
        self.assertAlmostEqual(rpn.evaluate("e"), math.e)
        self.assertAlmostEqual(rpn.evaluate("j"), (1 + math.sqrt(5)) / 2)

    def test_chs(self):
        self.assertEqual(rpn.evaluate("3 CHS"), -3.0)


class TestAritmetica(unittest.TestCase):
    def test_floats_negativos(self):
        self.assertEqual(rpn.evaluate("-2 -3 *"), 6.0)

    def test_ops(self):
        self.assertEqual(rpn.evaluate("10 3 -"), 7.0)
        self.assertEqual(rpn.evaluate("6 7 *"), 42.0)
        self.assertEqual(rpn.evaluate("6 2 /"), 3.0)


class TestFuncs(unittest.TestCase):
    def test_sqrt_log_ln_ex_10x_yx_inv(self):
        self.assertEqual(rpn.evaluate("9 sqrt"), 3.0)
        self.assertEqual(rpn.evaluate("100 log"), 2.0)
        self.assertAlmostEqual(rpn.evaluate("1 ln"), 0.0)
        self.assertEqual(rpn.evaluate("0 ex"), 1.0)
        self.assertEqual(rpn.evaluate("2 10x"), 100.0)
        self.assertEqual(rpn.evaluate("2 3 yx"), 8.0)
        self.assertEqual(rpn.evaluate("4 1/x"), 0.25)


class TestTrigGrados(unittest.TestCase):
    def test_sin_cos_tg(self):
        self.assertEqual(rpn.evaluate("90 sin"), 1.0)
        self.assertEqual(rpn.evaluate("0 cos"), 1.0)
        self.assertAlmostEqual(rpn.evaluate("45 tg"), 1.0)

    def test_inv(self):
        self.assertEqual(rpn.evaluate("1 asin"), 90.0)
        self.assertEqual(rpn.evaluate("0 acos"), 90.0)
        self.assertEqual(rpn.evaluate("1 atan"), 45.0)


class TestMemoria(unittest.TestCase):
    def test_sto_rcl_compacto(self):
        self.assertEqual(rpn.evaluate("42 STO3 RCL3"), 42.0)

    def test_sto_rcl_dos_tokens(self):
        # 7 en M04; RCL 4 empuja 7; otro 4 literal; +: 7+4=11
        self.assertEqual(rpn.evaluate("7 STO 4 RCL 4 4 +"), 11.0)


class TestNormalizacionTokens(unittest.TestCase):
    def test_sto03(self):
        self.assertEqual(rpn.evaluate("99 STO03 RCL03"), 99.0)

    def test_norm_toks_sto_slot_invalido_except(self):
        # Cubre try/except en _norm_toks cuando _slot falla (STO + slot invalido).
        out = rpn._norm_toks(["STO", "99"])
        self.assertEqual(out, ["STO", "99"])

    def test_sto_slot_no_memoria(self):
        try:
            rpn.evaluate("7 STO foo")
            self.fail()
        except rpn.RPNError as e:
            self.assertIn("memoria", str(e).lower())

    def test_acos_fuera_dom(self):
        try:
            rpn.evaluate("2 acos")
            self.fail()
        except rpn.RPNError as e:
            self.assertIn("acos", str(e).lower())


class TestInvocacionScript(unittest.TestCase):
    """Cubre if __name__ == '__main__' ejecutando el archivo como script."""

    def test_runpy_main(self):
        import runpy

        buf = io.StringIO()
        err = io.StringIO()
        with patch.object(sys, "argv", ["rpn.py", "1", "1", "+"]):
            with patch("sys.stdout", buf):
                with patch("sys.stderr", err):
                    runpy.run_path(
                        str(Path(__file__).resolve().parent / "rpn.py"),
                        run_name="__main__",
                    )
        self.assertEqual(buf.getvalue().strip(), "2.0")


class TestMain(unittest.TestCase):
    def test_main_argv(self):
        with patch.object(sys, "argv", ["rpn.py", "3", "4", "+"]):
            with patch("sys.stdout", new_callable=io.StringIO) as out:
                rpn.main()
                self.assertEqual(out.getvalue().strip(), "7.0")

    def test_main_error_exit(self):
        with patch.object(sys, "argv", ["rpn.py", "3", "0", "/"]):
            with patch("sys.stderr", new_callable=io.StringIO):
                with self.assertRaises(SystemExit) as cm:
                    rpn.main()
                self.assertEqual(cm.exception.code, 1)

    def test_main_stdin(self):
        with patch.object(sys, "argv", ["rpn.py"]):
            with patch("sys.stdin", io.StringIO("2 3 +\n")):
                with patch("sys.stdout", new_callable=io.StringIO) as out:
                    rpn.main()
                    self.assertEqual(out.getvalue().strip(), "5.0")


if __name__ == "__main__":
    unittest.main()
