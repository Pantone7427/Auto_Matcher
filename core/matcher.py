import logging
from typing import List, Dict, Any

from core.ocr_processor import procesar_soporte
from core.excel_reader import obtener_transaccion_libre, marcar_usado
import pandas as pd

logger = logging.getLogger(__name__)


def matchear_soportes(
    soporte_paths: List[str],
    df_tbs: pd.DataFrame,
    margen: float = 100.0
) -> List[Dict[str, Any]]:
    """
    Empareja soportes con transacciones bancarias.

    Args:
        soporte_paths: Lista de rutas a imágenes de soportes.
        df_tbs: DataFrame de TBs con columna 'usado'.
        margen: Margen en pesos para coincidencia de valores.

    Returns:
        Lista de diccionarios con la información de emparejamiento:
        {
            'soporte': ruta soporte,
            'estado': 'ABONADO'|'RECHAZADO'|'ERROR',
            'valor_soporte': float,
            'tb_idx': índice en df_tbs o None,
            'tb_info': Serie de la TB o None
        }
    """
    resultados = []

    for path in soporte_paths:
        estado, valor = procesar_soporte(path)
        resultado = {
            'soporte': path,
            'estado': estado,
            'valor_soporte': valor,
            'tb_idx': None,
            'tb_info': None
        }

        if estado != 'ABONADO':
            logger.info(f"Soporte rechazado: {path} con estado {estado}")
            resultados.append(resultado)
            continue

        idx, tb = obtener_transaccion_libre(df_tbs, valor, margen)
        if idx >= 0 and isinstance(tb, pd.Series):
            marcar_usado(df_tbs, idx)
            resultado['tb_idx'] = idx
            resultado['tb_info'] = tb
            logger.info(f"Soporte {path} emparejado con TB idx={idx}")
        else:
            logger.warning(f"No se emparejó TB para soporte {path}")

        resultados.append(resultado)

    return resultados


if __name__ == '__main__':
    import argparse
    import os
    from core.excel_reader import leer_excel, guardar_excel

    parser = argparse.ArgumentParser(description='Empareja soportes con TBs')
    parser.add_argument('soportes_dir', help='Directorio con imágenes de soportes')
    parser.add_argument('excel_path', help='Ruta al Excel de TBs')
    parser.add_argument('--margen', type=float, default=100.0,
                        help='Margen en pesos para emparejar')
    args = parser.parse_args()

    soporte_paths = [os.path.join(args.soportes_dir, f)
                     for f in sorted(os.listdir(args.soportes_dir))
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    df = leer_excel(args.excel_path)
    resultados = matchear_soportes(soporte_paths, df, args.margen)
    guardar_excel(df, args.excel_path)

    # Imprimir resumen
    for res in resultados:
        print(res)
