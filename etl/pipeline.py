import time
import logging
from etl.config import setup_logging, DATABASE_URL
from etl.extract import extract_raw_data
from etl.validate import DataQualityEngine
from etl.transform import transform_dimensions, merge_fact_sales
from etl.load import PostgresLoader


def run_pipeline():
    """Executa o pipeline completo de ETL (Extrato, Validate, Transform, Load)"""

    setup_logging()
    logger = logging.getLogger("ETL_Ochestrator")

    logger.info("==================================================")
    logger.info("🚀 INICIANDO PIPELINE DE ETL - SALES PULSE BI")
    logger.info("==================================================")

    start_time = time.time()

    try:
        # 1. Extração
        raw_data = extract_raw_data()

        # 2. Validação & Data Quality
        logger.info("--- ETAPA: Data Quality & Sanitização ---")
        dq = DataQualityEngine()
        df_items_clean = dq.validate_fact_items(raw_data['order_items'])
        df_orders_clean = dq.validate_orders(raw_data["orders"])

        # 3. Transformação
        logger.info("--- ETAPA: Transformação Dimensional e Modelagem Fato ---")
        df_cust_t, df_prod_t, df_sales_t = transform_dimensions(
            df_cust=raw_data["customers"],
            df_prod=raw_data["products"],
            df_sales=raw_data["salespeople"],
        )

        fact_sales = merge_fact_sales(df_items_clean, df_orders_clean)
        
        # 4. Carga no Data Warehouse (PostgreSQL)
        logger.info("--- ETAPA: Carregamento no PostgreSQL DW ---")
        loader = PostgresLoader(DATABASE_URL)

        loader.load_df(df_cust_t, "dim_customer")
        loader.load_df(df_prod_t, "dim_product")
        loader.load_df(df_sales_t, "dim_salesperson")
        loader.load_df(fact_sales, "fact_sales")
        loader.load_df(raw_data["targets"], "fact_targets")

        # Carrega relatório de Data Qualiy para auditoria no BI
        dq_report_df = dq.get_report_df()
        loader.load_df(dq_report_df, "stg_data_quality_report")

        elapsed = round(time.time() - start_time, 2)
        logger.info("==================================================")
        logger.info("✨ PIPELINE EXECUTADO COM 100%% DE SUCESSO EM %s SEGUNDOS!", elapsed)
        logger.info("==================================================")

    except Exception as e:
        logger.critical("❌ FALHA FATAL NO PIPELINE ETL: %s", str(e), exc_info=True)
        raise e


if __name__ == "__main__":
    run_pipeline()
