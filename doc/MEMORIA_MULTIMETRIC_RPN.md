# Memoria — Resultados de multimetric sobre `rpn.py`

Documento de registro de la ejecución del analizador **multimetric** sobre el programa entregable [`src/chatGPT/rpn.py`](../src/chatGPT/rpn.py).

## Metadatos de la corrida

| Campo | Valor |
|--------|--------|
| Fecha de la memoria | 2026-03-29 |
| Archivo analizado | `src/chatGPT/rpn.py` |
| Herramienta | multimetric (salida JSON `overall`) |
| Entorno | Windows; Python 3.14 |

## Comando utilizado

En PowerShell, desde la raíz del repositorio:

```text
"%LocalAppData%\Programs\Python\Python314\Scripts\multimetric.exe" src\chatGPT\rpn.py --jobs 1
```

*Motivo de `--jobs 1` y del ejecutable `.exe`:* en esta máquina, `py -3 -m multimetric` puede fallar por `multiprocessing` bajo Python 3.14; el binario en `Scripts` con un solo job evita el fallo.

## Resultados agregados (`overall`)

Valores obtenidos en la **última** corrida registrada (misma estructura que el campo `overall` del JSON de multimetric):

| Métrica | Valor |
|---------|------:|
| `loc` | 227 |
| `comment_ratio` | **34,876** |
| `cyclomatic_complexity` | 35 |
| `maintainability_index` | 27,022 |
| `halstead_volume` | 10292,884 |
| `halstead_difficulty` | 94,919 |
| `halstead_effort` | 976992,611 |
| `halstead_timerequired` | 54277,367 |
| `halstead_bugprop` | 3,431 |
| `operands_sum` / `operands_uniq` | 667 / 130 |
| `operators_sum` / `operators_uniq` | 727 / 37 |
| `fanout_external` / `fanout_internal` | 6 / 0 |
| `pylint` (puntuación integrada) | 100,0 |
| `tiobe` | 85,023 |
| Subíndices TIOBE (`tiobe_compiler`, `tiobe_coverage`, …) | 100,0 (cada uno en esta corrida) |
| `tiobe_complexity` | 0,154 |

### Consigna `comment_ratio` (≥ 1/3 ≈ 33 %)

La guía del TP pide que, si `comment_ratio` es **menor** que un tercio, se exploren medidas hasta situarse en ese entorno. Tras incorporar **bloques de comentarios `#` por sección** (estructura del módulo, pila, STO/RCL, operadores, trig, E/S), multimetric reporta **`comment_ratio` ≈ 34,9 %**, por encima del **33 %** de referencia, sin alterar la lógica ni los tests.

## Lectura breve

- **`loc`:** líneas de código contadas por la herramienta; sube respecto de versiones con menos comentarios.
- **`comment_ratio`:** proporción de líneas de comentario según multimetric; el valor cumple el umbral ~1/3 pedido en el práctico.
- **Complejidad ciclomática (35):** acorde a una calculadora con muchas ramas de operadores; se mitiga con funciones `_apply_*`.
- **Halstead / TIOBE:** referencia cuantitativa; regenerar tras cambios grandes al fuente.

## Archivo de datos

- [`multimetric_rpn.json`](multimetric_rpn.json) — metadatos de la corrida y bloque `salida_overall` (métricas agregadas).
- [`multimetric_rpn_full_output.json`](multimetric_rpn_full_output.json) — salida típica de multimetric con secciones `files` y `overall` (para auditoría o comparación con la consola).

---

*Esta memoria cumple el requisito de registrar los resultados obtenidos en la ejecución de multimetric.*
