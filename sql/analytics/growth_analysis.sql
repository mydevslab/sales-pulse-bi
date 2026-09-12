-- =============================================================================
-- QUERY ANALÍTICA: Análise de Crescimento MoM (Month-over-Month) e YoY (Year-over-Year)
-- Utiliza Window Functions (LAG e OVER) para inteligência temporal performática no DW.
-- =============================================================================

WITH montly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS sales_month,
        SUM(net_revenue) AS current_net_revenue,
        SUM(gross_margin) AS current_gross_margin,
        COUNT(DISTINCT order_id) AS total_orders
    FROM fact_sales
    WHERE status IN ("Entregue", "Faturado")
    GROUP BY DATE_TRUNC('month', order_date)::DATE
),
windowed_metrics AS (
    SELECT
        sales_month,
        current_net_revenue,
        current_gross_margin,
        total_orders,
        -- Lag de 1 Mês (MoM)
        LAG(current_net_revenue, 1) OVER (ORDER BY sales_month) AS prev_month_revenue, 
        -- Lag de 12 Meses (YoY)
        LAG(current_net_revenue, 12) OVER (ORDER BY sales_month) AS prev_year_revenue
    FROM monthly_revenue
)
SELECT
    sales_month,
    current_net_revenue,
    prev_month_revenue,
    ROUND(
        COALESCE((current_net_revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0) * 100, 0),
        2
    ) AS mom_growth_pct,
    prev_year_revenue,
    ROUND(
        COALESCE((current_net_revenue - prev_year_revenue) / NULLIF(prev_year_revenue, 0) * 100, 0),
        2
    ) AS yoy_growth_pct,
    current_gross_margin,
    ROUND(
        COALESCE((current_gross_margin / NULLIF(current_net_revenue, 0) * 100, 0), AS gross_margin_pct)
    )
FROM windowed_metrics
ORDER BY sales_month DESC;