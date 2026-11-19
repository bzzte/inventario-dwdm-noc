# Inventario automatizado DWDM – NOC

Prototipo que automatiza el levantamiento del inventario de elementos de red (NE) de la red óptica DWDM desde Huawei iMaster NCE, lo limpia y lo muestra en un tablero web.

Proyecto final de Optativa II (IoT) y Aplicaciones de Telecomunicaciones – Ingeniería Electrónica, Universidad de San Buenaventura, Bogotá (2026).

**Autores:** Danna Michel Alfonso Guillen, Nicol Dayana Herrera Martínez, Duvan Steven Rivera Yela.

## Estructura del repositorio

| Carpeta | Contenido | Capa del sistema |
|---|---|---|
| `extractor/` | `extractor_selenium.py`: abre el portal de NCE, pausa para la intervención humana (CAPTCHA) y detecta el reporte exportado | Capa A – Adquisición |
| `procesamiento/` | `procesar_zip_html.py`: descomprime el `NE_*.zip`, omite las 3 líneas de metadatos y genera `inventario_huawei_limpio.csv`. `mapeo_campos.py`: descarta columnas sin valor operativo y agrega el campo *Plataforma NMS* | Capa B – Procesamiento |
| `dashboard/` | `dashboard_noc.py`: tablero en Streamlit con vista global y ficha técnica por nodo | Capa C – Visualización |
| `db/` | `esquema_inventario.sql`: esquema jerárquico propuesto para PostgreSQL (plataforma → nodo → chasis → tarjeta → puerto → longitud de onda) | Modelo de datos |
| `datos/` | Muestra **sintética** del inventario para probar sin acceso a NCE | – |


## Requisitos

- Windows, Google Chrome y Python 3.14
- Dependencias: `pip install -r requirements.txt`

## Ejecución

1. Definir la dirección del portal y las credenciales como variables de entorno (nunca en el código):
   ```
   set NCE_URL=https://direccion-del-portal-nce
   set NCE_USER=su_usuario
   set NCE_PASS=su_contraseña
   ```
2. Extraer: `py extractor/extractor_selenium.py`. Resolver el CAPTCHA si aparece, ir a **Resource → Physical Inventory → NEs**, exportar y presionar ENTER cuando termine la descarga.
3. Procesar: `py procesamiento/procesar_zip_html.py`. Debe generarse `inventario_huawei_limpio.csv`.
4. Visualizar: `py -m streamlit run dashboard/dashboard_noc.py --server.address localhost` y abrir `http://localhost:8501`.

Sin acceso a NCE, el tablero se puede probar con la muestra sintética: copiar `datos/inventario_muestra.csv` como `inventario_huawei_limpio.csv` y ejecutar el paso 4. La muestra usa nombres y direcciones ficticias (rango de documentación 192.0.2.0/24).

## Nota sobre esta versión

Es una versión depurada del código usado en las pruebas del informe: se retiraron la dirección del portal, las credenciales y las rutas locales, y se organizó por capas. La lógica de extracción, limpieza y visualización es la misma. Los selectores del formulario de inicio de sesión en `extractor_selenium.py` deben verificarse contra el portal de NCE.

## Seguridad y confidencialidad

Este repositorio no contiene credenciales, direcciones IP, MAC ni datos reales de la red de la empresa. Los reportes exportados (`.zip`) y los inventarios reales (`.csv`) están excluidos por `.gitignore`.
