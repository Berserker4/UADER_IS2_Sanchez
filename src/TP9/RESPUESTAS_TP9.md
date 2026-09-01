# TP9 - Administracion de proyectos (Planificacion)
## Ingenieria de Software II - Resolucion

---

### 1. Puede el mantenimiento continuo considerarse un proyecto?

No de forma automatica. Un proyecto tiene inicio y fin definidos, objetivo unico y recursos acotados. El mantenimiento continuo (indefinido, rutinario) es una operacion permanente, no un proyecto.

Para tratarlo como proyecto hay que asignarle:
- Alcance acotado (un release, un lote de tickets, una migracion).
- Inicio y fin claros.
- Objetivo medible.
- Presupuesto y equipo asignados a ese tramo.
- Entregables y criterios de aceptacion.

Sin esos limites, sigue siendo operacion/servicio.

---

### 2. Por que ciertas iniciativas se estructuran como programas y no como proyectos?

Porque el objetivo es estrategico y de largo plazo, compuesto por varios proyectos relacionados que por si solos no entregan el beneficio completo. Un programa coordina interdependencias y beneficios acumulados; un proyecto entrega un resultado concreto y acotado. Ejemplo: "transformacion digital" (programa) vs "migrar el modulo de facturacion" (proyecto).

---

### 3. Efecto de fijar arbitrariamente Tiempo, Recursos y Requerimientos

El tetragono Tiempo-Costo-Alcance-Calidad es un sistema de trade-offs. Si se fijan tres parametros a valores comodos sin holgura, la unica variable que absorbe el desajuste es la calidad (mas defectos, deuda tecnica, retrabajo) o el proyecto se vuelve inviable.

En la practica: estimaciones irreales, overtime, recortes ocultos de calidad y alto riesgo de fracaso.

---

### 4. Script Python / Jupyter - esfuerzo y tiempo calendario

Relaciones:

E = 8 * S^0.95

td = 2.4 * E^0.33

Archivos:
- ej4_esfuerzo_calendario.ipynb
- ej4_esfuerzo_calendario.py
- Graficos: ej4_esfuerzo_vs_tamano.png, ej4_td_vs_esfuerzo.png

Ejemplo: para S=1000 -> E ~= 5663.57, td ~= 41.57.

---

### 5. Backlog, velocidad y alcance

Datos: velocidad 5 SP/sprint, sprint = 2 semanas.

| Funcion | SP | Hits | Densidad (Hits/SP) |
|---------|----|------|--------------------:|
| F | 2 | 2179 | 1089.5 |
| C | 8 | 6602 | 825.3 |
| G | 13 | 8030 | 617.7 |
| B | 3 | 1762 | 587.3 |
| A | 2 | 1104 | 552.0 |
| D | 5 | 1565 | 313.0 |

Criterio: maximizar hits/SP dentro de la capacidad.

Criterio verificado por busqueda exhaustiva (mochila 0-1 maximizando Hits).

#### 5.1 Con 6 semanas (3 sprints x 5 = 15 SP)
Incluir: F, C, B, A (15 SP, 11647 hits). Fuera: G, D.

#### 5.2 Presupuesto a la mitad (~3 semanas = 7.5 SP)
Incluir: F, B, A (7 SP).
Respecto al alcance de 5.1, se elimina C (la mas grande que entraba antes). G y D siguen fuera.
Si se interpreta como 1 sprint (5 SP): F y B.

#### 5.3 Equipo 7 semanas (3.5 sprints = 17.5 SP)
Optimo sigue siendo F, C, B, A (15 SP). Los 2.5 SP libres no alcanzan para meter D (5) ni G (13). El alcance no cambia vs 5.1.

#### 5.4 Prioridad de D (arquitectura / lider tecnico)
Por Hits/SP, D es la peor (313). Igual, como enabler de arquitectura conviene prioridad tecnica alta (no por valor de uso).
Si se fuerza D en 6 semanas: D, F, C (15 SP); se sacrifican B y A.

#### 5.5 Deuda tecnica = 1 SP/sprint => velocidad neta 4 SP/sprint
Se modifica todo lo anterior:
- 6 semanas: 12 SP -> F, C, A (se cae B respecto a 5.1)
- presupuesto a la mitad (~6 SP): F, B
- 7 semanas: 14 SP -> F, C, B
- forzando D en 6 semanas (12 SP): D, F, B, A (se cae C)

