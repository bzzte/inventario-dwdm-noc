"""
Mapeo de campos y depuración del inventario limpio.
Lo usa el tablero (dashboard/dashboard_noc.py).
"""
import pandas as pd

# Columnas del reporte de Huawei sin valor operativo para el NOC
COLUMNAS_BASURA = [
    'NE IPv6 Address', 'Physical location', 'NE alias',
    'Patch Version List', 'Optical NE', 'Life cycle status', 'Custom Label'
]


def cargar_inventario(ruta_csv="inventario_huawei_limpio.csv"):
    """Lee el inventario limpio, descarta columnas basura y estandariza la plataforma."""
    df = pd.read_csv(ruta_csv, encoding='utf-8', on_bad_lines='skip')

    # 1. Depuración: eliminar columnas innecesarias del reporte de Huawei
    columnas_existentes = [col for col in COLUMNAS_BASURA if col in df.columns]
    df = df.drop(columns=columnas_existentes)

    # 2. Estandarización de plataforma para arquitectura multi-vendor
    if 'Plataforma NMS' not in df.columns:
        df['Plataforma NMS'] = 'Huawei iMaster NCE'

    return df


def conteo_tarjetas(df_filtrado):
    """
    3. Conteo por tipo de tarjeta de un nodo.
    Variables clave: 'NE Name' (nodo), 'NE IP Address' (IP de gestión),
    'Software Version' (versión) y 'Board Type' (tarjetas instaladas).
    El reporte de NEs no trae 'Board Type': en ese caso devuelve None.
    """
    if 'Board Type' not in df_filtrado.columns:
        return None
    conteo = df_filtrado['Board Type'].value_counts().reset_index()
    conteo.columns = ['Tipo de Tarjeta (Board)', 'Cantidad Instalada']
    return conteo
