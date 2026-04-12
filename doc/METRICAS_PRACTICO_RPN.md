# Práctico RPN — Metodología, pruebas y multimetric

## 1. Metodología con ChatGPT

- Se elaboraron **prompts sucesivos** para definir la calculadora RPN: pila, literales, operadores, memorias `STO`/`RCL`, funciones, `RPNError`, `main` por argv/stdin, sin `eval`/`exec`.
- Los fragmentos generados se **integraron y ajustaron** en el archivo local [`src/chatGPT/rpn.py`](../src/chatGPT/rpn.py).
- Se añadió la batería [`src/chatGPT/test_rpn.py`](../src/chatGPT/test_rpn.py) con **`unittest`**, objetivo de **cobertura ≥ 90 %** sobre `rpn.py` (logrado **100 %** con `coverage`).
- Las **pruebas funcionales** (caja negra, proceso real `python rpn.py`) están en [`src/chatGPT/test_rpn_funcional.py`](../src/chatGPT/test_rpn_funcional.py); los casos (TC-F01…TC-F07) se listan en §3.
- Las **condiciones de error** se cubren con:
  - **`try` / `except`** en los tests (p. ej. captura de `RPNError` al dividir por cero, token inválido, dominios de `sqrt`/`log`/`asin`).
  - **`assertRaises`** donde conviene.
  - En el programa, **`try`/`except`** en `evaluate` (conversión a `float`) y en `main` (errores de evaluación → stderr y código de salida ≠ 0).

## 2. Cobertura con la librería `coverage`

