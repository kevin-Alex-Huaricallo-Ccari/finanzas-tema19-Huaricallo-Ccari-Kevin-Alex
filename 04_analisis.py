# Estudiante: HUARICALLO CCARI KEVIN ALEX
# Código: 2024200502H
# Tema: Tema N.º 19 - Tasa de interés real ex post de los depósitos a plazo en el Perú
# Fecha de extracción: 2026-09-24

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


def realizar_analisis_econometrico():
  input_path = os.path.join(
      "datos_procesados", "datos_procesados_2024200502H.csv"
  )
  if not os.path.exists(input_path):
    raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

  df = pd.read_csv(input_path)
  print(f"Cargados {len(df)} registros válidos para el modelo OLS.\n")

  folder_salidas = "salidas"
  if not os.path.exists(folder_salidas):
    os.makedirs(folder_salidas)

  variables_num = [
      "tasa_real_expost",
      "tasa_bcrp",
      "tipo_cambio",
      "embig_riesgo",
      "liquidez_m2",
  ]

  # 1. Estadísticas Descriptivas
  resumen_stats = df[variables_num].describe().T
  resumen_stats["skewness"] = df[variables_num].skew()
  resumen_stats["kurtosis"] = df[variables_num].kurtosis()
  path_stats = os.path.join(
      folder_salidas, "tabla_estadisticas_descriptivas.csv"
  )
  resumen_stats.to_csv(path_stats)

  print("--- ESTADÍSTICAS DESCRIPTIVAS ---")
  print(resumen_stats[["mean", "std", "min", "50%", "max", "skewness"]])

  # 2. Matriz de Correlación
  matriz_corr = df[variables_num].corr()
  path_corr = os.path.join(folder_salidas, "matriz_correlacion.csv")
  matriz_corr.to_csv(path_corr)

  # 3. Regresión OLS con Errores Robustos Newey-West (HAC)
  Y = df["tasa_real_expost"]
  X = df[["tasa_bcrp", "tipo_cambio", "embig_riesgo", "liquidez_m2"]]
  X = sm.add_constant(X)

  modelo = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})

  path_modelo = os.path.join(folder_salidas, "resultados_regresion_ols.txt")
  with open(path_modelo, "w", encoding="utf-8") as f:
    f.write(modelo.summary().as_text())

  print("\n--- RESUMEN DEL MODELO ECONOMÉTRICO (OLS HAC) ---")
  print(modelo.summary())

  # 4. Evolución de la tasa real ex post
  fig, ax = plt.subplots(figsize=(10, 4))
  ax.plot(
      df["periodo"],
      df["tasa_real_expost"],
      color="navy",
      linewidth=2,
      label="Tasa Real Ex Post (Y)",
  )
  ax.axhline(0, color="red", linestyle="--", linewidth=1)
  ax.set_title(
      "Evolución de la Tasa Real Ex Post (2010–2025)",
      fontsize=11,
      fontweight="bold",
  )
  ax.set_xlabel("Periodo")
  ax.set_ylabel("Porcentaje (%)")
  ax.set_xticks(range(0, len(df), 24), df["periodo"].iloc[::24], rotation=45)
  ax.grid(True, linestyle=":", alpha=0.6)
  fig.tight_layout()
  fig.savefig(
      os.path.join(folder_salidas, "grafico1_tasa_real_expost.png"), dpi=300
  )
  plt.close(fig)

  inflacion_anual = df["tipmn_nom"] - df["tasa_real_expost"]
  fig, ax = plt.subplots(figsize=(10, 4))
  ax.plot(df["periodo"], df["tipmn_nom"], label="TIPMN", color="teal")
  ax.plot(
      df["periodo"],
      inflacion_anual,
      label="Inflación anualizada (IPC)",
      color="darkorange",
  )
  ax.set_title("TIPMN e inflación anualizada")
  ax.set_xlabel("Periodo")
  ax.set_ylabel("Porcentaje (%)")
  ax.set_xticks(range(0, len(df), 24), df["periodo"].iloc[::24], rotation=45)
  ax.grid(True, linestyle=":", alpha=0.6)
  ax.legend()
  fig.tight_layout()
  fig.savefig(
      os.path.join(folder_salidas, "grafico2_tipmn_inflacion.png"), dpi=300
  )
  plt.close(fig)

  nombres = ["Tasa real", "Tasa BCRP", "Tipo de cambio", "EMBIG", "Liquidez M2"]
  fig, ax = plt.subplots(figsize=(8, 6))
  imagen = ax.imshow(matriz_corr.to_numpy(), cmap="RdYlBu_r", vmin=-1, vmax=1)
  ax.set_xticks(range(len(nombres)), nombres, rotation=35, ha="right")
  ax.set_yticks(range(len(nombres)), nombres)
  ax.set_title("Matriz de correlación")
  for row in range(len(nombres)):
    for column in range(len(nombres)):
      ax.text(
          column,
          row,
          f"{matriz_corr.iloc[row, column]:.2f}",
          ha="center",
          va="center",
          color="black",
      )
  fig.colorbar(imagen, ax=ax, label="Correlación")
  fig.tight_layout()
  fig.savefig(
      os.path.join(folder_salidas, "grafico3_matriz_correlacion.png"), dpi=300
  )
  plt.close(fig)

  nombres_variables = {
      "tasa_bcrp": "Tasa de referencia BCRP (%)",
      "tipo_cambio": "Tipo de cambio (S/ por US$)",
      "embig_riesgo": "EMBIG Perú (puntos básicos)",
      "liquidez_m2": "Liquidez M2 (millones de S/)",
  }
  colores = ["royalblue", "darkorange", "seagreen", "firebrick"]
  for (variable, nombre), color in zip(nombres_variables.items(), colores):
    valores_x = df[variable]
    valores_y = df["tasa_real_expost"]
    linea_x = np.linspace(valores_x.min(), valores_x.max(), 100)
    pendiente, intercepto = np.polyfit(valores_x, valores_y, 1)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(valores_x, valores_y, color=color, alpha=0.65, s=24)
    ax.plot(
        linea_x,
        pendiente * linea_x + intercepto,
        color="black",
        linewidth=2,
    )
    ax.set_title(f"Tasa real ex post y {nombre}")
    ax.set_xlabel(nombre)
    ax.set_ylabel("Tasa real ex post (%)")
    ax.grid(True, linestyle=":", alpha=0.6)
    fig.tight_layout()
    fig.savefig(
        os.path.join(folder_salidas, f"grafico4_relacion_{variable}.png"),
        dpi=300,
    )
    plt.close(fig)

  print("\n==========================================")
  print("--- ANÁLISIS COMPLETADO CON ÉXITO ---")
  print("Se generaron 7 gráficos y los demás insumos en /salidas.")
  print("==========================================")


if __name__ == "__main__":
  realizar_analisis_econometrico()