import pandas as pd
from typing import Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


def leer_excel(excel_path: str, sheet_name: str = None) -> pd.DataFrame:
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name, dtype={'Valor': float})
        df = df.rename(columns=lambda x: x.strip())
        if 'usado' not in df.columns:
            df['usado'] = False
        else:
            df['usado'] = df['usado'].fillna(False)
        logger.info(f"Leído Excel con {len(df)} transacciones desde '{excel_path}'")
        return df
    except FileNotFoundError:
        logger.error(f"Archivo Excel no encontrado: {excel_path}")
        raise
    except Exception as e:
        logger.exception(f"Error leyendo Excel: {e}")
        raise


def guardar_excel(df: pd.DataFrame, excel_path: str) -> None:
    try:
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False)
        logger.info(f"Excel guardado con marcas de 'usado' en '{excel_path}'")
    except Exception as e:
        logger.error(f"Error guardando Excel: {e}")
        raise


def obtener_transaccion_libre(df: pd.DataFrame, valor_soporte: float, margen: float = 100.0) -> Tuple[int, pd.Series]:
    candidatos = df[
        (~df['usado']) &
        (df['Valor'].between(valor_soporte - margen, valor_soporte + margen))
    ]
    if not candidatos.empty:
        idx = candidatos.index[0]
        logger.info(f"Transacción libre encontrada en índice {idx} para valor {valor_soporte}")
        return idx, df.loc[idx]
    else:
        logger.warning(f"No se encontró transacción libre para valor {valor_soporte}")
        return -1, None


def marcar_usado(df: pd.DataFrame, idx: int) -> None:
    try:
        df.at[idx, 'usado'] = True
        logger.info(f"Transacción en índice {idx} marcada como usada.")
    except Exception as e:
        logger.error(f"Error marcando transacción usada: {e}")
        raise


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Leer y procesar Excel de TBs')
    parser.add_argument('excel_path', help='Ruta al archivo Excel')
    args = parser.parse_args()

    df = leer_excel(args.excel_path)
    print(df.head())