from pathlib import Path

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

def set_chrome_options(download_directory: str, cache_directory: Path) -> Options:
    """
    Configura las opciones de ChromeDriver para la automatización del navegador.

    Parámetros:
    ----------
    download_directory: str
        La ruta al directorio donde se descargarán los archivos.

    Retorno:
    -------
    Options
        Un objeto de tipo `Options` configurado con las preferencias de descarga y otras opciones de Chrome.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Iniciar navegador maximizado

    # Configurar las preferencias de descarga de Chrome
    prefs = {
        "download.default_directory": download_directory,  # Configurar directorio de descarga
        "download.prompt_for_download": False,  # Desactivar la solicitud de confirmación de descarga
        "download.directory_upgrade": True,  # Permitir la actualización del directorio de descarga
        "safebrowsing.enabled": True  # Activar navegación segura
    }
    chrome_options.add_experimental_option("prefs", prefs)

    cache_directory = Path(cache_directory)

    # Configurar el directorio de cache del navegador
    if cache_directory.exists():
        chrome_options.add_argument(f"user-data-dir={cache_directory}")
    else:
        cache_directory.mkdir(parents=True, exist_ok=True)
        chrome_options.add_argument(f"user-data-dir={cache_directory}")

    return chrome_options


def init_webdriver(pbar: tqdm, chrome_options: Options) -> WebDriver:
    """
    Inicializa el navegador ChromeDriver con las opciones especificadas.

    Parámetros:
    ----------
    pbar: tqdm
        Un objeto de tipo `tqdm` que representa la barra de progreso.

    chrome_options: Options
        Un objeto de tipo `Options` configurado con las preferencias del navegador Chrome.

    Retorno:
    -------
    webdriver.Chrome
        Una instancia de ChromeDriver inicializada con las opciones proporcionadas.
    """
    try:
        # Paso 1: Inicializar el navegador
        pbar.set_description("Inicializando navegador")
        driver = webdriver.Chrome(options=chrome_options)
        pbar.update(1)

    except WebDriverException:
        pbar.set_description("Instalando ChromeDriver")
        driver_service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(options=chrome_options, service=driver_service)
        pbar.update(1)

    return driver
