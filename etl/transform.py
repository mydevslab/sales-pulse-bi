import logging
import pandas as pd

logger = logging.getLogger(name)


def transform(
    df_cust: pd.DataFrame,
df_prod: pd.DataFrame,
df_sales: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Aplica regras de tratamento de nulos e padronização nas tabelas dimensionais.

    Returns:
        tuple contendo (df_cust_treated, df_prod_treated, df_sales_treated)
    """

    logger.info("Iniciando TRANSFORMAS nas tabelas dimensionais...")

    # 1. Tratamento da dimenção Clientes
    df_cust_treated = df_cust.copy()
    df_cust_treated['region'] = df_cust_treated['region'].fillna("Não Informado")
    df_cust_treated['segment'] = df_cust_treated['segment'].fillna("Geral")

    # 2. Tratamento da dimensão Produtos
    df_prod_treated = df_prod.copy()
    df_prod_treated['category'] = df_prod_treated['category'].fillna("Sem Categoria")

    # 3. Tratamento da dimensão Vendedores
    df_sales_treated = df_sales.copy()
    df_sales_treated['region'] = df_sales_treated['region'].fillna("Geral")

    logger.info("Transformações dimensionais concluídas com sucesso.")
    return df_cust_treated, df_prod_treated, df_sales_treated


def merge_fact_sales(
    df_items: pd.DataFrame,
    df_orders: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cruza os itens dos pedidos com os cabeçalhos válidos para compor a Tabela Fato unificada.
    Calcula margem de lucro bruta ($) e percentual (%).

    """

    logger.info("Construind Fato de Venda (join order_items + orders)...")

    fact_df = pd.merge(
        df_items,
        df_orders[['order_id', 'customer_id', 'sales_rep_id', 'channel', 'order_date', 'status']],
        on='order_id',
        how='inner'
    )

    # Cálculos operacionais de margem bruta
    fact_df['gross_margin'] = (fact_df['net_revenue'] - fact_df['total_cost']).round(2)
    fact_df['gross_margin_pct'] = (fact_df['gross_margin'] / fact_df['net_revenue'].replace(0, pd.NA)).round(4).fillna(0.0)

    logger.info("Fato de Vendas gerada com %d linhas operacionais.", len(fact_df))

    return fact_df
