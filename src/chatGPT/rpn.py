#!/usr/bin/env python3
"""
Calculadora en notacion polaca inversa (RPN) — practico UADER IS2.

Pila: ultimo elemento = tope. Binarios (+ - * /, yx): se retiran x (tope) e y;
resultado y op x (coherente con ejemplos 3 4 + -> 7).

Errores: RPNError con mensajes claros; main() captura RPNError (try/except),
escribe en stderr y sale con codigo 1. Conversion numerica: try/except ValueError.

Memorias 00..09; STO/RCL en token compacto (STO3) o dos tokens (STO 3).
Trig: grados; inversas: salida en grados.
Sin eval ni exec.
"""

# =============================================================================
# Estructura del modulo (TP IS2 — multimetric / comment_ratio):
# 1) Imports y constantes globales (regex, tablas trig, memorias implicitas).
# 2) Excepcion RPNError y utilidades de pila (_need, _pop).
# 3) Normalizacion de tokens STO/RCL (_norm_toks, _slot).
# 4) Aplicacion de operadores por familias (_apply_*).
# 5) Bucle principal evaluate() y punto de entrada main().
# =============================================================================

from __future__ import annotations

import math
import re
import sys
from collections.abc import Callable
from typing import Final

# --- Constantes y tablas ------------------------------------------------------
# PHI: numero aureado para la constante de usuario 'j'.
# _K: constantes p(pi), e, j empujadas como literales simbolicos.
# _TR / _ARC: funciones trig en grados (entradas) y salida inversa en grados.
PHI: Final[float] = (1.0 + math.sqrt(5.0)) / 2.0
_K: Final[dict[str, float]] = {"p": math.pi, "e": math.e, "j": PHI}
_TR: Final[dict[str, Callable[[float], float]]] = {
    "sin": math.sin,
    "cos": math.cos,
    "tg": math.tan,
}
_ARC: Final[dict[str, Callable[[float], float]]] = {
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
}

# Regex compiladas: evita recompilar patrones en cada token (rendimiento leve).
_RE_SLOT = re.compile(r"^(0[0-9]|[0-9])$")
_RE_STO_RCL_COMPACT = re.compile(r"^(STO|RCL)(0[0-9]|[0-9])$", re.I)


class RPNError(Exception):
    """Error de evaluacion RPN (pila, dominio, token invalido, etc.)."""


# --- Pila: comprobaciones minimas --------------------------------------------
# La pila es una list[float]; el tope es el ultimo elemento.
def _need(stack: list[float], n: int) -> None:
    if len(stack) < n:
        raise RPNError("pila insuficiente para operar")


def _pop(stack: list[float]) -> float:
    _need(stack, 1)
    return stack.pop()


def _slot(tok: str) -> str:
    if not _RE_SLOT.match(tok) or int(tok) > 9:
        raise RPNError(f"slot de memoria invalido: {tok!r}")
    return f"{int(tok):02d}"


# --- Tokens: STO y RCL ---------------------------------------------------------
# Acepta forma compacta (STO3) o dos tokens (STO 3). Normaliza indice a "03".
def _norm_toks(ts: list[str]) -> list[str]:
    """Normaliza STO/RCL compactos (STO3) y forma de dos tokens."""
    o: list[str] = []
    i = 0
    while i < len(ts):
        m = _RE_STO_RCL_COMPACT.match(ts[i])
        if m:
            o += [m.group(1).upper(), _slot(m.group(2))]
            i += 1
            continue
        t = ts[i]
        if t.upper() in ("STO", "RCL") and i + 1 < len(ts):
            try:
                o += [t.upper(), _slot(ts[i + 1])]
                i += 2
                continue
            except RPNError:
                pass
        o.append(t)
        i += 1
    return o


# --- Memorias 00..09 ---------------------------------------------------------
# STO guarda el tope de la pila; RCL empuja el valor del slot.
def _process_sto_rcl(
    stack: list[float],
    mem: dict[str, float],
    ts: list[str],
    i: int,
    tok_upper: str,
) -> int:
    """Procesa STO/RCL con indice; devuelve el nuevo indice i."""
    if i + 1 >= len(ts):
        raise RPNError(f"{tok_upper} requiere indice de memoria")
    sl = ts[i + 1]
    if sl not in mem:
        raise RPNError(f"slot de memoria invalido: {sl!r}")
    if tok_upper == "STO":
        _need(stack, 1)
        mem[sl] = _pop(stack)
    else:
        stack.append(mem[sl])
    return i + 2


