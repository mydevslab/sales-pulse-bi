# Guia de Especificação Técnica dos Dashboards Executivos | Sales Pulse BI

Este documento especifica a arquitetura de informação, a hierarquia visual e a matriz de navegação dos dashboards desenvolvidos em Power BI para a Nexa Distribuição.

## 📐 1. Modelo de Dados & Relacionamentos (Star Schema)

No Power BI Desktop, garanta as seguintes cardinalidades no modelo semântico:

| Tabela Origem(1) | Tabela Destino(N) | Chave de Relacionamento | Direção do Filtro |
|------------------|-------------------|-------------------------|-------------------|
`dim_date` | `fact_sales`  |  `Date` = `order_date`  | Única (Single)
dim_datefact_targets | Date = target_month | Única (Single)
dim_customer | fact_salescustomer_id | Única (Single)
dim_product | fact_salesproduct_id | Única (Single)
dim_salespersonfact_salessalesperson_idÚnica (Single)
dim_salesperson | fact_targets | salesperson_id | Única (Single)

## 🖥️ 2. Estrutura das Páginas do Relatório

O relatório é composto por 6 páginas executivas e operacionais:

### 📄 Página 1: Executive Overview (Visão Geral de Performance Comercial)

- **Objetivo:** Fornecer aos C-Levels e Diretores Comerciais um panorama imediato do faturamento, rentabilidade e alcance de metas.
- **Componentes Visuais:** 
    - **Top Cards (KPIs):** `Total Net Revenue ($)`, `Gross Margin %`, `Total Orders`, `Target Achievement %`, `YoY Growth %`.
    - **Gráfico Principal (Combo Chart):** Colunas empilhadas representando a Receita Líquida Mensal (`Total Net Revenue`) cruzadas com uma linha representando a Meta Mensal (`Total Target Revenue`).
    - **Gráfico Secundário (Bar Chart):** Receita Líquida por Região (`Sudeste`, `Sul`, `Nordeste`, etc.).
    - **Filtros Globais:** Ano/Mês (`dim_date`), Região, Canal de Venda.

### 📄 Página 2: Sales Performance & Team Ranking

- **Objetivo:** Avaliar o desempenho individual da equipe comercial, identificando vendedores de alta performance e consultores abaixo da meta.
- **Componentes Visuais:** 
    - **Matriz Comercial (Matrix Visual):** Vendedor > Região > Senioridade | Métrica: `Total Net Revenue`, `Total Target Revenue`, `Target Variance Amount`, `Target Achievement %`, `Average Ticket`.
    - **Gráfico de Dispersão (Scatter Plot):** Eixo X: `Total Orders` | Eixo Y: `Average Ticket` | Tamanho da Bolha: `Total Net Revenue` | Categoria: `Salesperson Name`.
    - **Cards Dinâmicos:** Top 1 Vendedor do Mês e Maior Ticket Médio.

### 📄 Página 3: Profitability & Product Mix

- **Objetivo:** Identificar as categorias e produtos mais lucrativos, diagnosticando itens com alta receita mas margem comprimida.
- **Componentes Visuais:** 
    - **Matriz de Quadrantes (Scatter Plot de Rentabilidade):** Eixo X: `Total Net Revenue` | Eixo Y: `Gross Margin %` | Detalhe: `product_name` | Linhas de Referência: Média de Receita e Margem Mínima de 25%.
    - **Gráfico de Pareto (Combo Chart):** Colunas: `Gross Margin` por Categoria | Linha: Margem Acumulada %.
    - **Tabela de Detalhamento:** Lista dos 10 Produtos com Menor Margem Bruta (Alerta Vermelho).
    
### 📄 Página 4: Customer Analytics & Curva ABCO

- **bjetivo:** Monitorar a saúde da base de clientes B2B, concentração de faturamento e risco de churn.
- **Componentes Visuais:** 
    - **Gráfico de Curva ABC:** Classificação de Clientes em Classe A (Top 80% Receita), Classe B (15%), e Classe C (5%).
    - **Donut Chart**: Distribuição de Faturamento por Segmento de Cliente (Corporativo, Médio Porte, Pequeno Porte).
    - **Tabela Operacional de Churn Risk:** Lista de Clientes sem pedidos registrados nos últimos 60/90 dias.
    
### 📄 Página 5: Target & Variance Analysis (Análise de Desvios)

- **Objetivo:** Explicar a variação matemática entre o planejado (Meta) e o realizado (Faturamento).
- **Componentes Visuais:** 
    - **Gráfico Cascata (Waterfall Chart):** Ponto de partida: `Total Target Revenue` | Pontes: Variações por Região e Canal | Ponto de Chegada: `Total Net Revenue`.
    - **Bar Chart Bicolor**: Vendedores em vermelho (`Target Variance Amount < 0`) e vendedores em verde (`Target Variance Amount >= 0`).
    
### 📄 Página 6: Data Quality & Governance Audit

- **Objetivo:** Exibir a auditoria do pipeline ETL aos Analytics Engineers e auditores internos.
- **Componentes Visuais:** 
    **- Gauge Visual:** `DQ Global Score Pct` (Alerta amarelo se < 98%).
    - `Tabela de Inconsistências:` Datasets auditados (`fact_sales_items`, `orders`), total de registros processados, total de rejeições e campo detalhado de motivos (details).
    
## 🎨 3. Guia de Identidade Visual e Cores (Theme Tokens)

- Primary Corporate: `#1E293B` (Slate Navy)
- Secondary / Highlights: `#0EA5E9` (Cyan Blue)
- Success / Meta Atingida: `#10B981` (Emerald Green)
- Warning / Alerta de Margem: `#F59E0B` (Amber)
- Danger / Abaixo da Meta: `#EF4444` (Crimson Red)
- Background Neutral: `#F8FAFC` (Light Gray)