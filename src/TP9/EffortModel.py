#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* EffortModel - modificado TP9
#* Modelos estaticos: lineal y exponencial (potencia via log-log)
#* Dataset del enunciado TP9
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
import numpy as np
import pandas as pd
import argparse
import statsmodels.api as sm
import sys
import matplotlib.pyplot as plt

# dataset del enunciado TP9
data = {
    'LOC': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
    'Esfuerzo': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
}

version = "7.0-TP9"
linear = False
exponential = False
estimate_loc = None

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--version", required=False, help="version", action="store_true")
ap.add_argument("-x", "--exponential", required=False, help="Exponential model", action="store_true")
ap.add_argument("-l", "--linear", required=False, help="Linear model", action="store_true")
ap.add_argument("-e", "--estimate", type=float, required=False, help="LOC a estimar")
ap.add_argument("-o", "--out", default="ej9_effort.png")
ap.add_argument("--both", action="store_true", help="corre lineal y exponencial")
args = vars(ap.parse_args())

if args['version'] == True:
    print("Program %s version %s" % (sys.argv[0], version))
    sys.exit(0)

if args['linear'] == True:
    linear = True
if args['exponential'] == True:
    exponential = True
if args['both'] == True or (linear == False and exponential == False):
    linear = True
    exponential = True
if args['estimate'] is not None:
    estimate_loc = args['estimate']

df = pd.DataFrame(data)
print("Dataset TP9:")
print(df)
print("Correlacion LOC-Esfuerzo = %.4f" % (df['LOC'].corr(df['Esfuerzo'])))

resultados = {}

# modelo lineal E = b + a*LOC
if linear:
    a, b = np.polyfit(df['LOC'], df['Esfuerzo'], 1)
    R = np.corrcoef(df['LOC'], df['Esfuerzo'])
    r_value = (R[0][1]) ** 2
    print("Modelo lineal E=%.6f + %.6f*LOC" % (b, a))
    print("R-squared=%.4f (lineal)" % (r_value))
    resultados['lineal'] = {'a': a, 'b': b, 'r2': r_value, 'pred': lambda loc: b + a * loc}
    lbl = ("modelo lineal (R2=%.4f)" % (r_value))
    x_line = np.linspace(min(200, df['LOC'].min()), max(10000, df['LOC'].max()), 300)
    plt.plot(x_line, a * x_line + b, label=lbl, color='red')

# modelo exponencial/potencia E = k * LOC^b  (como el original del taller)
if exponential:
    df['logEsfuerzo'] = np.log(df['Esfuerzo'])
    df['logLOC'] = np.log(df['LOC'])
    X = sm.add_constant(df['logLOC'])
    Y = df['logEsfuerzo']
    mx = sm.OLS(Y, X).fit()
    print(mx.summary())
    k = np.exp(mx.params['const'])
    b_exp = mx.params['logLOC']
    print("Modelo exponencial E=%.6f*(LOC^%.6f)" % (k, b_exp))
    print("R-squared=%.4f (exponencial)" % (mx.rsquared))
    resultados['exponencial'] = {
        'k': k, 'b': b_exp, 'r2': mx.rsquared,
        'pred': lambda loc, k=k, b_exp=b_exp: k * (loc ** b_exp)
    }
    lbl = ("modelo exponencial (R2=%.4f)" % (mx.rsquared))
    x_line = np.linspace(min(200, df['LOC'].min()), max(10000, df['LOC'].max()), 300)
    plt.plot(x_line, k * (x_line ** b_exp), label=lbl, color='green')

# elige mejor por R2
mejor_nombre = max(resultados.keys(), key=lambda n: resultados[n]['r2'])
mejor = resultados[mejor_nombre]
print("\nMejor modelo por R2: %s (R2=%.4f)" % (mejor_nombre, mejor['r2']))

locs_est = []
if estimate_loc is not None:
    locs_est = [estimate_loc]
else:
    locs_est = [9100, 200]

for loc in locs_est:
    e_hat = float(mejor['pred'](loc))
    print("Estimacion LOC=%.0f con modelo %s: E=%.3f PM" % (loc, mejor_nombre, e_hat))
    plt.scatter([loc], [e_hat], s=80, zorder=4, label="LOC=%.0f -> E=%.2f" % (loc, e_hat))
    if loc < df['LOC'].min() or loc > df['LOC'].max():
        print(
            "Cuidado: LOC=%.0f esta fuera del rango historico [%d, %d]. "
            "La extrapolacion no es confiable." % (loc, df['LOC'].min(), df['LOC'].max())
        )

plt.scatter(df['LOC'], df['Esfuerzo'], label='Datos historicos', color='#1f4e79', zorder=3)
plt.xlabel('Complejidad [LOC]')
plt.ylabel('Esfuerzo (persona-mes)')
plt.title('EffortModel TP9')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(args['out'], dpi=150)
print("Grafico: %s" % args['out'])
plt.close()
