# TP10 - Administracion de proyectos (Gestion)
## Ingenieria de Software II - Resolucion

---

### 1. VPN, rentabilidad y gestion profesional (Jupyter)

Parametros: costo 1000/mes vencido, beneficio VP=18000 al entregar, r=1% mensual.

VPN = VP(beneficio) - VP(inversion)
Rentabilidad = VPN / VP(inversion)

Archivos: ej1_vpn.ipynb, ej1_vpn.py

| Caso | Meses | Costo/mes | VP inversion | VPN | Rentabilidad |
|------|------:|----------:|-------------:|----:|-------------:|
| a) Plan | 12 | 1000 | 11255.08 | **4719.01** | **41.93%** |
| b) Extension +3m | 15 | 1000 | 13865.05 | **1639.24** | **11.82%** |
| d) Retraso +6m | 18 | 1000 | 16398.27 | **-1349.96** | **-8.23%** |
| e) PM +5% a tiempo | 12 | 1050 | 11817.83 | **4156.25** | **35.17%** |

#### 1.c Rentabilidades
Plan: 41.93%. Extension 15 meses: 11.82%.

#### 1.d Impacto del retraso de 6 meses
Ademas de alargar el desembolso, posterga el cobro del beneficio. El VPN pasa de +4719 a **-1350** (proyecto que destruye valor). Incluso el retraso de 3 meses ya reduce la rentabilidad a menos de un tercio.

#### 1.e Conveniencia de gestion profesional (+5%)
VPN con PM = 4156.25 > VPN con demora de 3 meses = 1639.24.
Desde una mirada puramente financiera **conviene** pagar el 5% extra: se preserva casi todo el valor del plan y se evita la perdida por demora.

#### 1.f Desafio (15 meses, mismo VPN del plan)
Costo mensual maximo aceptable: **777.88**
(asi VPN_15 = VPN_plan = 4719.01).

---

### 2. Equilibrio financiero proveedor / patrocinante

Base: costo 1000/mes x 12, pago 14000 en mes 12, r=1%.
NPV equilibrio del proveedor = 1169.21

Archivo: ej2_equilibrio.py

#### 2.a Pago en mes 14 (neutro)
P = 14000 * (1.01)^2 = **14281.40**

#### 2.b Entrega mes 6, pago mes 12 (neutro al proveedor)
Al acortar costos a 6 meses el proveedor ahorra esfuerzo; el pago que mantiene el mismo NPV es **7847.98**

#### 2.c Entrega y pago en mes 6 (mismo equilibrio)
P = **7393.16**
(menor que 2.b porque el pago anticipado tiene mas valor presente; hace falta menos nominal).

---

### 3. Por que D = Esfuerzo / (Horas-dia/persona) * 1/Staff solo vale para equipo unipersonal?

Porque supone que el esfuerzo se divide linealmente al agregar personas (productividad perfecta, sin comunicacion ni particion). Con N>1 aparecen overhead de comunicacion, acoplamiento de tareas e indivisibilidades: el tiempo calendario no baja como 1/Staff. Solo con Staff=1 la formula es exacta.

---

### 4. Por que tau_proyecto = sum tau_i solo vale en proyectos secuenciales triviales?

Porque suma todas las duraciones como si nada pudiera ejecutarse en paralelo. En una red real la duracion es el **camino critico** (el mas largo), no la suma total. Con dependencias y paralelismo, sum(tau_i) sobrestima el calendario.

---

### 5. Retrasar una tarea del camino critico (margen=0) retrasa el proyecto

El camino critico es la cadena mas larga. Margen=0 significa que no hay holgura: cualquier atraso de esa tarea empuja el inicio de sus sucesoras criticas y, en cascada, la fecha de fin del proyecto. No hay buffer que absorba el desvio.

---

### 6. No conviene agregar recursos a una actividad con margen != 0

Acelerar una tarea con holgura no reduce la fecha de fin (el critico no cambia) y si consume recursos, costo y atencion de gestion. Esas personas conviene asignarlas a tareas criticas o a reduccion de riesgo real del camino critico.

---

### 7. Reducir el calendario 50% solo con crashing: viable?

En general **no**. El crashing tiene rendimientos decrecientes (ley de Brooks / costos crecientes de compresion). Comprimir un 50% suele ser imposible o ruinoso: mas gente no implica mitad de tiempo, y el critico tiene un limite fisico de paralelizacion. Solo seria imaginable en proyectos muy secuenciales triviales con holgura enorme, que no es el caso tipico.

---

### 8. Calendario agresivo y consigna de "cero cambios": alcanza?

**No alcanza por si sola.** Cero cambios ayuda a congelar alcance, pero un calendario muy agresivo suele fallar por estimacion, riesgo tecnico, dependencias y productividad. Sin buffer de riesgo, calidad y capacidad real, la consigna solo traslada la presion al equipo; no elimina la incertidumbre.

---

### 9. Contingencia por sismos en Concepcion del Uruguay (UADER)?

En gestion de riesgos se prioriza por **probabilidad x impacto** (y detectabilidad). Entre Rios / Concepcion del Uruguay no es zona de amenaza sismica relevante frente a otros riesgos locales (inundaciones, cortes de energia, enfermedad, ausentismo). Un plan de contingencia sismico especifico no se justifica por el marco de exposicion; conviene reservar contingencia para riesgos con probabilidad/impacto materiales en ese contexto.