El módulo **`unittest`** de la biblioteca estándar **no** mide cobertura de líneas ni ramas: solo indica si los tests pasan o fallan. Para obtener un **porcentaje de código ejecutado** durante las pruebas hace falta una herramienta adicional, típicamente el paquete **[coverage](https://coverage.readthedocs.io/)** (`coverage` en PyPI).

### Instalación

```text
python -m pip install coverage
```

En este repo también: `python -m pip install -r requirements-dev.txt` (incluye `coverage`).

**PATH (Windows y venv):** si el comando `coverage` no se reconoce en la terminal, el ejecutable suele estar en `Scripts\` del Python o del entorno virtual. Una forma robusta es invocar el módulo con el mismo intérprete:

```text
py -3 -m coverage run ...
py -3 -m coverage report -m
```

Así no dependés de tener `Scripts` en el PATH.

### Flujo básico

```text
coverage run -m unittest -v
coverage report -m
```

`coverage run` ejecuta los tests bajo trazado; `coverage report -m` muestra el porcentaje por archivo y las **líneas que faltan** (`Missing`).

### Forzar cobertura mínima: `--fail-under=90`

```text
coverage report --fail-under=90
```

**Para qué sirve:** si el total de cobertura es **menor** al umbral (aquí 90 %), el comando termina con **código de salida distinto de cero**. Eso permite:

- **Integración continua (CI):** fallar el build si alguien agrega código sin tests suficientes.
- **Scripts locales o pre-commit:** no aceptar el cambio hasta subir la cobertura o añadir pruebas.
- **Reglas de equipo:** automatizar el requisito “≥ 90 %” sin depender de revisar el informe a mano cada vez.

### Reporte HTML (ver qué falta cubrir)

```text
coverage html
```

Genera la carpeta **`htmlcov/`** con `index.html`: vista por archivo, líneas en verde (ejecutadas) y rojo (no ejecutadas). Útil para decidir **qué tests escribir** para cubrir ramas o líneas concretas.

### Comandos en este proyecto (desde `src/chatGPT/`)

Los tests viven junto a `rpn.py`; conviene fijar qué se mide y omitir los propios archivos de test:

```text
py -3 -m unittest discover -p "test_*.py" -v
py -3 -m coverage run --source=. --omit="test_*.py" -m unittest discover -p "test_*.py" -q
py -3 -m coverage report -m --include="rpn.py"
py -3 -m coverage report -m --include="rpn.py" --fail-under=90
py -3 -m coverage html --include="rpn.py"
```

La línea con `coverage run` ejecuta **todas** las pruebas (`test_rpn.py` + `test_rpn_funcional.py`) y atribuye la cobertura principalmente a `rpn.py` (los `test_*.py` se omiten del cómputo). Abrí `htmlcov/index.html` tras `coverage html` (ruta relativa al directorio de trabajo actual).

---

## 3. Pruebas funcionales y casos de prueba (test cases)

Objetivo: verificar el programa **como usuario**: invocación por línea de comandos o stdin, salida en stdout, errores en stderr y código de salida.

| ID | Descripción breve | Entrada | Resultado esperado |
|----|-------------------|---------|----------------------|
| TC-F01 | Suma básica por argv | `python rpn.py 3 4 +` | stdout `7.0`, código 0 |
| TC-F02 | Expresión tipo HP | `python rpn.py 5 1 2 + 4 * + 3 -` | stdout `14.0`, código 0 |
| TC-F03 | Entrada por stdin | pipe `2 3 +\n` sin argumentos | stdout `5.0`, código 0 |
| TC-F04 | División por cero | `python rpn.py 3 0 /` | stderr con mensaje (p. ej. “division”), código ≠ 0 |
| TC-F05 | Memoria STO/RCL compacto | `python rpn.py 42 STO3 RCL3` | stdout `42.0`, código 0 |
| TC-F06 | Constante π | `python rpn.py p` | stdout ≈ π, código 0 |
| TC-F07 | Pila insuficiente | `python rpn.py +` | error en stderr, código ≠ 0 |

Implementación: clase `TestFuncionalCajaNegra` en `test_rpn_funcional.py` (subprocess, sin importar la lógica interna).

Instalación de herramientas: `py -3 -m pip install -r requirements-dev.txt` (raíz del repo).

---

## 4. Pylint (analizador estático)

### Instalación

```text
python -m pip install pylint
```

También: `py -3 -m pip install -r requirements-dev.txt` (incluye `pylint`). En Windows conviene `py -3 -m pylint` si `pylint.exe` no está en el PATH.

### Ejecución sobre `rpn.py` (consigna)

Desde el directorio del módulo:

```text
cd src\chatGPT
py -3 -m pylint rpn.py
```

### Análisis del resultado (primera corrida)

En la **primera corrida** (antes de refactor y estilo), pylint informó entre otros:

- **C0301** — líneas demasiado largas (> 100 caracteres).
- **C0410** — varios `import` en una sola línea (`math, re, sys`).
- **C0115 / C0116** — faltaban docstrings en `RPNError`, `evaluate` y `main`.
- **C0321** — más de una sentencia en la misma línea (p. ej. `_need`/`_pop`, cuerpo de `evaluate`).
- **C0103** — el nombre `U` no cumplía `snake_case`.
- **R0912 / R0915** — demasiadas ramas y sentencias en `evaluate` (umbral de pylint).

Puntuación aproximada: **7,70/10**. La salida completa se guardó en [`pylint_rpn_primera_corrida.txt`](pylint_rpn_primera_corrida.txt).

### Correcciones aplicadas

- **Imports:** un `import` por línea (`math`, `re`, `sys`).
- **Docstrings:** módulo ya existente; se añadieron textos en `RPNError`, funciones auxiliares donde aporta (`_norm_toks`, `_apply_stack_op`, `_apply_sqrt_log_exp`, `evaluate`, `main`).
- **Estilo:** se partieron líneas largas y sentencias encadenadas con `;` en varias líneas.
- **Nombres:** `U` sustituido por `tok_upper` (y uso coherente en memoria).
- **Complejidad:** se extrajo lógica de `evaluate` a funciones (`_process_sto_rcl`, `_apply_binary_arithmetic`, `_apply_stack_op`, `_apply_sqrt_log_exp`, `_apply_trig`, `_apply_arc`) para cumplir límites de ramas y sentencias sin cambiar el comportamiento.
- **Cobertura:** tras el refactor, se añadió el test `test_uno_sobre_x_cero_try` (`0 1/x`) para cubrir la rama de división por cero en `1/x` y mantener **100 %** de cobertura en `rpn.py`.

### Estado tras las correcciones

Segunda corrida: **10,00/10**, sin mensajes de tipo `C`/`R`/`W` en `rpn.py`. Detalle en [`pylint_rpn_final.txt`](pylint_rpn_final.txt).

### Recomendaciones no aplicadas

**Ninguna:** no se desactivaron reglas con `# pylint: disable=…`; las observaciones de la primera corrida se abordaron con cambios de código o refactor.

---

## 5. Black y Ruff (`pyproject.toml`)

### Instalación y versiones (evitar PATH)

```text
python -m pip install -U black ruff
py -3 -m black --version
py -3 -m ruff --version
```

Ejemplo de salida: **Black 26.3.1**, **Ruff 0.15.10** (las versiones concretas dependen de la fecha de `pip install -U`). Usar `py -3 -m black` y `py -3 -m ruff` evita depender de que `Scripts` esté en el PATH en Windows.

### Archivo [`pyproject.toml`](../pyproject.toml) — significado de la configuración

| Clave | Significado |
|-------|-------------|
| **`[tool.black]`** | Ajustes del formateador **Black** (estilo unificado, opinionado). |
| **`line-length = 88`** | Máximo de caracteres por línea antes de partir expresiones (convención habitual con Black, compatible con muchos editores). |
| **`target-version = ["py311"]`** | Black asume sintaxis y reglas de **Python 3.11** al reformatear (no cambia la versión del intérprete, solo cómo escribe el código). |
| **`[tool.ruff]`** | Configuración global de **Ruff** (sustituto rápido de flake8 + isort + muchas reglas). |
| **`target-version = "py311"`** | Ruff aplica reglas y sugerencias (`UP`, etc.) coherentes con **Python 3.11**. |
| **`[tool.ruff.lint]`** | En Ruff ≥ 0.2, reglas de lint van en esta subsección (equivalente a `select`/`ignore` de nivel superior en versiones antiguas). |
| **`select = ["E", "F", "I", "B", "UP"]`** | Conjuntos de reglas activados: **E** (pycodestyle errores), **F** (Pyflakes: imports, nombres, etc.), **I** (isort: orden de imports), **B** (flake8-bugbear: patrones propensos a bugs), **UP** (pyupgrade: sintaxis moderna). |
| **`ignore = []`** | Ninguna regla desactivada explícitamente (lista vacía = no se ignoran códigos). |

*Nota:* La consigna pedía `select`/`ignore` bajo `[tool.ruff]`; con **Ruff 0.15** las advertencias deprecan esa forma en favor de `[tool.ruff.lint]`, que es **equivalente** y deja la salida sin avisos.

### Comandos usados en este proyecto

Desde `src/chatGPT/`:

```text
py -3 -m black --check --diff rpn.py
py -3 -m black rpn.py
py -3 -m ruff check rpn.py
```

- **`black --check --diff`:** no modifica archivos; falla si el formato difiere y muestra el diff unificado.
- **`black rpn.py`:** aplica el formato (p. ej. línea en blanco tras docstring del módulo).
- **`ruff check`:** ejecuta el linter según `select`; **`ruff check --fix`** puede corregir automáticamente algunos hallazgos.

Tras iterar, **Black** y **Ruff** no reportan observaciones sobre `rpn.py`.

---

## 6. Mejoras sugeridas (revisión tipo ChatGPT) e implementación

A partir de una revisión del código ya funcional, se adoptaron mejoras que **no cambian el comportamiento** observable en los tests:

- **`from __future__ import annotations`:** permite anotaciones de tipo más legibles y posponer la evaluación de tipos (PEP 563).
- **Anotaciones de tipo** en funciones y variables (`evaluate(expr: str) -> float`, pilas `list[float]`, memorias `dict[str, float]`, `Final[...]` en constantes).
- **`Callable` tipado** para `_TR` y `_ARC` (menos ambigüedad que `dict` genérico).
- **Expresiones regulares precompiladas** (`_RE_SLOT`, `_RE_STO_RCL_COMPACT`) para evitar recompilar el mismo patrón en cada token.
- **Salida de error:** `print(err, file=sys.stderr)` en lugar de `print(str(err), …)`.
- **Dominio de `asin`/`acos`:** condición explícita `a < -1.0 or a > 1.0` (equivalente a la cadena de comparaciones anterior, más clara para linters).

No se implementaron cambios que alteren la interfaz pública (`evaluate`, `main`, `RPNError`) ni el protocolo de línea de comandos.

---

## 7. Multimetric sobre `rpn.py`

**Memoria de resultados:** los valores obtenidos en la ejecución de multimetric (comando, fecha, tabla `overall` y lectura breve) están en [`MEMORIA_MULTIMETRIC_RPN.md`](MEMORIA_MULTIMETRIC_RPN.md). Los datos consolidados y la salida JSON completa: [`multimetric_rpn.json`](multimetric_rpn.json) y [`multimetric_rpn_full_output.json`](multimetric_rpn_full_output.json).

En **Windows**, si `py -3 -m multimetric` falla por `multiprocessing` (p. ej. Python 3.14), usar el ejecutable instalado:

```text
"%LocalAppData%\Programs\Python\Python314\Scripts\multimetric.exe" src\chatGPT\rpn.py --jobs 1
```

### a) `comment_ratio` (Overall)

- En la corrida registrada en la memoria (2026-03-29), tras añadir **bloques `#` por sección** en `rpn.py`: **comment_ratio ≈ 34,876** (≥ **33 %** ≈ 1/3, según multimetric).
- Conviene **regenerar** multimetric tras cada cambio sustancial y actualizar [`MEMORIA_MULTIMETRIC_RPN.md`](MEMORIA_MULTIMETRIC_RPN.md).

### b) `halstead_effort` y `halstead_timerequired` — significado y comparación con el tiempo real

- **Halstead “effort” (E)**: estimación del esfuerzo cognitivo para comprender/escribir el código a partir del volumen y la dificultad (métrica de Halstead).
- **Halstead “time required” (T)**: suele derivarse como \(T \approx E / S\) con \(S\) en el orden de **18** segundos en la interpretación clásica (segundos de comprensión estimados, **no** tiempo de CPU).
- **Comparación con tu tiempo real**: anotá cuántos **minutos u horas** dedicaste a diseño, codificación y depuración **después** de tener una primera versión ejecutable. Es normal que el tiempo humano no coincida con \(T\): Halstead mide un **modelo abstracto**, no calendario real.

### c) `halstead_bugprop` vs defectos reales (post–primera ejecución correcta)

- **Bugprop** propone un **número esperado de errores** a partir del volumen Halstead (heurística).
- Los **bugs que corriste vos** (lógica, casos borde, tests) pueden ser **mayores o menores** que ese número: la métrica no predice tu proceso concreto.
- En este proyecto, ejemplos típicos fuera de sintaxis: orden RPN en `/`, `STO`/`RCL` y tokens compactos; conviene **listar** en la entrega cuántos defectos lógicos corregiste a mano.

### d) Reducir **McCabe** (`cyclomatic_complexity`) en ~10 %

Valor de referencia en la corrida de la memoria (2026-03-29): **35**. Un 10 % menos ≈ **31,5** (referencia orientativa; el valor exacto depende del análisis de multimetric sobre el archivo actual).

Estrategias aplicables (sin cambiar el comportamiento):

1. **Extraer** bloques de `evaluate` a funciones pequeñas (`_apply_binario`, `_apply_unario`, `_mem_sto`, etc.) para que cada función tenga menos ramas visibles en un solo grafo.
2. **Tabla de despacho**: diccionario `nombre_token → función` en lugar de una larga cadena `elif`.
3. **Unificar** casos similares (`log`/`ln`, `ex`/`10x`) en un solo manejador parametrizado.
4. **Tests** que permitan refactor con confianza (ya hay cobertura alta).

## Referencias rápidas

| Métrica (Overall — memoria 2026-03-29) | Valor |
|----------------------------------------|------:|
| comment_ratio                          | ~34,88 |
| cyclomatic_complexity                  | 35 |
| halstead_effort                        | ~976 993 |
| halstead_timerequired                  | ~54 277 |
| halstead_bugprop                       | ~3,43 |
| loc                                    | 227 |

*Actualizar la tabla si regenerás multimetric sobre una versión nueva de `rpn.py`; ver siempre [`MEMORIA_MULTIMETRIC_RPN.md`](MEMORIA_MULTIMETRIC_RPN.md).*
