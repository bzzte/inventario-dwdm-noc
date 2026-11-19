"""
Capa B - Procesamiento.
Localiza el último reporte NE_*.zip exportado por Huawei iMaster NCE, extrae su
archivo interno, omite las 3 líneas de metadatos y genera inventario_huawei_limpio.csv.
"""
import os
import zipfile
import glob
import pandas as pd

# Carpeta donde Chrome guarda las descargas (por defecto, la carpeta del usuario).
RUTA_BASE = os.environ.get("NCE_RUTA", os.path.expanduser("~"))


def procesar_zip_directo(ruta_base=RUTA_BASE):
    # 1. Localizar el archivo ZIP más reciente descargado de NCE
    patron_busqueda = os.path.join(ruta_base, "NE_*.zip")
    archivos_zip = glob.glob(patron_busqueda)
    if not archivos_zip:
        print(f"[ERROR] No se encontró ningún NE_*.zip en {ruta_base}")
        return None
    archivo_reciente = max(archivos_zip, key=os.path.getctime)
    print(f"[*] Archivo ZIP detectado: {os.path.basename(archivo_reciente)}")

    # 2. Extraer el archivo de datos interno (.csv, .txt o .html)
    with zipfile.ZipFile(archivo_reciente, 'r') as zip_ref:
        archivos_internos = zip_ref.namelist()
        archivo_interno = next((f for f in archivos_internos if f.endswith(('.csv', '.txt', '.html'))), None)
        if archivo_interno is None:
            print("[ERROR] El ZIP no contiene un archivo .csv, .txt o .html")
            return None
        zip_ref.extract(archivo_interno, path=ruta_base)
        ruta_extraida = os.path.join(ruta_base, archivo_interno)

    # 3. Leer la tabla omitiendo las 3 filas de cabecera basura de Huawei
    try:
        df = pd.read_csv(ruta_extraida, encoding='utf-8', skiprows=3)
    except UnicodeDecodeError:
        df = pd.read_csv(ruta_extraida, encoding='latin1', skiprows=3)

    # Limpiar espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()

    # 4. Exportar la tabla estructurada
    archivo_salida = os.path.join(ruta_base, "inventario_huawei_limpio.csv")
    df.to_csv(archivo_salida, index=False)

    print("[OK] ¡Procesamiento exitoso!")
    print(f"[OK] Archivo listo y depurado: {archivo_salida}")
    print(f"[*] Total de equipos/filas cargadas: {len(df)}")
    return archivo_salida


if __name__ == "__main__":
    print("+" * 44)
    print("   NOC BACKEND - PROCESAMIENTO LIMPIO DE ZIP")
    print("+" * 44)
    procesar_zip_directo()
