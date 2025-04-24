import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
from typing import Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


def preprocesar_imagen(img: Image.Image) -> Image.Image:
    img = img.convert("L")
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    return img


def extraer_estado(img: Image.Image) -> str:
    try:
        texto = pytesseract.image_to_string(img, lang='spa')
        for linea in texto.splitlines():
            if 'abonado' in linea.lower():
                logger.info("Estado encontrado: ABONADO")
                return "ABONADO"
        logger.info("Estado no encontrado o diferente a 'ABONADO'")
        return "RECHAZADO"
    except Exception as e:
        logger.error(f"Error en OCR de estado: {e}")
        return "ERROR"


def extraer_valor(img: Image.Image) -> float:
    try:
        texto = pytesseract.image_to_string(img, lang='spa')
        coincidencias = re.findall(r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})", texto)
        if coincidencias:
            valor_texto = coincidencias[-1].replace(".", "").replace(",", ".")
            valor = round(float(valor_texto), 2)
            logger.info(f"Valor extraído: {valor}")
            return valor
        else:
            logger.warning("No se encontró valor en el texto OCR")
            return -1.0
    except Exception as e:
        logger.error(f"Error en OCR de valor: {e}")
        return -1.0


def procesar_soporte(imagen_path: str) -> Tuple[str, float]:
    try:
        img = Image.open(imagen_path)
        img_proc = preprocesar_imagen(img)
        estado = extraer_estado(img_proc)
        valor = extraer_valor(img_proc)
        return estado, valor
    except Exception as e:
        logger.error(f"Error procesando soporte '{imagen_path}': {e}")
        return "ERROR", -1.0
