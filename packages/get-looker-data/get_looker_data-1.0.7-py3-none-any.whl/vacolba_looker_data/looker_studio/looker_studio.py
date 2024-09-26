import os
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm

from vacolba_looker_data.utils.looker_studio.methods import is_cache_available, authenticate_user, copy_cache, main_flow, \
    setup_driver_with_cache
from vacolba_looker_data.utils.webdriver.methods import handle_open_url
from vacolba_looker_data.utils.webdriver.configurations import set_chrome_options

# Cargar archivo .env desde una ruta absoluta
env_path = Path('.') / '.env'  # Esto intenta cargar el .env en el directorio de trabajo actual
load_dotenv(dotenv_path=env_path)

# Configurar las variables de entorno
LOOKER_STUDIO_URL = os.getenv('LOOKER_STUDIO_URL')
VACOLBA_USER = os.getenv('VACOLBA_USER')
VACOLBA_PASS = os.getenv('VACOLBA_PASS')
DOWNLOAD_DIRECTORY = os.getenv('DOWNLOAD_DIRECTORY', str(Path('files').resolve()))
CACHE_DIRECTORY = Path('cache').resolve()
TEMP_CACHE_DIRECTORY = Path('temp_cache').resolve()
BUTTON_INDEX = os.getenv('BUTTON_INDEX', 3)


def get_looker_data(pbar: tqdm, looker_url: str = LOOKER_STUDIO_URL):
    """Obtiene los datos de Looker Studio, gestionando la autenticación y la caché."""
    # Configuración del driver
    cache_directory = CACHE_DIRECTORY if is_cache_available(CACHE_DIRECTORY) else TEMP_CACHE_DIRECTORY
    driver = setup_driver_with_cache(set_chrome_options, DOWNLOAD_DIRECTORY, cache_directory, pbar)

    try:
        if not is_cache_available(CACHE_DIRECTORY):
            # Autenticación y copia de la caché al directorio permanente si es necesario
            authenticate_user(driver, pbar, looker_url, VACOLBA_USER, VACOLBA_PASS)
            driver.quit()  # Cerrar navegador para copiar caché
            copy_cache(TEMP_CACHE_DIRECTORY, CACHE_DIRECTORY)
            driver = setup_driver_with_cache(set_chrome_options, DOWNLOAD_DIRECTORY, CACHE_DIRECTORY, pbar)
        else:
            pbar.set_description("Autenticacion obtenida")
            pbar.update(3)

        # Ejecutar flujo principal después de la autenticación
        handle_open_url(pbar, driver, looker_url, "Abriendo Looker Studio")
        main_flow(pbar, driver, int(BUTTON_INDEX))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        pbar.set_description("Cerrando navegador")
        driver.quit()