# --- Aritmetica binaria (+ - * /) --------------------------------------------
# Orden RPN: se sacan x (tope) e y; se calcula y op x como en los ejemplos.
def _apply_binary_arithmetic(stack: list[float], t: str) -> None:
    x, y = _pop(stack), _pop(stack)
    if t == "+":
        stack.append(y + x)
    elif t == "-":
        stack.append(y - x)
    elif t == "*":
        stack.append(y * x)
    else:
        if x == 0:
            raise RPNError("division por cero")
        stack.append(y / x)


# --- Comandos de pila (dup, swap, drop, clear, chs) -------------------------
def _apply_stack_op(stack: list[float], u: str) -> None:
    """dup, swap, drop, clear, chs (u ya validado por el llamador)."""
    if u == "dup":
        _need(stack, 1)
        stack.append(stack[-1])
    elif u == "swap":
        _need(stack, 2)
        a, b = stack.pop(), stack.pop()
        stack.extend([a, b])
    elif u == "drop":
        _pop(stack)
    elif u == "clear":
        stack.clear()
    elif u == "chs":
        _need(stack, 1)
        stack.append(-_pop(stack))


# --- Funciones cientificas (raiz, log, potencias, 1/x) -----------------------
def _apply_sqrt_log_exp(stack: list[float], u: str, t_raw: str) -> bool:
    """sqrt, log, ln, ex, 10x, yx, 1/x. True si reconoce u."""
    if u == "sqrt":
        _need(stack, 1)
        a = _pop(stack)
        if a < 0:
            raise RPNError("sqrt de valor negativo")
        stack.append(math.sqrt(a))
        return True
    if u in ("log", "ln"):
        _need(stack, 1)
        a = _pop(stack)
        if a <= 0:
            raise RPNError("log/ln: argumento debe ser > 0")
        stack.append(math.log10(a) if u == "log" else math.log(a))
        return True
    if u in ("ex", "10x"):
        _need(stack, 1)
        a = _pop(stack)
        stack.append(math.exp(a) if u == "ex" else 10**a)
        return True
    if u == "yx":
        _need(stack, 2)
        x, y = _pop(stack), _pop(stack)
        stack.append(y**x)
        return True
    if t_raw == "1/x" or u == "1/x":
        _need(stack, 1)
        a = _pop(stack)
        if a == 0:
            raise RPNError("division por cero")
        stack.append(1.0 / a)
        return True
    return False


# --- Trigonometria en grados --------------------------------------------------
# sin/cos/tg reciben grados; internamente se convierte a radianes para math.*.
def _apply_trig(stack: list[float], u: str) -> bool:
    if u not in _TR:
        return False
    _need(stack, 1)
    stack.append(_TR[u](math.radians(_pop(stack))))
    return True


# --- Arcoseno/arco tangente: dominio [-1,1] para asin/acos -------------------
def _apply_arc(stack: list[float], u: str) -> bool:
    if u not in _ARC:
        return False
    _need(stack, 1)
    a = _pop(stack)
    if u in ("asin", "acos") and (a < -1.0 or a > 1.0):
        raise RPNError(f"{u}: argumento fuera de [-1,1]")
    stack.append(math.degrees(_ARC[u](a)))
    return True


# --- Evaluacion principal ----------------------------------------------------
# Recorre tokens: numeros con float(); operadores delegan en helpers.
def evaluate(expr: str) -> float:
    """Evalua una expresion RPN (string con tokens separados por espacio)."""
    ts = _norm_toks(expr.split())
    stack: list[float] = []
    mem = {f"{k:02d}": 0.0 for k in range(10)}
    i = 0
    while i < len(ts):
        t = ts[i]
        try:
            stack.append(float(t))
            i += 1
            continue
        except ValueError:
            pass
        u = t.lower()
        tok_upper = t.upper()
        if u in _K:
            stack.append(_K[u])
        elif tok_upper in ("STO", "RCL"):
            i = _process_sto_rcl(stack, mem, ts, i, tok_upper)
            continue
        elif u in ("dup", "swap", "drop", "clear", "chs"):
            _apply_stack_op(stack, u)
        elif t in "+-*/":
            _apply_binary_arithmetic(stack, t)
        elif _apply_sqrt_log_exp(stack, u, t):
            pass
        elif _apply_trig(stack, u):
            pass
        elif _apply_arc(stack, u):
            pass
        else:
            raise RPNError(f"token invalido: {t!r}")
        i += 1
    if len(stack) != 1:
        raise RPNError("al final debe quedar exactamente un valor en la pila")
    return stack[0]


# --- Entrada/salida: argv unidos o stdin; errores en stderr ------------------
def main() -> None:
    """Lee argv o stdin, imprime resultado o error en stderr."""
    line = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    try:
        print(evaluate(line))
    except RPNError as err:
        print(err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
