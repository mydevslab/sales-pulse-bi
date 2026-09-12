import logging
import pandas as pd
from sqlalchemy import create_engine

logger = logging.getLogger(name)


class PostgresLoader:
    """Módulo responsável por conectar ao DW PostgreSQL e persistence de DataFrames."""
    
    def __init__(self, connection_string:str):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)

    def load_df(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str='public',
        if_exists: str="replace"
    ) -> None:
        """
        Carrega um DataFrame pandas na tabela especificada no PostgreSQL.
        """

        try:
            with self.engine.begin() as conn:
                df.to_sql(
                    name=table_name,
                    con=conn,
                    schema=schema,
                    if_exists=if_exists,
                    index=False
                )
            
            logger.info("Carga concluída com sucesso na tabela '%s.%s' (%d registros).",
                        schema, table_name, len(df))
            
        except Exception as e:
            logger.error("Erro ao carregar dados na tabela '%s.%s:%s'", schema, table_name, str(e))
            raise e
