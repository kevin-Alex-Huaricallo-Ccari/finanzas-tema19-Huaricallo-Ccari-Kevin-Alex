# Estudiante: HUARICALLO CCARI KEVIN ALEX
# Código: 2024200502H
# Tema: Tema N.º 19 - Tasa de interés real ex post de los depósitos a plazo en el Perú
# Fecha de extracción: 2026-09-24

import csv
import json
import os
import urllib.request


def extraer_datos_bcrp():
  series = {
      "PN07816NM": ("tipmn_nom", "TIPMN"),
      "PN38705PM": ("ipc", "Índice de Precios al Consumidor (IPC)"),
      "PD04722MM": ("tasa_bcrp", "Tasa de Referencia de la Política Monetaria"),
      "PN01207PM": ("tipo_cambio", "Interbancario - Promedio"),
      "PN01129XM": ("embig_riesgo", "EMBIG) - Perú"),
      "PN00237MM": ("liquidez_m2", "Liquidez en Soles"),
  }
  base_url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
  records = {}

  print("Conectando con la API del BCRP...")
  for code, (column_name, expected_name) in series.items():
    url = f"{base_url}/{code}/json/2010-1/2025-12"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    with urllib.request.urlopen(req, timeout=30) as response:
      data = json.loads(response.read().decode("utf-8"))

    api_series = data.get("config", {}).get("series", [])
    if len(api_series) != 1 or expected_name.lower() not in api_series[0].get("name", "").lower():
      raise ValueError(f"La API no devolvió la serie esperada para el código {code}.")

    periods = data.get("periods", [])
    if not periods:
      raise ValueError(f"La API no devolvió periodos para el código {code}.")

    for period in periods:
      period_name = period.get("name")
      values = period.get("values", [])
      if period_name is None or len(values) != 1:
        raise ValueError(f"Respuesta inesperada para el código {code}.")

      row = records.setdefault(period_name, {"periodo": period_name})
      try:
        row[column_name] = float(values[0])
      except (ValueError, TypeError):
        row[column_name] = None

  folder = "datos_crudos"
  os.makedirs(folder, exist_ok=True)

  filename = os.path.join(folder, "datos_crudos_2024200502H.csv")
  fieldnames = ["periodo"] + [column_name for column_name, _ in series.values()]
  with open(filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records.values())

  print(
      f"[✓] Extracción exitosa. {len(records)} periodos guardados en:"
      f" {filename}"
  )


if __name__ == "__main__":
  extraer_datos_bcrp()