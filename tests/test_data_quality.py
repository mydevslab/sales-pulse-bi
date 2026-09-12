import pytest
import pandas as pd
from etl.validate import DataQualityEngine
from etl.transform import transform_dimensions, merge_fact_sales


@pytest.fixture
def sample_items_df():
    """Fixture que fornece um DataFrame de itens com anomalias controladas."""
    return pd.DataFrame([
        {
            "item_id": "ITEM-001",
            "order_id": "PED-100",
            "product_id": "PROD-001",
            "quantity": 10,
            "unit_price": 50.0,
            "unit_cost": 30.0,
            "gross_revenue": 500.0,
            "discount_amount": 50.0,
            "net_revenue": 450.0,
            "total_cost": 300.0
        },
        # Anomalia 1: Chave duplicada (ITEM-001)
        {
            "item_id": "ITEM-001",
            "order_id": "PED-100",
            "product_id": "PROD-001",
            "quantity": 10,
            "unit_price": 50.0,
            "unit_cost": 30.0,
            "gross_revenue": 500.0,
            "discount_amount": 50.0,
            "net_revenue": 450.0,
            "total_cost": 300.0
        },
        # Anomalia 2: Quantidade negativa
        {
            "item_id": "ITEM-002",
            "order_id": "PED-101",
            "product_id": "PROD-002",
            "quantity":-5,
            "unit_price": 20.0,
            "unit_cost": 10.0,
            "gross_revenue": 100.0,
            "discount_amount": 0.0,
            "net_revenue": 100.0,
            "total_cost": 50.0
        },
        # Anomalia 3: Receita bruta negativa
        {
            "item_id": "ITEM-003",
            "order_id": "PED-102",
            "product_id": "PROD-003",
            "quantity": 2,
            "unit_price": 100.0,
            "unit_cost": 50.0,
            "gross_revenue":-200.0,
            "discount_amount": 0.0,
            "net_revenue": 200.0,
            "total_cost": 100.0
        },
        # Anomalia 4: Receita líquida maior que receita bruta
        {
            "item_id": "ITEM-004",
            "order_id": "PED-103",
            "product_id": "PROD-004",
            "quantity": 1,
            "unit_price": 100.0,
            "unit_cost": 50.0,
            "gross_revenue": 100.0,
            "discount_amount": 0.0,
            "net_revenue": 150.0,
            "total_cost": 50.0
        }
    ])


@pytest.fixture
def sample_orders_df():
    """Fixture que fornece um DataFrame de pedidos com datas normais e anômala."""
    return pd.DataFrame([
        {
            "order_id": "PED-100",
            "customer_id": "CLI-001",
            "salesperson_id": "VEN-001",
            "channel": "Inside Sales",
            "order_date": "2024-05-15",
            "status": "Entregue"
        },
        # Data futura fora do escopo
        {
            "order_id": "PED-104",
            "customer_id": "CLI-002",
            "salesperson_id": "VEN-002",
            "channel": "E-commerce B2B",
            "order_date": "2030-01-01",
            "status": "Entregue"
        }
    ])

# -----------------------------------------------------------------------------
# TESTES DE DATA QUALITY
# -----------------------------------------------------------------------------


def test_validate_fact_items_deduplication(sample_items_df):
    """Garante que itens duplicados por `item_id` sejam removidos."""
    dq = DataQualityEngine()
    clean_df = dq.validate_fact_items(sample_items_df)
    
    assert len(clean_df[clean_df["item_id"] == "ITEM-001"]) == 1


def test_validate_fact_items_removes_invalid_quantities_and_revenues(sample_items_df):
    """Garante a eliminação de quantidades <= 0 e receitas inconsistentes."""
    dq = DataQualityEngine()
    clean_df = dq.validate_fact_items(sample_items_df)
    
    # Resta apenas o ITEM-001 válido
    assert len(clean_df) == 1
    assert clean_df.iloc[0]["item_id"] == "ITEM-001"


def test_validate_orders_filters_future_dates(sample_orders_df):
    """Garante que pedidos com datas futuras fora do limite sejam desconsiderados."""
    dq = DataQualityEngine()
    clean_orders = dq.validate_orders(sample_orders_df)
    
    assert len(clean_orders) == 1
    assert clean_orders.iloc[0]["order_id"] == "PED-100"


def test_data_quality_report_generation(sample_items_df, sample_orders_df):
    """Verifica se o relatório final de audit de Data Quality é gerado corretamente."""
    dq = DataQualityEngine()
    dq.validate_fact_items(sample_items_df)
    dq.validate_orders(sample_orders_df)
    
    report_df = dq.get_report_df()
    assert len(report_df) == 2
    assert "quality_score_pct" in report_df.columns
    assert "dataset" in report_df.columns

# -----------------------------------------------------------------------------
# TESTES DE TRANSFORMAÇÃO E CÁLCULO
# -----------------------------------------------------------------------------


def test_transform_dimensions_null_handling():
    """Valida o preenchimento por valores default nos nulos das dimensões."""
    df_cust = pd.DataFrame([{"customer_id": "C1", "region": None, "segment": None}])
    df_prod = pd.DataFrame([{"product_id": "P1", "category": None}])
    df_sales = pd.DataFrame([{"salesperson_id": "S1", "region": None}])

    cust_t, prod_t, sales_t = transform_dimensions(df_cust, df_prod, df_sales)

    assert cust_t.iloc[0]["region"] == "Não Informado"
    assert cust_t.iloc[0]["segment"] == "Geral"
    assert prod_t.iloc[0]["category"] == "Sem Categoria"
    assert sales_t.iloc[0]["region"] == "Geral"


def test_merge_fact_sales_calculations():
    """Testa os cálculos de margem bruta ($) e percentual (%)."""
    df_items = pd.DataFrame([{
        "item_id": "I1",
        "order_id": "O1",
        "product_id": "P1",
        "quantity": 10,
        "net_revenue": 100.0,
        "total_cost": 60.0
    }])
    
    df_orders = pd.DataFrame([{
        "order_id": "O1",
        "customer_id": "C1",
        "salesperson_id": "S1",
        "channel": "Direto",
        "order_date": "2024-01-01",
        "status": "Entregue"
    }])

    fact_df = merge_fact_sales(df_items, df_orders)

    assert len(fact_df) == 1
    assert fact_df.iloc[0]["gross_margin"] == 40.0
    assert fact_df.iloc[0]["gross_margin_pct"] == 0.40