Script: ej5_backlog.py

---

### 6. Resumen - Harrison, "What Do Software Developers Need to Know about Business?"

Harrison critica la idea de que un desarrollador inteligente puede aprender negocio de oidas. El conocimiento de negocio (costos, valor, trade-offs economicos, gestion) es una disciplina con profundidad propia; tratarlo como trivial es ignorancia del campo.

Relevancia al alcance: el alcance no es solo una lista de funciones tecnicas, es una decision de negocio (que valor entregar con recursos limitados). Sin criterio economico se prioriza mal el backlog y se fija mal el trade-off del ej. 3.

---

### 7. Resumen - Colla, "Subjective Consistency"

Ante falta de datos historicos o actividades poco modelables, la estimacion cae en juicio de expertos, que es subjetivo. Colla propone usar comparaciones pareadas (adaptacion de AHP de Saaty) para medir la consistencia de esas opiniones (Consistency Ratio).

Relevancia a estimacion: complementa modelos estadisticos (ej. 8-9). Cuando el modelo no aplica, el experto sigue siendo util si se controla su consistencia.

---

### 8. Modelo PNR (dinamico)

Archivo: `PNR_sistemis.py` (basado en el del taller, dataset historico original)

Dataset calibracion del taller:
- t = 1..10 meses
- p(t) = 8, 21, 25, 30, 25, 24, 17, 15, 11, 6
- K historico = 182 PM
- a calibrado ~= 0.02957

Modelo:
- p(t) = 2 K a t exp(-a t^2)
- E(t) = K (1 - exp(-a t^2))

Uso:
```
python PNR_sistemis.py -k 72 -o ej8_pnr_72.png
python PNR_sistemis.py -k 72 -a 4 -o ej8_pnr_a4.png
```

8.a) Acepta K en PM (-k), grafica datos historicos, modelo de mejor ajuste y curva PNR del proyecto.

8.b) Para K=72 PM (ej8_pnr_72.png):
- Pico aprox t=4.11 meses, pmax ~= 10.6 personas
- Diferencias: los puntos historicos corresponden a un proyecto mas grande (K=182). El modelo calibrado suaviza esos puntos. La curva del proyecto K=72 tiene la misma forma (mismo a) pero menor amplitud: misma dinamica temporal, menos gente en cada mes.

8.c) Con a x4 (ej8_pnr_a4.png):
- Pico se adelanta a t ~= 2.06 meses y pmax sube a ~= 21.2 (casi el doble)
- Efecto: se exige mucho mas staff en menos tiempo
- Zona imposible: el calendario queda demasiado comprimido para el esfuerzo; el equipo no puede crecer/absorber tanta gente a tiempo y el plan tiende a fallar

Backup del original del taller: `PNR_sistemis_original.py`

---

### 9. Modelo estatico de esfuerzo

Archivo: `EffortModel.py` (basado en el del taller, dataset del enunciado TP9)

```
python EffortModel.py --both -o ej9_comparacion.png
python EffortModel.py --both -e 9100 -o ej9_loc_9100.png
python EffortModel.py --both -e 200 -o ej9_loc_200.png
```

9.a) Modelos:
| Modelo | Expresion | R2 |
|--------|-----------|-----|
| Lineal | E = -3.266667 + 0.002939*LOC | 0.9726 |
| Exponencial (potencia, como el taller) | E = 0.000368 * (LOC^1.207561) | **0.9757** |

Mejor por R2: **exponencial**.

9.b) LOC=9100 (dentro de rango): E ~= **22.24 PM**. Grafico: ej9_loc_9100.png

9.c) LOC=200 (fuera de rango): E ~= **0.22 PM**.
Precaucion: LOC=200 esta muy por debajo del minimo historico (1000). La extrapolacion no es confiable; el modelo no tiene evidencia en esa zona. Conviene no usarlo solo ahi.

Backup del original: `EffortModel_original.py`
---

### 10. Por que etapas/fases con go/no-go aumentan el valor para el patrocinante?

Porque introduce una opcion real: se puede abandonar o pivotar si el riesgo no justifica seguir, limitando la perdida al costo de las fases ya hechas. Sin etapas se compromete todo de una vez. Menos riesgo => mayor valor esperado para quien lo financia.

---

### 11. La contabilidad captura las acciones financieras (criterio del devengado)?

