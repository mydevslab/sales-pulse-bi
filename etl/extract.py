import os
import logging
import pandas as pd
from etl.config import RAW_DATA_PATH

logger = logging.getLogger(__name__)


def extract_raw_data() -> dict[str, pd.DataFrame]:
    """
    Lê todos os arquivos CSV brutos da pasta data/raw/ e retorna um dicionário de DataFrames
    Returns:
    dict[str, pd.DataFrame]: Dicionário contendo os DataFrames extraídos.
    """
    logger.info("Iniciando fase de EXTRAÇÃO de dados brutos da pasta %s...", RAW_DATA_PATH)

    datasets = {
        "customers": "customers.csv",
        "products": "products.csv",
        "salespeople": "salespeople.csv",
        "orders": "orders.csv",
        "orders_items": "orders_items.csv",
        "targets": "targets.csv",
    }

    raw_dfs = {}

    for key, filename in datasets.items():
        file_path = os.path.join(RAW_DATA_PATH, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {file_path}")
        
        df = pd.read_csv(file_path)
        raw_dfs[key] = df
        logger.info("Extratído '%s': %d registros encontrados.", key, len(df))

    logger.info("Extração concluída com sucesso (d% tabelas carregadas em memória).", len(raw_dfs))
    
    return raw_dfs

