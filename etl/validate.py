import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataQualityEngine:
    """
    Engine de Data Quality responsável por auditar, higienizar e gerar relatórios sobre inconsistências encontradas nos dados brutos.
    """

    def __init__(self):
        self.report = []

    def validate_fact_items(self, df_items: pd.DataFrame) -> pd.DataFrame:
        """
        Valida e higieniza a tabela de itens de pedidos.
        Regras aplicadas:
        1. Desduplicação por item_id.
        2. Remoção de quantidades <= 0.
        3. Remoção de faturamentos/receitas negativas.
        4. Invariante: net_revenue <= gross_revenue.
        """

        initial_len = len(df_items)

        # 1. Checagem de chave primária duplicada
        df_clean = df_items.drop_duplicates(subset=['item_id'], keep='first')
        dupes_removed = initial_len - len(df_clean)

        # 2. Identificar quantidades <= 0 e receitas < 0
        invalid_qty = len(df_clean[df_clean['quantity'] <= 0])
        invalid_rev = len(df_clean[df_clean['gross_revenue'] < 0])

        # 3. Filtrar registros com quantidade > 0 e receitas >= 0
        df_clean = df_clean[
            (df_clean['quantity'] > 0) & 
            (df_clean['gross_revenue'] >= 0) & 
            (df_clean['net_revenue'] >= 0)
        ]

        # 4. Regra da Receita Líquida <= Receita Bruta
        invalid_net = len(df_clean[df_clean['net_revenue'] > df_clean['gross_revenue']])
        df_clean = df_clean[df_clean['net_revenue'] <= df_clean['gross_revenue']]

        valid_count = len(df_clean)
        rejected_count = initial_len - valid_count
        score_pct = round((valid_count / initial_len) * 100, 2) if initial_len > 0 else 100.0

        self.report.append({
            "dataset": "fact_sales_items",
            "total_records": initial_len,
            "valid_records": valid_count,
            "rejected_records": rejected_count,
            "quality_score_pct": score_pct,
            "details": f"Removidos: {dupes_removed} duplicados, {invalid_qty} qty inválida, {invalid_rev} receita negativa, {invalid_net} líq > bruta."
        })

        logger.info("Fact Items Quality Score: %s%%", score_pct)
        
        return df_clean

    def validate_orders(self, df_orders: pd.DataFrame) -> pd.DataFrame:
        """
        Valida a tabela de cabeçalhos de pedidos.
        Regras aplicadas:
        1. Conversão de datas e remoção de registros nulos.
        2. Remoção de datas futuras fora do limite do projeto (ex: 2026-12-31).
        """

        initial_len = len(df_orders)
        df_clean = df_orders.copy()
        df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], errors='coerce')

        # Remover datas futuras além do limite do projeto (2026-12-31)
        max_valid_date = pd.to_datetime("2026-12-31")
        df_clean = df_clean[
            (df_clean['order_date'].notnull()) & 
            (df_clean['order_date'] <= max_valid_date)
        ]
 
        df_clean['order_date'] = df_clean['order_date'].dt.strftime("%Y-%m-%d")

        valid_count = len(df_clean)
        rejected_count = initial_len - valid_count
        score_pct = round((valid_count / initial_len) * 100, 2) if initial_len > 0 else 100.0

        self.report.append({
            "dataset": "orders",
            "total_records": initial_len,
            "valid_records": valid_count,
            "rejected_records": rejected_count,
            "quality_score_pct": score_pct,
            "details": f"Removidos {initial_len - valid_count} registros com datas nulas ou futuras."
        })
        
        return df_clean

    def get_report_df(self) -> pd.DataFrame:
        """
        Retorna o relatório compliado de Data Quality como DataFrame.
        """

        return pd.DataFrame(self.report)
