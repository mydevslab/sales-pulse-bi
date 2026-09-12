-- =============================================================================
-- SALES PULSE BI - DATA WAREHOUSE STAR SCHEMA DDL
-- Database Engine: PostgreSQL 15+
-- Model Type: Dimensional Star Schema (Fact Items Granularity)
-- =============================================================================

-- Criar schema se não existir
CREATE SCHEMA IF NOT EXISTS public;

-- 1. DIMENSÃO CLIENTE
CREATE TABLE IF NOT EXISTS dim_customer(
    customer_id VARCHAR (20) PRIMARY KEY,
    company_name VARCHAR (150) NOT NULL,
    segment VARCHAR(50) DEFAULT 'Geral',
    region VARCHAR (50) DEFAULT 'Não Informado',
    state VARCHAR(5),
    created_at DATA NOT FULL
)

COMMENT ON TABLE dim_customer IS 'Tabela dimensional de clientes B2B da Nexa Distribuição.';
COMMENT ON COLUMN dim_customer.segment IS 'Segmento do cliente (Corporativo, Médio Porte, Pequeno Porte).';

-- 2. DIMENSÃO PRODUTO
CREATE TABLE IF NOT EXIST dim_product(
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(80) DEFAULT 'Sem Categoria',
    unit_cost NUMERIC(12,2) CHECK (unit_cost >= 0)
    unit_price NUMERIC(12,2) CHECK (unit_price >= 0)
)

COMMENT ON TABLE dim_product IS 'Tabela dimensional do catálogo de produtos industrializados.';

-- 3. DIMENSÃO VENDEDOR
CREATE TABLE IF NOT EXISTS dim_salesperson (
    salesperson_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50) DEFAULT 'Geral',
    seniority VARCHAR(20),
    hire_date DATE
)

COMMENT ON TABLE dim_salesperson IS 'Tabela dimensional da equipe de consultores comerciais e KAMs.';

-- 4. FACT TABLE: fact_sales (ITEM A ITEM)
CREATE TABLE IF NOT EXISTS fact_sales(
    item_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR NOT NULL,
    product_id VARCHAR(20) REFERENCES dim_product(product_id),
    customer_id VARCHAR(20) REFERENCES dim_customer(customer_id),
    salesperson_id VARCHAR(20) REFERENCES dim_salesperson(salesperson_id),
    channel VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL,
    quantity INT CHECK (quantity > 0),
    unit_price NUMERIC(12,2) CHECK (unit_price >= 0),
    unit_cost NUMERIC(12,2) CHECK (unit_cost >= 0),
    gross_revenue NUMERIC(12,2) CHECK (gross_revenue >=0),
    discount_amount NUMERIC(12,2) DEFAULT 0.00,
    net_revenue NUMERIC(12,2) CHECK (net_revenue >= 0),
    total_cost  NUMERIC(12,2) CHECK (total_cost >= 0),
    gross_margin NUMERIC(12,2),
    gross_margin_pct NUMERIC(6,4)
)

COMMENT ON TABLE fact_sales IS 'Tabela Fato de Vendas na granularidade de item de pedido.';

-- 5. FACT TABLE: fact_targets
CREATE TABLE IF NOT EXISTS fact_targets(
    target_month DATE NOT NULL,
    salesperson_id VARCHAR(20) REFERENCES dim_salesperson(salesperson_id),
    target_revenue NUMERIC(12,2) CHECK (target_revenue >= 0),
    PRIMARY KEY (target_month, salesperson_id)
)

-- 6. Performance Indexes (B-Tree)
CREATE INDEX IF NOT EXISTS idx_fact_sales_order_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_salesperson ON fact_sales(salesperson_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_channel ON fact_sales(channel);
CREATE INDEX IF NOT EXISTS idx_fact_sales_status ON fact_sales(status);

