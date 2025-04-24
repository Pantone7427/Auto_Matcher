import logging

def get_logger(name: str = __name__) -> logging.Logger:
    """
    Crea y devuelve un logger configurado con un formato estándar para consola.

    Args:
        name (str): Nombre del logger. Por defecto, el módulo actual.

    Returns:
        logging.Logger: Instancia de logger lista para usar.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
