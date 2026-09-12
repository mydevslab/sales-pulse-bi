import logging
import pandas as pd

logger = logging.getLogger(name)


class DataQualityEngine:
    """
    Engine de Data Quality responsável por auditar, higienizar e gerar relatórios sobre inconsistências encontradas nos dados brutos.
    """

    def init(self):
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

        # 1. Duplicidade por chave primária
        df_clean = df_items.drop_duplicates(subset=['item_id'], keep='first')
        dupes_removed = initial_len - len(df_clean)

        # 2. Valores zerados ou negativos em quantidade e receita bruta

        invalid_qty = len(df_clean[df_clean['quantinty'] <= 0])
        invalid_rev = len([df_clean[df_clean['gross_revenue']] < 0])

        df_clean = df_clean[
            (df_clean['quantity'] > 0) & 
            (df_clean['gross_revenue' >= 0]) & 
            (df_clean['net_revenue'] >= 0)
        ]

        # 3. Validação de Receita Líquida vs Receita Bruta
        invalid_net = len(df_clean[df_clean['net_revenue'] > df_clean['gross_revenue']])
        df_clean = df_clean[df_clean['net_revenue'] <= df_clean['gross_revenue']]

        valid_count = len(df_clean)
        rejected_count = initial_len - valid_count
        quality_score = round((valid_count / initial_len) * 100, 2) if initial_len > 0 else 100.0

        details = (f"Removidos: {dupes_removed} duplicados, {invalid_qty} qty <= 0, "
        f"{invalid_rev} receita bruta < 0, {invalid_net} receita líquida > bruta")

        self.report.append({
            "dataset": "fact_sales_items",
            "total_records": initial_len,
            "valid_records": valid_count,
            "rejected_records": rejected_count,
            "quality_score_pct": quality_score,
            "details": details,
        })

        logger.info("DQ audit em order_items: Score %.2f%% (%d mantidos, %d rejeitados).",
                quality_score, valid_count, rejected_count)
        
        return df_clean

    def validate_orders(self, df_orders: pd.DataFrame) -> pd.DataFrame:
        """
        Valida a tabela de cabeçalhos de pedidos.
        Regras aplicadas:
        1. Conversão de datas e remoção de registros nulos.
        2. Remoção de datas futuras fora do limite do projeto (ex: 2026-12-31).
        """

        initial_len = len(df_orders)
        df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], errors='coerce')

        max_valid_date = pd.to_datetime("2026-12-31")
        df_clean = df_orders[
            (df_orders['order_date'].notnull()) & 
            (df_orders['order_date'] <= max_valid_date)
        ].copy()

        # 
        df_clean['order_date'] = df_clean['order_date'].dt.strftime("%Y-%m-%d")

        valid_count = len(df_clean)
        rejected_count = initial_len - valid_count
        quality_score = round((valid_count / initial_len) * 100, 2) if initial_len > 0 else 100.0

        self.report.append({
            "dataset": "orders",
            "total_records": initial_len,
            "valid_records": valid_count,
            "rejected_records": rejected_count,
            "quality_score_pct": quality_score,
            "details": f"Removidos {rejected_count} pedidos com datas nulas ou fora do escopo (futuras)",
        })
        
        logger.info("DQ audit em orders: Score %.2f%% (%d mantidos, %d rejeitados).",
                quality_score, valid_count, rejected_count)

        return df_clean

    def get_report_df(self) -> pd.DataFrame:
        """
        Retorna o relatório compliado de Data Quality como DataFrame.
        """

        return pd.DataFrame(self.report)