---

### 10. Por que transferir un riesgo en vez de mitigarlo?

Cuando el costo o la capacidad interna de mitigarlo superan el beneficio, o cuando un tercero esta mejor posicionado (seguro, outsourcing, contrato con clausulas). Transferir mueve el impacto economico a quien puede absorberlo mas eficientemente.

---

### 11. Controlar el trabajo del equipo, no a los individuos

El entregable y el flujo de valor son del sistema (equipo/proceso). Controlar personas genera micromanagement, distorsiona incentivos y no garantiza el resultado colectivo. Controlar el trabajo (avances, burndown, calidad, impedimentos) alinea al objetivo del proyecto.

---

### 12. GitHub vs gestion de configuracion (CM)

| Necesidad tipica de CM | GitHub | Cumple? | Justificacion |
|------------------------|--------|---------|---------------|
| Control de versiones | Git repos | Si | Historial, branches, tags |
| Identificacion de baselines | Releases/Tags | Si | Versionado de entregables |
| Control de cambios | Pull Requests + Reviews | Parcial/Si | Flujo de aprobacion; politicas según plan |
| Trazabilidad req-cambio-codigo | Issues + PR links + Projects | Parcial | Hay vinculos, pero no es ALM completo tipo DOORS |
| Build/CI reproducible | Actions | Si | Pipelines de build/test |
| Artefactos binarios | Packages / Releases | Parcial/Si | Suficiente para muchos equipos |
| Control de acceso / auditoria | Permissions, audit log | Si | Roles y registro de eventos |
| CM de entornos/infra | limitado nativo | Parcial | Se complementa con IaC externo |

Conclusion: GitHub cubre bien el nucleo de CM de codigo y cambios; para CM integral de producto/entornos suele hacer falta complementarlo (wiki/docs, IaC, tool de requisitos).

---

### 13. Fabrica de software vs equipo convencional de proyecto

- **Fabrica:** orientada a capacidad estable, estandarizacion de procesos, especializacion por rol/cola de trabajo, metricas de throughput, multiples pedidos/proyectos concurrentes.
- **Equipo de proyecto:** equipo temporal alineado a un objetivo unico, ownership de punta a punta, mayor acoplamiento al dominio del patrocinante y al ciclo de vida de ese proyecto.

---

### 14. Red de actividades (CPM)

Archivo: ej14_cpm.py
Graficos: ej14_gantt_infinito.png, ej14_gantt_staff2.png

#### 14.a Recursos infinitos
Duracion total: **47**
Camino critico: **A -> D -> H -> J** (5+20+10+12)

| Tarea | ES | EF | LS | LF | Slack |
|-------|---:|---:|---:|---:|------:|
| A | 0 | 5 | 0 | 5 | 0 |
| B | 5 | 8 | 16 | 19 | 11 |
| C | 5 | 15 | 9 | 19 | 4 |
| D | 5 | 25 | 5 | 25 | 0 |
| E | 15 | 20 | 20 | 25 | 5 |
| F | 15 | 21 | 19 | 25 | 4 |
| G | 15 | 22 | 19 | 26 | 4 |
| H | 25 | 35 | 25 | 35 | 0 |
| I | 25 | 34 | 26 | 35 | 1 |
| J | 35 | 47 | 35 | 47 | 0 |

#### 14.b Staff = 2 personas (1 persona/tarea, indivisible)
Duracion total: **53**
Nuevo camino critico (cadena que demora el fin bajo leveling): **A -> C -> B -> G -> F -> H -> J**

Agenda resultante:
- A: 0-5
- C y D: 5-15 / 5-25 (las 2 personas)
- B: 15-18 (con D)
- G: 18-25 (con D)
- E: 25-30 ; F: 25-31
- I: 30-39 ; H: 31-41
- J: 41-53

La restriccion de recursos alarga 6 unidades respecto del CPM ideal (47 -> 53) porque B/C/D/E/F/G compiten por solo 2 slots.

---

## Checklist vs enunciado

| Punto | Estado |
|-------|--------|
| 1a VPN plan | OK: 4719.01 |
| 1b VPN +3m | OK: 1639.24 |
| 1c rentabilidades | OK: 41.93% / 11.82% |
| 1d impacto retraso 6m | OK: VPN negativo |
| 1e PM +5% | OK: conviene vs demora |
| 1f desafio costo max | OK: 777.88 |
| 2a pago mes 14 | OK: 14281.40 |
| 2b entrega 6 / pago 12 | OK: 7847.98 |
| 2c entrega y pago 6 | OK: 7393.16 |
| 3 formula unipersonal | OK |
| 4 suma secuencial | OK |
| 5 camino critico | OK |
| 6 margen != 0 | OK |
| 7 crashing 50% | OK: no viable |
| 8 cero cambios | OK: no alcanza |
| 9 sismos CDU | OK: no priorizar |
| 10 transferir riesgo | OK |
| 11 controlar trabajo | OK |
| 12 tabla GitHub CM | OK |
| 13 fabrica vs proyecto | OK |
| 14a CPM infinito | OK: 47, A-D-H-J |
| 14b staff 2 | OK: 53, A-C-B-G-F-H-J |
