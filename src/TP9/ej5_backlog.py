# TP9 - Ejercicio 5
# priorizacion por hits/SP, velocidad 5 SP/sprint (2 semanas)

from dataclasses import dataclass

@dataclass
class Feature:
    name: str
    sp: int
    hits: int

    @property
    def value_density(self):
        return self.hits / self.sp

features = [
    Feature("A", 2, 1104),
    Feature("B", 3, 1762),
    Feature("C", 8, 6602),
    Feature("D", 5, 1565),
    Feature("F", 2, 2179),
    Feature("G", 13, 8030),
]

def capacidad_sp(semanas, velocidad=5, deuda_tecnica=0):
    sprints = semanas / 2
    return sprints * max(velocidad - deuda_tecnica, 0)

def seleccionar(features, presupuesto_sp, forzar=None):
    forzar = forzar or []
    elegidas = []
    restantes = []
    usado = 0

    forzadas = [f for f in features if f.name in forzar]
    otras = [f for f in features if f.name not in forzar]
    otras = sorted(otras, key=lambda f: f.value_density, reverse=True)

    for f in forzadas + otras:
        if usado + f.sp <= presupuesto_sp + 1e-9:
            elegidas.append(f)
            usado += f.sp
        else:
            restantes.append(f)
    return elegidas, restantes, usado

def reportar(titulo, elegidas, restantes, usado, presupuesto):
    print("=" * 60)
    print(titulo)
    print(f"Presupuesto SP: {presupuesto:.1f} | Usados: {usado}")
    print("Incluidas:", ", ".join(f"{f.name}({f.sp})" for f in elegidas) or "(ninguna)")
    print("Fuera:    ", ", ".join(f"{f.name}({f.sp})" for f in restantes) or "(ninguna)")

print("Ranking hits/SP:")
for f in sorted(features, key=lambda x: x.value_density, reverse=True):
    print(f"  Funcion {f.name}: {f.value_density:.2f}")

# 1) 6 semanas = 15 SP
cap6 = capacidad_sp(6)
e, r, u = seleccionar(features, cap6)
reportar("1) 6 semanas (15 SP)", e, r, u, cap6)

# 2) presupuesto a la mitad ~= 7.5 SP
cap_mitad = capacidad_sp(3)
e2, r2, u2 = seleccionar(features, cap_mitad)
reportar("2) presupuesto a la mitad (7.5 SP)", e2, r2, u2, cap_mitad)

e2b, r2b, u2b = seleccionar(features, 5)
reportar("2-bis) si es 1 sprint (5 SP)", e2b, r2b, u2b, 5)

# 3) 7 semanas = 17.5 SP
cap7 = capacidad_sp(7)
e3, r3, u3 = seleccionar(features, cap7)
reportar("3) 7 semanas (17.5 SP)", e3, r3, u3, cap7)

# 4) D por arquitectura
print("=" * 60)
print("4) Prioridad de D (arquitectura)")
d = next(f for f in features if f.name == "D")
print(f"Densidad de D = {d.value_density:.2f} (baja en valor de uso)")
print("Conviene priorizarla como enabler tecnico, no por hits.")
e4, r4, u4 = seleccionar(features, cap6, forzar=["D"])
reportar("4) 6 semanas forzando D", e4, r4, u4, cap6)

# 5) deuda tecnica 1 SP/sprint -> velocidad neta 4
cap6_dt = capacidad_sp(6, deuda_tecnica=1)
e5, r5, u5 = seleccionar(features, cap6_dt)
reportar("5) 6 semanas con deuda tecnica (12 SP)", e5, r5, u5, cap6_dt)

cap_mitad_dt = capacidad_sp(3, deuda_tecnica=1)
e5m, r5m, u5m = seleccionar(features, cap_mitad_dt)
reportar("5) mitad presupuesto con deuda (6 SP)", e5m, r5m, u5m, cap_mitad_dt)

cap7_dt = capacidad_sp(7, deuda_tecnica=1)
e5s, r5s, u5s = seleccionar(features, cap7_dt)
reportar("5) 7 semanas con deuda (14 SP)", e5s, r5s, u5s, cap7_dt)

e5d, r5d, u5d = seleccionar(features, cap6_dt, forzar=["D"])
reportar("5) 6 semanas deuda + forzando D", e5d, r5d, u5d, cap6_dt)
