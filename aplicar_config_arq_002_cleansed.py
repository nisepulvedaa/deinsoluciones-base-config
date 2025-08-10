import os
import re
import config
from pathlib import Path


# === Variables específicas que deseas reemplazar ===
VARIABLES_PERMITIDAS = {
    "nombre_proceso",
    "periodicidad",
    "dataset_cleansed_zone",
    "nombre_tabla_cleansed",
    "nombre_tabla_hub",
    "campo_fecha_tabla_cleansed",
    "correos_destinatarios",
    "fecha_ejecucion",
    "ddl_satelite",
    "ddl_hub",
    "ddl_link",
    "insert_satelite",
    "insert_hub",
    "insert_link"
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