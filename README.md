# Tasa de Interés Real Ex Post de los Depósitos a Plazo en el Perú (2010–2025)

## Información general

- *Curso:* Finanzas I (Código 055D)
- *Docente:* MSc. Ciro Iván Machacuay Meza
- *Unidad:* I
- *Estudiante:* HUARICALLO CCARI KEVIN ALEX
- *Código de matrícula:* 2024200502H
- *Tema asignado:* Tema N.º 19

---

## 1. Descripción del Proyecto

El presente trabajo de investigación analiza los determinantes macrofinancieros de la Tasa de Interés Real Ex Post de los depósitos a plazo fijo en moneda nacional en el Perú durante el periodo 2010–2025, evaluando el impacto de la política monetaria, el tipo de cambio, el riesgo país y la liquidez del sistema bancario.

## 2. Variables de Investigación

- *Variable Endógena (Y):* Tasa de Interés Real Ex Post (construida a partir de la TIPMN y el IPC).
- *Variables Exógenas (X):*
  1. *Tasa de Referencia del BCRP:* Postura de la política monetaria.
  2. *Variación del Tipo de Cambio (TC):* Presión cambiaria y preferencia por moneda.
  3. *Riesgo País (EMBIG Perú):* Incertidumbre macroeconómica.
  4. *Liquidez del Sistema (M2):* Agregado monetario en moneda nacional.

## 3. Fuentes de Datos y Vía de Extracción

- *Fuente Principal (API REST):* BCRPData REST (https://estadisticas.bcrp.gob.pe/estadisticas/series/api/).
- *Cobertura:* Frecuencia mensual (2010–2025) con más de 180 observaciones.

## 4. Estructura del Repositorio

- /codigo: Scripts de extracción (01_extraccion_api.py), limpieza (03_limpieza_datos.py) y análisis (04_analisis.py).
- /datos_crudos: Archivo CSV original de la API (datos_crudos_2024200502H.csv).
- /datos_procesados: Dataset limpio y preparado (datos_procesados_2024200502H.csv).
- /salidas: Tablas y gráficos generados para el artículo en LaTeX.

## 🔑 Verificación de Integridad de Datos (SHA-256)

* **Archivo:** `datos_procesados/datos_procesados_2024200502H.csv`
* **Algoritmo:** SHA-256
* **Hash:** `9a83d8dc06f35778c51b085162178569ab4d2bcb05063ea1e930d0d34239c819`