Si, en el sentido contable: bajo devengado registra hechos economicos cuando se generan (no cuando se cobra/paga).
Pero eso no alcanza para la decision de inversion: el valor se analiza con flujos de fondos, VAN/VPN y costo de oportunidad.

---

### 12. Promocion impositiva y apalancamiento impositivo

Desalienta el apalancamiento impositivo via deuda. El escudo fiscal de los intereses vale tc * intereses. Si baja la alicuota efectiva por el regimen de promocion, baja el beneficio fiscal del endeudamiento.

---

### 13. Incertidumbre +/-30% vs contingencias +5%

No son lo mismo:
- +/-30% es la banda de error de la estimacion (cono de incertidumbre): se gestiona con rangos y reestimacion, no hinchando el presupuesto base.
- La contingencia (~5%) es una reserva para riesgos residuales identificados; no pretende cubrir toda la incertidumbre del estimador.

Poner +30% de contingencia sesgaria sistematicamente todos los proyectos.

---

### 14. Esperanza de apostar a color (ruleta con un cero verde)

Ruleta europea: 37 casillas (18 rojo, 18 negro, 1 verde). Apuesta $1000 a color (pago 1:1).

E[X] = (18/37)(+1000) + (19/37)(-1000) = -1000/37 ~= -$27.03

La esperanza es negativa (ventaja de la casa por el cero).

---

### 15. "Telar de los colores" - Pg y Pp con esperanza nula

Inversion $1000, ganancia prometida 7% => +70 si gana; si pierde se asume perdida del capital -1000.
Pg + Pp = 1 y E = 0:

70 Pg - 1000(1 - Pg) = 0 => Pg = 1000/1070 ~= 93.46%, Pp = 70/1070 ~= 6.54%

Hace falta ganar casi siempre para apenas empatar en esperanza.

---

### 16. Valor presente (r = 7% mensual, cobro $1000 en 1 ano)

Vp = 1000 / (1.07)^12 ~= $444.01

---

### 17. TEA implicita del ejercicio anterior (ej. 16)

En el ej. 16 la tasa mensual es r = 7%. La TEA es la tasa anual equivalente:

TEA = (1 + r)^12 - 1 = (1.07)^12 - 1

(1.07)^12 ~= 2.252192

TEA ~= 1.252192 = **125.22%**

Comprobacion: aplicar TEA una vez al ano da el mismo factor que capitalizar 7% durante 12 meses:
1000 / (1 + TEA) = 1000 / 2.252192 ~= 444.01 = Vp del ej. 16.

Nota sobre "Calcule la duracion del proyecto y el nuevo camino critico":
esa frase aparece al final del punto 17 en el PDF, pero **no hay red de actividades, duraciones ni precedencias** en el enunciado. Sin ese grafo/tabla no se puede calcular un camino critico. Si tenes otra hoja/imagen del TP con el diagrama, pasala y lo resolvemos.

---

## Checklist vs enunciado

| Punto | Estado |
|-------|--------|
| 1 teoria mantenimiento/proyecto | OK |
| 2 programas vs proyectos | OK |
| 3 fijar T+R+Req | OK |
| 4 Jupyter + graficos E y td | OK (ipynb + py + png) |
| 5.1 alcance 6 sem | OK: F,C,B,A |
| 5.2 mitad presupuesto | OK: elimina C |
| 5.3 7 semanas | OK: igual F,C,B,A |
| 5.4 prioridad D | OK: forzar como arquitectura |
| 5.5 deuda tecnica 1 SP | OK: recalcula 6/mitad/7/D |
| 6 resumen Harrison + relevancia alcance | OK |
| 7 resumen Colla + relevancia estimacion | OK |
| 8 PNR a/b/c con 72 PM y a x4 | OK con dataset del taller (K hist=182, a~=0.0296) |
| 9 lineal/exp, LOC 9100 y 200 | OK (mejor exponencial R2=0.9757; LOC9100~=22.24 PM) |
| 10 fases / valor opcion | OK |
| 11 contabilidad / devengado | OK |
| 12 apalancamiento impositivo | OK: desalienta |
| 13 contingencias 5% vs +/-30% | OK |
| 14 esperanza ruleta | OK: -27.03 |
| 15 Telar Pg/Pp | OK: 93.46% / 6.54% |
| 16 Vp | OK: 444.01 |
| 17 TEA | OK: 125.22% (camino critico falta en el PDF) |
