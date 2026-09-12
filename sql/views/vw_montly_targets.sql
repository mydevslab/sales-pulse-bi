-- =============================================================================
-- VIEW: vw_monthly_targets
-- Descrição: Compara a meta de receita mensal com a receita líquida realizada
--            por vendedor, calculando o desvio ($) e o percentual de atingimento.
-- =============================================================================

CREATE OR REPLACE VIEW vw_monthly_targets AS
WITH sales_montly AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS sales_montly,
        SUM(net_revenue) AS actual_revenue
    FROM fact_sales
    WHERE status IN ("Entregue", "Faturado")
    GROUP BY DATE_TRUNC('month', order_date)::DATE, salesperson_id
)
SELECT
    t.target_month,
    sp.salesperson_id,
    sp.name AS salesperson_name,
    COALESCE(sp.region, 'Geral') AS region,
    sp.seniority,
    t.target_revenue,
    COALESCE(s.actual_revenue, 0.00) AS actual_revenue,
    COALESCE(s.actual_revenue, 0.00) - t.target_revenue AS variance_amount,
    ROUND(
        COALESCE(s.actual_revenue, 0.00) / NULLIF(t.target_revenue, 0),
        4
    ) AS target_achievement_pct
    CASE
    WHEN COALESCE(s.actual_revenue, 0.00) >= t.target_revenue THEN 'Meta Atingida'
    ELSE 'Abaixo da Meta'
FROM fact_targets t
LEFT JOIN dim_salesperson sp ON t.salesperson_id = sp.salesperson_id
LEFT JOIN sales_montly s
    ON t.target_month = s.sales_month
    AND t.salesperson_id = s.salesperson_id

COMMENT ON VIEW vw_monthly_targets IS 'Comparativo mensal de meta x realizado por vendedor.';