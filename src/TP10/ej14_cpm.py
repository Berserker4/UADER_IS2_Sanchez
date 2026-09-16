#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* TP10 - Ejercicio 14: CPM recursos infinitos y staff=2
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
"""Red de actividades: CPM y leveling con 2 personas."""

from __future__ import annotations

from collections import defaultdict

from pathlib import Path

import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent

TASKS = {
    "A": {"dur": 5, "preds": []},
    "B": {"dur": 3, "preds": ["A"]},
    "C": {"dur": 10, "preds": ["A"]},
    "D": {"dur": 20, "preds": ["A"]},
    "E": {"dur": 5, "preds": ["B", "C"]},
    "F": {"dur": 6, "preds": ["B", "C"]},
    "G": {"dur": 7, "preds": ["B", "C"]},
    "H": {"dur": 10, "preds": ["E", "F", "D"]},
    "I": {"dur": 9, "preds": ["G", "D"]},
    "J": {"dur": 12, "preds": ["H", "I"]},
}


def successors(tasks: dict) -> dict:
    succs = defaultdict(list)
    for name, data in tasks.items():
        for p in data["preds"]:
            succs[p].append(name)
    return succs


def topo_order(tasks: dict) -> list:
    remaining = {k: set(v["preds"]) for k, v in tasks.items()}
    ready = [k for k, preds in remaining.items() if not preds]
    order = []
    while ready:
        ready.sort()
        n = ready.pop(0)
        order.append(n)
        for m, preds in remaining.items():
            if n in preds:
                preds.remove(n)
                if not preds and m not in order and m not in ready:
                    ready.append(m)
    return order


def cpm_infinite(tasks: dict) -> dict:
    order = topo_order(tasks)
    es, ef = {}, {}
    for n in order:
        es[n] = max((ef[p] for p in tasks[n]["preds"]), default=0)
        ef[n] = es[n] + tasks[n]["dur"]
    t_end = max(ef.values())
    succs = successors(tasks)
    lf, ls = {}, {}
    for n in reversed(order):
        lf[n] = min((ls[s] for s in succs[n]), default=t_end)
        ls[n] = lf[n] - tasks[n]["dur"]
    slack = {n: ls[n] - es[n] for n in order}
    critical = [n for n in order if abs(slack[n]) < 1e-9]
    return {
        "order": order,
        "ES": es,
        "EF": ef,
        "LS": ls,
        "LF": lf,
        "slack": slack,
        "duration": t_end,
        "critical": critical,
        "succs": succs,
    }


def schedule_staff(tasks: dict, staff: int = 2, ls_priority: dict | None = None) -> dict:
    """List scheduling: prioridad por LS (CPM) y luego mayor duracion."""
    succs = successors(tasks)
    unfinished = set(tasks)
    done_time = {}
    running = {}
    schedule = {}
    t = 0

    def rem_path(tk: str) -> int:
        memo = {}

        def dfs(u: str) -> int:
            if u in memo:
                return memo[u]
            kids = succs[u]
            memo[u] = tasks[u]["dur"] + (max(dfs(s) for s in kids) if kids else 0)
            return memo[u]

        return dfs(tk)

    while unfinished or running:
        for tk, ft in list(running.items()):
            if ft <= t:
                done_time[tk] = running.pop(tk)
                unfinished.discard(tk)

        eligible = [
            tk
            for tk in unfinished
            if tk not in running and all(p in done_time for p in tasks[tk]["preds"])
        ]

        def prio(tk: str):
            ls = ls_priority[tk] if ls_priority else 0
            return (ls, -rem_path(tk), -tasks[tk]["dur"], tk)

        eligible.sort(key=prio)
        free = staff - len(running)
        for tk in eligible:
            if free <= 0:
                break
            schedule[tk] = (t, t + tasks[tk]["dur"])
            running[tk] = t + tasks[tk]["dur"]
            free -= 1

        if not running:
            break
        t = min(running.values())

    duration = max(ft for _, ft in schedule.values())
    return {"schedule": schedule, "duration": duration}


def plot_gantt(schedule: dict, critical: set, out: str, title: str) -> None:
    names = sorted(schedule.keys(), key=lambda n: (schedule[n][0], n))
    fig, ax = plt.subplots(figsize=(11, 5))
    for i, name in enumerate(names):
        start, finish = schedule[name]
        color = "#8b1e1e" if name in critical else "#1f4e79"
        ax.barh(i, finish - start, left=start, height=0.6, color=color, edgecolor="black")
        ax.text(start + (finish - start) / 2, i, name, ha="center", va="center", color="white", fontsize=9)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel("Tiempo")
    ax.set_title(title)
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"Grafico: {out}")


def main() -> None:
    cpm = cpm_infinite(TASKS)
    print("=== a) Recursos infinitos ===")
    print(f"Duracion total: {cpm['duration']}")
    print(f"Camino critico: {' -> '.join(cpm['critical'])}")
    for n in cpm["order"]:
        print(
            f"  {n}: ES={cpm['ES'][n]} EF={cpm['EF'][n]} "
            f"LS={cpm['LS'][n]} LF={cpm['LF'][n]} slack={cpm['slack'][n]}"
        )

    sch_inf = {n: (cpm["ES"][n], cpm["EF"][n]) for n in cpm["order"]}
    plot_gantt(
        sch_inf,
        set(cpm["critical"]),
        str(OUT_DIR / "ej14_gantt_infinito.png"),
        f"CPM recursos infinitos (D={cpm['duration']}) - critico en rojo",
    )

    rc = schedule_staff(TASKS, staff=2, ls_priority=cpm["LS"])
    print("=== b) Staff = 2 personas ===")
    print(f"Duracion total: {rc['duration']}")
    for n in cpm["order"]:
        s, f = rc["schedule"][n]
        print(f"  {n}: {s} -> {f}")

    # Cadena critica observada en el leveling (sin holgura de recurso)
    # A-C-B-G-F-H-J = 53
    crit2 = {"A", "C", "B", "G", "F", "H", "J"}
    print(f"Nuevo camino critico (recursos): {' -> '.join(['A','C','B','G','F','H','J'])}")
    plot_gantt(
        rc["schedule"],
        crit2,
        str(OUT_DIR / "ej14_gantt_staff2.png"),
        f"Leveling staff=2 (D={rc['duration']}) - critico en rojo",
    )


if __name__ == "__main__":
    main()
