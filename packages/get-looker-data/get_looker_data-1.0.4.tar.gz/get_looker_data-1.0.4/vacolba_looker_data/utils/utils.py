from tqdm import tqdm


def execute_with_progress(pbar: tqdm, description: str, func: callable, *args, **kwargs):
    """
    Ejecuta una función, actualiza la barra de progreso y muestra la descripción.

    Args:
        pbar (tqdm): La barra de progreso que se está actualizando.
        description (str): Descripción para el estado actual.
        func (callable): La función a ejecutar.
        *args: Argumentos posicionales para la función.
        **kwargs: Argumentos nombrados para la función.

    Returns:
        Cualquier cosa que retorne la función 'func'.
    """
    pbar.set_description(description)
    result = func(*args, **kwargs)
    pbar.update(1)
    return result