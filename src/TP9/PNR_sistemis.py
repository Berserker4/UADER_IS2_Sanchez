#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* PNR_sistemis - modificado TP9
#* Modelos dinamicos Putnam-Norden-Rayleigh
#* Dataset del taller Modelos dinamicos
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
import numpy as np
import sys
import argparse
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# dataset historico del taller (esfuerzo instantaneo)
t_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
E_data = np.array([8, 21, 25, 30, 25, 24, 17, 15, 11, 6], dtype=float)
K_hist = float(np.sum(E_data))

def E_inst(t, K, a):
    return 2 * K * a * t * np.exp(-a * t**2)

def E_acum(t, K, a):
    return K * (1 - np.exp(-a * (t**2)))

def fit_modelo(t, e):
    # calibra a con K = suma del historico
    def modelo(tt, a):
        return E_inst(tt, K_hist, a)
    popt, _ = curve_fit(modelo, t, e, p0=[0.1])
    return float(popt[0])

def graficar(K, a, a_label, outfile):
    t = np.linspace(0.1, max(t_data) * 1.2, 300)

    # historico + modelo calibrado (K historico) + PNR del proyecto (K pedido)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    ax.scatter(t_data, E_data, color="#1f4e79", label="Datos historicos", zorder=3)
    ax.plot(t, E_inst(t, K_hist, a), "--", color="#2e7d32", label=f"Modelo ajuste a={a:.4f}")
    ax.plot(t, E_inst(t, K, a), color="#8b1e1e", linewidth=2, label=f"PNR proyecto K={K:.0f}")
    ax.set_xlabel("Tiempo (meses)")
    ax.set_ylabel("Esfuerzo instantaneo (personas)")
    ax.set_title("Esfuerzo instantaneo p(t)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    ax2 = axes[1]
    ax2.scatter(t_data, np.cumsum(E_data), color="#1f4e79", label="Historico acum.", zorder=3)
    ax2.plot(t, E_acum(t, K_hist, a), "--", color="#2e7d32", label="Modelo acum. calibrado")
    ax2.plot(t, E_acum(t, K, a), color="#8b1e1e", linewidth=2, label=f"PNR acum. K={K:.0f}")
    ax2.set_xlabel("Tiempo (meses)")
    ax2.set_ylabel("Esfuerzo acumulado (PM)")
    ax2.set_title("Esfuerzo acumulado E(t)")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8)

    fig.suptitle(f"PNR TP9 - K={K:.0f} PM | {a_label}")
    fig.tight_layout()
    fig.savefig(outfile, dpi=150)
    print(f"Grafico: {outfile}")
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--esfuerzo", type=float, default=72.0, help="Esfuerzo total PM")
    ap.add_argument("-a", "--amult", type=float, default=1.0, help="Multiplicador de a calibrado")
    ap.add_argument("-o", "--out", default="ej8_pnr.png")
    args = ap.parse_args()

    a_cal = fit_modelo(t_data, E_data)
    a_usado = a_cal * args.amult
    K = args.esfuerzo

    print(f"K historico calibracion = {K_hist:.0f} PM")
    print(f"a calibrado = {a_cal:.6f}")
    print(f"a usado = {a_usado:.6f} (x{args.amult})")
    print(f"K proyecto = {K:.1f} PM")

    # pico aproximado t=1/sqrt(2a)
    t_pico = 1.0 / np.sqrt(2.0 * a_usado)
    p_pico = E_inst(t_pico, K, a_usado)
    print(f"Pico aprox t={t_pico:.2f} meses, pmax={p_pico:.2f} personas")

    label = f"a calibrado" if args.amult == 1 else f"a x {args.amult}"
    graficar(K, a_usado, label, args.out)

    if args.amult > 1:
        print(
            "Con a mayor la curva se comprime: pico mas alto y mas temprano. "
            "Eso empuja a la zona imposible (calendario demasiado corto para el esfuerzo)."
        )

if __name__ == "__main__":
    main()
