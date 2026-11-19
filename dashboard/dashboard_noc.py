"""
Capa C - Visualización.
Tablero del NOC en Streamlit. Ejecutar desde la carpeta donde está inventario_huawei_limpio.csv:
    py -m streamlit run dashboard/dashboard_noc.py --server.address localhost
"""
import os
import sys
from datetime import datetime

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "procesamiento"))
from mapeo_campos import cargar_inventario, conteo_tarjetas  # noqa: E402

RUTA_CSV = os.environ.get("INVENTARIO_CSV", "inventario_huawei_limpio.csv")

st.set_page_config(page_title="Inventario DWDM - NOC", layout="wide")

if not os.path.exists(RUTA_CSV):
    st.error(f"No se encontró {RUTA_CSV}. Ejecute primero el procesador.")
    st.stop()

df = cargar_inventario(RUTA_CSV)
sincronizacion = datetime.fromtimestamp(os.path.getmtime(RUTA_CSV)).strftime("%Y-%m-%d %H:%M:%S")

# --- Barra lateral: filtros ---
st.sidebar.header("Filtros de Infraestructura")
plataformas = ["Todos"] + sorted(df['Plataforma NMS'].dropna().unique().tolist())
plataforma = st.sidebar.selectbox("Seleccionar Plataforma NMS", plataformas)
if plataforma != "Todos":
    df = df[df['Plataforma NMS'] == plataforma]

st.sidebar.header("Análisis Individual DWDM")
nodos_lista = ["Vista Global"] + sorted(df['NE Name'].dropna().unique().tolist())
nodo = st.sidebar.selectbox("Buscar comportamiento por Nodo", nodos_lista)

# --- Vista global ---
if nodo == "Vista Global":
    st.markdown("**Dashboard de Inventario Automatizado DWDM**")
    st.write("Centro de Operaciones de Red (NOC) - Grupo Salinas")
    st.caption(f"Última sincronización de red: {sincronizacion}")
    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("Elementos de red (filas)", len(df))
    c2.metric("Nodos distintos", df['NE Name'].nunique())
    c3.metric("Plataformas integradas", df['Plataforma NMS'].nunique())

    st.subheader(f"Inventario Físico Centralizado - {plataforma}")
    st.dataframe(df, width="stretch")

# --- Vista por nodo ---
else:
    df_filtrado = df[df['NE Name'] == nodo]
    st.header(f"Comportamiento de Hardware: {nodo}")

    col_graf, col_ficha = st.columns([2, 1])
    with col_graf:
        conteo = conteo_tarjetas(df_filtrado)
        if conteo is None:
            st.info("Parámetro 'Board Type' no detectado para graficar.")
        else:
            st.bar_chart(conteo.set_index('Tipo de Tarjeta (Board)'))
    with col_ficha:
        fila = df_filtrado.iloc[0]
        st.markdown("**Ficha Técnica del Equipo:**")
        st.markdown(f"- **IP de Gestión:** {fila.get('NE IP Address', 'N/D')}")
        st.markdown(f"- **Versión de Software:** {fila.get('Software Version', 'N/D')}")
        st.markdown(f"- **Registros del nodo:** {len(df_filtrado)}")

    st.subheader(f"Inventario Físico del nodo {nodo}")
    st.dataframe(df_filtrado, width="stretch")
