"""
Capa A - Adquisición.
Abre el portal de Huawei iMaster NCE, inyecta las credenciales y se pausa para la
intervención humana (CAPTCHA y exportación). Después detecta el NE_*.zip descargado
y llama al procesador.

Variables de entorno requeridas: NCE_URL, NCE_USER, NCE_PASS.
Opcional: NCE_RUTA (carpeta de descargas; por defecto, la carpeta del usuario).
"""
import os
import sys
import glob
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "procesamiento"))
from procesar_zip_html import procesar_zip_directo  # noqa: E402

NCE_URL = os.environ["NCE_URL"]
NCE_USER = os.environ["NCE_USER"]
NCE_PASS = os.environ["NCE_PASS"]
RUTA_BASE = os.environ.get("NCE_RUTA", os.path.expanduser("~"))

# Selectores del formulario UNISSO. VERIFICAR contra el portal real.
SELECTOR_USUARIO = (By.CSS_SELECTOR, "input[type='text']")
SELECTOR_CLAVE = (By.CSS_SELECTOR, "input[type='password']")
SELECTOR_BOTON = (By.ID, "submitDataverify")


def configurar_chrome():
    """Chrome descarga automáticamente en RUTA_BASE, sin cuadros de diálogo."""
    opciones = webdriver.ChromeOptions()
    opciones.add_experimental_option("prefs", {
        "download.default_directory": RUTA_BASE,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True,
    })
    opciones.add_argument("--ignore-certificate-errors")
    return webdriver.Chrome(options=opciones)


def main():
    print("=" * 50)
    print("   NOC BACKEND - EXPORTACIÓN DIRECTA NCE")
    print("=" * 50)

    driver = configurar_chrome()
    espera = WebDriverWait(driver, 15)

    print("\n[1/3] Abriendo portal de NCE...")
    driver.get(NCE_URL)

    print("[2/3] Rellenando credenciales...")
    espera.until(EC.presence_of_element_located(SELECTOR_USUARIO)).send_keys(NCE_USER)
    driver.find_element(*SELECTOR_CLAVE).send_keys(NCE_PASS)

    print("[*] Clic en botón de acceso...")
    boton = espera.until(EC.presence_of_element_located(SELECTOR_BOTON))
    driver.execute_script("arguments[0].click();", boton)
    time.sleep(3)

    # Pausa intencional: intervención humana (human-in-the-loop)
    print("\n" + "=" * 58)
    print(" INTERVENCIÓN HUMANA REQUERIDA (VERIFICACIÓN ROBOT)")
    print("=" * 58)
    print("1. Resuelve el CAPTCHA en Chrome si aparece.")
    print("2. Ve a Resource -> Physical Inventory -> NEs.")
    print("3. Haz clic en el botón 'Export All' en la plataforma NCE.")
    input(">>> 4. Cuando el archivo se HAYA DESCARGADO en tu PC, presiona [ENTER] aquí... <<<")

    print("\n[3/3] Consolidando archivo para el Dashboard...")
    archivos = glob.glob(os.path.join(RUTA_BASE, "NE_*.zip"))
    if not archivos:
        print("[ERROR] No se encontró ningún NE_*.zip. ¿Terminó la descarga?")
        driver.quit()
        return
    reciente = max(archivos, key=os.path.getctime)
    print(f"[*] Archivo detectado: {os.path.basename(reciente)}")

    salida = procesar_zip_directo(RUTA_BASE)
    if salida:
        print(f"\n[OK] ¡Listo! Archivo ZIP procesado y guardado como: {os.path.basename(salida)}")
    driver.quit()


if __name__ == "__main__":
    main()
