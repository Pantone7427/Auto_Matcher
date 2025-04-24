import os
import logging
from typing import Dict, Any, List
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from utils.logger import get_logger  # Importa la función para obtener el logger

# Obtén el logger usando la función get_logger
logger = get_logger(__name__)

def generar_pdf_individual(
    soporte_path: str,
    tb_info: Any,
    output_dir: str
) -> str:
    """
    Genera un PDF individual combinando la imagen del soporte y datos de la TB.

    Args:
        soporte_path (str): Ruta a la imagen del soporte.
        tb_info (pandas.Series): Serie con datos de la transacción ('No Egreso' y 'Girado a').
        output_dir (str): Carpeta donde guardar el PDF.

    Returns:
        str: Ruta al PDF generado.
    """
    if not os.path.isfile(soporte_path):
        logger.error(f"No se encontró la imagen del soporte: {soporte_path}")
        raise FileNotFoundError(f"Imagen no encontrada: {soporte_path}")

    os.makedirs(output_dir, exist_ok=True)

    # Definir nombre del PDF
    no_egreso = str(tb_info.get('No Egreso', 'NA')).strip()
    girado_a = str(tb_info.get('Girado a', 'NA')).strip()
    filename = f"{no_egreso} - {girado_a}.pdf"
    output_path = os.path.join(output_dir, filename)

    try:
        # Crear canvas ReportLab
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        # Dibujar imagen del soporte
        img = Image.open(soporte_path)
        img_width, img_height = img.size
        aspect = img_height / img_width
        max_width = width * 0.8
        max_height = height * 0.5

        # Ajustar tamaño manteniendo proporción
        if img_width > max_width:
            img_width = max_width
            img_height = img_width * aspect
        if img_height > max_height:
            img_height = max_height
            img_width = img_height / aspect

        x_img = (width - img_width) / 2
        y_img = height - img_height - 50
        c.drawImage(soporte_path, x_img, y_img, img_width, img_height)

        # Escribir datos de la TB debajo de la imagen
        text_y = y_img - 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, text_y, f"No Egreso: {no_egreso}")
        c.drawString(50, text_y - 20, f"Girado a: {girado_a}")

        c.showPage()
        c.save()

        logger.info(f"PDF generado: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Error generando PDF para {soporte_path}: {e}")
        raise


def generar_pdfs(
    resultados: List[Dict[str, Any]],
    output_dir: str
) -> List[str]:
    """
    Genera múltiples PDFs individuales para cada resultado emparejado.

    Args:
        resultados: Lista de dicts con claves 'soporte', 'tb_info', 'estado'.
        output_dir: Carpeta de salida para los PDFs.

    Returns:
        List[str]: Rutas de los PDFs generados.
    """
    pdf_paths = []
    for res in resultados:
        if res['estado'] == 'ABONADO' and res['tb_info'] is not None:
            path = generar_pdf_individual(
                res['soporte'], res['tb_info'], output_dir
            )
            pdf_paths.append(path)
        else:
            logger.info(f"Saltando generación de PDF para soporte con estado {res['estado']}")
    return pdf_paths


if __name__ == '__main__':
    import argparse
    from matcher import matchear_soportes
    from core.excel_reader import leer_excel, guardar_excel

    parser = argparse.ArgumentParser(description='Genera PDFs individuales')
    parser.add_argument('soportes_dir', help='Directorio con imágenes de soportes')
    parser.add_argument('excel_path', help='Ruta al Excel de TBs')
    parser.add_argument('output_dir', help='Directorio de salida para PDFs')
    args = parser.parse_args()

    # Leer soporte y emparejar
    pdfs = []
    from core.extractor import extract_soportes
    soporte_paths = [os.path.join(args.soportes_dir, f) for f in os.listdir(args.soportes_dir) if f.lower().endswith(('.png','.jpg','.jpeg'))]
    df = leer_excel(args.excel_path)
    resultados = matchear_soportes(soporte_paths, df)
    guardar_excel(df, args.excel_path)
    pdfs = generar_pdfs(resultados, args.output_dir)

    print("PDFs generados:")
    for p in pdfs:
        print(p)
