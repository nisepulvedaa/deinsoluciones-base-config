import os
import re
import config
from pathlib import Path

# === Variables específicas que deseas reemplazar ===
VARIABLES_PERMITIDAS = {
    "nombre_proceso",
    "version_arquetipo_raw",
    "periodicidad",
    "buckets_detino",
    "path_destino",
    "proyecto",
    "nombre_archivo",
    "dataset_raw_zone",
    "nombre_tabla_raw",
    "campo_fecha_tabla_raw",
    "fecha_ejecucion",
    "ddl_raw",
    "correos_destinatarios"
}

# === Extraer solo las variables válidas desde config.py ===
variables = {
    k: str(v)
    for k, v in config.__dict__.items()
    if k in VARIABLES_PERMITIDAS
}

# === Directorio actual ===
directorio_actual = Path(__file__).parent.resolve()

print(f"🔍 Buscando archivos en: {directorio_actual}")

# === Reemplazo de variables en archivos .sql y .json ===
for archivo in directorio_actual.glob("*"):
    if not archivo.is_file() or archivo.suffix not in [".sql", ".json"]:
        continue

    print(f"🔧 Reemplazando variables en: {archivo.name}")
    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    for var, valor in variables.items():
        patron = rf"\{{\{{\s*{re.escape(var)}\s*\}}\}}"
        contenido = re.sub(patron, valor, contenido)

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

print("\n✅ Reemplazo de variables completado con éxito.")