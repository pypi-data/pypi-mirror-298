import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


OPTIONS_VALUES = {
    "select_option_21": "Este trimestre",
    "select_option_23": "El último trimestre"
}


def handle_open_url(pbar: tqdm, driver: WebDriver, looker_studio_url: str, description: str, update=True) -> None:
    """
       Abre url y actualiza la barra de progreso.

       Parámetros:
       ----------
       pbar : tqdm.std.tqdm
           Una instancia de la barra de progreso de `tqdm` que se utiliza para mostrar el progreso en la consola.

       driver : selenium.webdriver.chrome.webdriver.WebDriver
           La instancia del controlador de Selenium WebDriver que controla el navegador.

       looker_studio_url : str
           Una cadena de texto que sera la url a la que accederemos en el navegador.

       description : str
           Una cadena de texto que describe la acción actual que se está realizando. Esta descripción se muestra en la barra de progreso.

       Retorno:
       -------
       None
           Este método no retorna ningún valor.
    """
    pbar.set_description(description)
    driver.get(looker_studio_url)
    time.sleep(2)
    if update:
        pbar.update(1)


def handle_find_element_and_enter(pbar: tqdm, driver: WebDriver, description: str, element: str, value: str = None, ttl: int = 10) -> None:
    """
       Encuentra un elemento web por su XPath, interactúa con él y actualiza la barra de progreso.

       Este método busca un elemento en la página web utilizando Selenium, envía un valor de entrada si se proporciona,
       simula un evento de pulsación de tecla (ENTER), y luego espera un tiempo antes de continuar, actualizando la barra de progreso.

       Parámetros:
       ----------
       pbar : tqdm.std.tqdm
           Una instancia de la barra de progreso de `tqdm` que se utiliza para mostrar el progreso en la consola.

       driver : selenium.webdriver.chrome.webdriver.WebDriver
           La instancia del controlador de Selenium WebDriver que controla el navegador.

       description : str
           Una cadena de texto que describe la acción actual que se está realizando. Esta descripción se muestra en la barra de progreso.

       element : str
           Un selector XPath que identifica el elemento web en la página con el que se quiere interactuar.

       value : str, opcional
           El valor que se enviará al elemento web encontrado. Si es `None`, no se envía ningún valor de entrada (por defecto es `None`).

       ttl : int, opcional
           El tiempo en segundos que el script esperará después de interactuar con el elemento web antes de proceder. El valor predeterminado es 10 segundos.

       Retorno:
       -------
       None
           Este método no retorna ningún valor.
       """
    pbar.set_description(description)
    element_found = driver.find_element(By.XPATH, element)
    if value is not None:
        element_found.send_keys(value)
    element_found.send_keys(Keys.ENTER)
    time.sleep(ttl)
    pbar.update(1)


def handle_scroll_or_move(pbar: tqdm, driver: WebDriver, xpath: str, description: str,
                          action_type: str = "scroll") -> None:
    """
    Desplaza o mueve el cursor a un elemento especificado en la página y actualiza la barra de progreso.

    Parámetros:
    ----------
    pbar: tqdm
        Un objeto de tipo `tqdm` que representa la barra de progreso.

    driver: WebDriver
        Una instancia del navegador ChromeDriver.

    xpath: str
        El XPath del elemento al cual se desea desplazar o mover.

    description: str
        Una descripción del paso actual que se mostrará en la barra de progreso.

    action_type: str, opcional
        El tipo de acción a realizar: "scroll" para desplazamiento o "move" para mover el cursor. Por defecto es "scroll".

    Retorno:
    -------
    None
        Esta función no retorna ningún valor.
    """
    pbar.set_description(description)
    element = driver.find_element(By.XPATH, xpath)
    actions = ActionChains(driver)

    if action_type == "scroll":
        actions.scroll_to_element(element).perform()
    elif action_type == "move":
        actions.move_to_element(element).perform()

    pbar.update(1)
    time.sleep(5)  # Añadir tiempo de espera si es necesario


def handle_open_menu_options(pbar: tqdm, driver: WebDriver, menu_xpath: str, button_index: int) -> None:
    """
    Abre el menú mas opciones seleccionando un botón específico basado en su índice.

    Parámetros:
    ----------
    pbar: tqdm
        Un objeto de tipo `tqdm` que representa la barra de progreso.

    driver: WebDriver
        Una instancia del navegador WebDriver.

    menu_xpath: str
        El XPath del botón del menú del gráfico.

    button_index: int
        El índice del botón en la lista de botones del menú.

    Retorno:
    -------
    None
        Esta función no retorna ningún valor.
    """
    pbar.set_description("Abriendo Opciones de la tabla")
    menu_buttons = driver.find_elements(By.XPATH, menu_xpath)
    if button_index < len(menu_buttons):
        menu_button = menu_buttons[button_index]
        menu_button.click()
        time.sleep(5)  # Esperar para asegurar que el menú se abre completamente
        pbar.update(1)

def handle_export_data(pbar: tqdm, driver: WebDriver, export_xpath: str, button_name: str) -> None:
    """
    Exporta los datos haciendo clic en el botón de exportación basado en el nombre accesible.

    Parámetros:
    ----------
    pbar: tqdm
        Un objeto de tipo `tqdm` que representa la barra de progreso.

    driver: WebDriver
        Una instancia del navegador WebDriver.

    export_xpath: str
        El XPath del botón de exportación.

    button_name: str
        El nombre accesible del botón de exportación.

    Retorno:
    -------
    None
        Esta función no retorna ningún valor.
    """
    pbar.set_description("Exportando los datos")
    export_buttons = driver.find_elements(By.XPATH, export_xpath)
    for export_btn in export_buttons:
        if export_btn.accessible_name == button_name:
            export_btn.click()
            time.sleep(5)  # Esperar para asegurar que la exportación se procesa
    pbar.update(1)


def confirm_export(pbar: tqdm, driver: WebDriver, confirm_xpath: str) -> None:
    """
    Confirma la exportación haciendo clic en el botón de confirmación.

    Parámetros:
    ----------
    pbar: tqdm
        Un objeto de tipo `tqdm` que representa la barra de progreso.

    driver: WebDriver
        Una instancia del navegador WebDriver.

    confirm_xpath: str
        El XPath del botón de confirmación de exportación.

    Retorno:
    -------
    None
        Esta función no retorna ningún valor.
    """
    pbar.set_description("Confirmando exportación")
    confirm_export_btn = driver.find_element(By.XPATH, confirm_xpath)
    confirm_export_btn.click()
    time.sleep(30)  # Esperar para asegurar que la confirmación se procesa
    pbar.update(1)


def handle_filters(pbar: tqdm, driver: WebDriver, select_option="select_option_21"):
    pbar.set_description("Aplicando filtros")
    wait = WebDriverWait(driver, 10)
    date_filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//control-layout-wrapper[@class="datepicker"]')))
    date_filter_button.click()

    date_filter_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//md-select[@ng-model="$ctrl.selectedDateRangeOption"]'))
    )
    date_filter_button.click()

    date_range_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//md-option//div[contains(text(), "{OPTIONS_VALUES[select_option]}")]'))
    )
    date_range_option.click()

    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "md-raised")]'))
    )
    confirm_button.click()

    time.sleep(5)  # Esperar para asegurar que la confirmación se procesa
    pbar.update(1)
