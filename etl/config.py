import os
import logging
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env, se existir
load_dotenv()

# Configurações de conexão com o PostgreSQL DW
DB_USER = os.getenv("DB_USER", "dw_admin")
DB_PASS = os.getenv("DB_PASS", "dw_secure_password123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nexa_dw")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Diretórios de Dados do Pipeline
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw")
STAGING_DATA_PATH = os.getenv("STAGING_DATA_PATH", "daa/staging")
PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", "data/processed")

# Nível de Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def setup_logging():
    """Configura o logger padrão para o pipeline ETL."""

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s-%(levelname)s-[%(filename)s:%(lineno)d]-%(message)s"
    )
