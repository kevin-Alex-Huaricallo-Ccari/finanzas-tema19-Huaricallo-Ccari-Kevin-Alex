# Estudiante: HUARICALLO CCARI KEVIN ALEX
# Código: 2024200502H
# Tema: Tema N.º 19 - Tasa de interés real ex post de los depósitos a plazo en el Perú
# Fecha de extracción: 2026-09-24

import hashlib
import os
import pandas as pd


def limpiar_y_procesar_datos():
  input_path = os.path.join(
      "datos_crudos", "datos_crudos_2024200502H.csv"
  )
  if not os.path.exists(input_path):
    raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

  df = pd.read_csv(input_path)

  # Tratamiento de valores nulos en origen por arrastre
  df.ffill(inplace=True)
  df.bfill(inplace=True)

  # Cálculo de Inflación Anualizada y Tasa Real Ex Post (Ecuación de Fisher)
  df["ipc_variacion_anual"] = df["ipc"].pct_change(12) * 100
  df["tasa_real_expost"] = df["tipmn_nom"] - df["ipc_variacion_anual"]

  # Descartar las primeras 12 observaciones que contienen NaN por el porcentaje a 12 meses
  df_limpio = df.dropna().copy()

  columnas_salida = [
      "periodo",
      "tasa_real_expost",
      "tipmn_nom",
      "ipc",
      "tasa_bcrp",
      "tipo_cambio",
      "embig_riesgo",
      "liquidez_m2",
  ]
  df_procesado = df_limpio[columnas_salida]

  folder_out = "datos_procesados"
  if not os.path.exists(folder_out):
    os.makedirs(folder_out)

  output_filename = os.path.join(
      folder_out, "datos_procesados_2024200502H.csv"
  )
  df_procesado.to_csv(output_filename, index=False, encoding="utf-8")

  # Verificación SHA-256 exigida por la asignatura
  with open(output_filename, "rb") as f:
    sha256_hash = hashlib.sha256(f.read()).hexdigest()

  print("--- PROCESAMIENTO EXITOSO ---")
  print(f"Registros limpios obtenidos: {len(df_procesado)}")
  print(f"Archivo generado en: {output_filename}")
  print(f"Hash SHA-256: {sha256_hash}")


if __name__ == "__main__":
  limpiar_y_procesar_datos()