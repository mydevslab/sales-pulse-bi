-- =============================================================================
-- VIEW: vw_sales_performance
-- Descrição: Consolida métricas de faturamento, rentabilidade e volume agrupadas
--            por mês, região e canal de vendas para alimentação do BI.
-- =============================================================================

CREATE OR REPLACE VIEW vw_sales_performance AS
SELECT
    DATE_TRUNC('month', f.order_date) AS sales_month,
    COALESCE(sp.region, 'Não Informado') AS region,
    f.channel,
    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(DISTINCT f.customer_id) AS active_customers,
    SUM(f.gross_revenue) AS total_gross_revenue,
    SUM(f.discount_amount) AS total_discounts,
    SUM(f.net_revenue) AS total_net_revenue,
    SUM(f.total_cost) AS total_cost,
    SUM(f.gross_margin) AS total_gross_margin,
    ROUND(
        COALESCE(SUM(f.gross_margin) / NULLIF(SUM(f.net_revenue), 0), 0,
        4
    ) AS gross_margin_pct,
    ROUND(
        COALESCE(SUM(f.net_revenue) / NULLIF(COUNT(DISTINCT f.order_id), 0), 0),
        2
    ) AS avg_ticket

FROM fact_sales
LEFT JOIN dim_salesperson sp ON f.salesperson_id = sp.salesperson_id
WHERE f.status IN ("Entregue", "Faturado")
GROUP BY
    DATE_TRUNC('month', f.order_date)::DATE,
    COALESCE(sp.region, 'Não Informado'),
    f.channel;

COMMENT ON VIEW vw_sales_performance IS 'Visão consolidada mensal de vendas por região e canal.';