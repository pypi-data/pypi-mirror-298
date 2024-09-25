import shutil
import sys
from pathlib import Path
from typing import Callable

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from tqdm import tqdm

from vacolba_looker_data.utils.webdriver.configurations import init_webdriver
from vacolba_looker_data.utils.webdriver.methods import (
    handle_open_url,
    handle_find_element_and_enter,
    handle_scroll_or_move,
    handle_open_menu_options,
    handle_export_data,
    confirm_export, handle_filters
)


def is_cache_available(cache_dir: Path) -> bool:
    """Verifica si el directorio de caché tiene archivos."""
    return cache_dir.exists() and any(cache_dir.iterdir())


def setup_driver_with_cache(chrome_options_func: Callable[[str, Path], Options], download_dir: str, cache_dir: Path, pbar: tqdm) -> WebDriver:
    """Configura el driver con el directorio de caché proporcionado."""
    chrome_options = chrome_options_func(download_dir, cache_dir.resolve())
    return init_webdriver(pbar, chrome_options)


def authenticate_user(driver: WebDriver, pbar: tqdm, looker_studio_url: str, user: str, password: str):
    """Realiza el flujo de autenticación del usuario."""
    handle_open_url(pbar, driver, looker_studio_url, "Abriendo Looker Studio", False)
    # handle_find_element_and_enter(pbar, driver, "Entrar al Looker Studio", '//*[@type="button"]')
    handle_find_element_and_enter(pbar, driver, "Iniciando sesión", '//*[@type="email"]', user, ttl=5)
    handle_find_element_and_enter(pbar, driver, "Ingresando contraseña", '//*[@type="password"]', password)
    handle_find_element_and_enter(pbar, driver, "Entrar al Looker Studio", '//*[@type="button"]')


def copy_cache(src_dir: Path, dest_dir: Path):
    """Copia el contenido de la caché de origen a destino."""
    if src_dir.exists():
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)


def main_flow(pbar: tqdm, driver: WebDriver, button_index: int = 3):
    """Ejecuta el flujo principal después de la autenticación."""
    if sys.argv[1]:
        handle_filters(pbar, driver, sys.argv[1])
    handle_scroll_or_move(pbar, driver, '//*[contains(@class, "simple-table")]', "Desplazándose a la tabla", action_type="scroll")
    handle_scroll_or_move(pbar, driver, '//*[contains(@class, "headerCell")]', "Moviéndose al encabezado de la tabla", action_type="move")
    handle_open_menu_options(pbar, driver, '//*[contains(@class, "ng2-chart-menu-button")]', button_index)
    handle_export_data(pbar, driver, '//*[contains(@class, "mat-mdc-menu-item")]', 'Exportar')
    confirm_export(pbar, driver, '//*[contains(@class, "mat-mdc-raised-button")]')