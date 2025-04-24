# app.py - Punto de entrada del sistema AutoMatcher

import sys
import logging
from gui.main_window import App

# Configurar logging global
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        logging.exception("Error al iniciar la aplicación:")
        sys.exit(1)


if __name__ == "__main__":
    main()
