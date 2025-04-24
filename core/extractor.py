import os
import logging
from typing import List, Tuple

import pdfplumber
from PIL import Image
from utils.logger import get_logger

logger = get_logger(__name__)


def soporte_tiene_contenido(soporte_imagen: Image.Image, umbral_blanco: float = 0.98) -> bool:
    soporte_gris = soporte_imagen.convert("L")
    pixeles_totales = soporte_gris.width * soporte_gris.height
    pixeles_no_blancos = sum(1 for pixel in soporte_gris.getdata() if pixel < 240)
    proporcion_no_blancos = pixeles_no_blancos / pixeles_totales
    return proporcion_no_blancos > (1 - umbral_blanco)


def extract_soportes(
    pdf_path: str,
    output_dir: str,
    coordenadas: List[Tuple[float, float, float, float]] = None,
    umbral_blanco: float = 0.98
) -> List[str]:
    suport_paths: List[str] = []

    if not os.path.isfile(pdf_path):
        logger.error(f"No se encontró el PDF: {pdf_path}")
        raise FileNotFoundError(f"No se encontró el PDF: {pdf_path}")
    os.makedirs(output_dir, exist_ok=True)

    if coordenadas is None:
        coordenadas = [
            (0, 0, 612, 264),
            (0, 264, 612, 500),
            (0, 500, 612, 792)
        ]

    try:
        with pdfplumber.open(pdf_path) as pdf:
            logger.info(f"Abriendo PDF con {len(pdf.pages)} páginas")
            for page_num, page in enumerate(pdf.pages, start=1):
                page_img = page.to_image(resolution=72).original
                logger.info(f"Página {page_num}: tamaño {page.width}x{page.height} puntos")

                for idx, (x1, y1, x2, y2) in enumerate(coordenadas, start=1):
                    try:
                        soporte_img = page_img.crop((x1, y1, x2, y2))
                        if not soporte_tiene_contenido(soporte_img, umbral_blanco):
                            logger.info(f"Soporte vacío omitido: página {page_num}, región {idx}")
                            continue
                        nombre = f"soporte_p{page_num}_{idx}.png"
                        ruta = os.path.join(output_dir, nombre)
                        soporte_img.save(ruta)
                        suport_paths.append(ruta)
                        logger.info(f"Guardado soporte: {ruta}")
                    except Exception as e:
                        logger.error(f"Error al procesar soporte pagina {page_num}, idx {idx}: {e}")
    except Exception as e:
        logger.exception(f"Error al procesar el PDF: {e}")
        raise

    return suport_paths


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Extrae soportes bancarios de un PDF y guarda como imágenes'
    )
    parser.add_argument('pdf_path', help='Ruta al PDF de soportes')
    parser.add_argument('output_dir', help='Directorio de salida para imágenes')
    parser.add_argument('--umbral', type=float, default=0.98,
                        help='Umbral para omitir soportes vacíos (0-1)')
    args = parser.parse_args()

    try:
        extract_soportes(args.pdf_path, args.output_dir, umbral_blanco=args.umbral)
        logger.info("Extracción completada exitosamente.")
    except Exception as e:
        logger.error(f"La extracción falló: {e}")
