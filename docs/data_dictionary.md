# Dicionário de Dados | Nexa Distribuição DW (nexa_dw)

Este documento especifica a estrutura, tipos de dados, restrições e finalidades operacionais de todas as tabelas mantidas no Data Warehouse PostgreSQL (`nexa_dw`).

## 1. Tabelas Dimensionais (Dimensions)

### 1.1 `dim_customer`

Guarda as informações cadastrais e segmentação dos clientes B2B.

Coluna | Tipo de Dado | Nulo? | Chave | Descrição / Regra de Negócio
|------| ------------ | ----- | ----- | -----------------------------| 
customer_id | `VARCHAR(20)` | Não | PK | Identificador único do cliente (`CLI-00001`).
company_name | `VARCHAR(150)` | Não | - | Razão social ou nome fantasia da empresa.
segment | `VARCHAR(50)` | Não | - | Segmento comercial: `Corporativo`, `Médio Porte`, `Pequeno Porte` (Default: `Geral`).
region | `VARCHAR(50)` | Não | - | Região geográfica (Default: `Não Informado`).
state | `VARCHAR(5)` | Sim | - | UF de localização (ex: `SP`, `RJ`, `MG`).
created_at | `DATE` | Não | - | Data de cadastro do cliente no ERP.

### 1.2 `dim_product`

Catálogo de produtos industrializados comercializados.

Coluna | Tipo de Dado | Nulo? | Chave | Descrição / Regra de Negócio
|------| ------------ | ----- | ----- | -----------------------------| 
`product_id` | `VARCHAR(20)` | Não | PK | Código do produto (`PROD-0001`).
`product_name` | `VARCHAR(150)` | Não | - | Nome descritivo do produto.
`category` | `VARCHAR(80)` | Não | - | Categoria do produto (`Sem Categoria`).
`unit_cost` | `NUMERIC(12,2)` | Não | - | Custo unitário de aquisição/produção ($\ge 0$).
`unit_price` | `NUMERIC(12,2)` | Não | - | Preço público de tabela ($\ge 0$).


### 1.3 `dim_salesperson`

Equipe comercial de consultores, KAMs e representantes.

Coluna | Tipo de Dado | Nulo? | Chave | Descrição / Regra de Negócio
|------| ------------ | ----- | ----- | -----------------------------| 
salesperson_id | `VARCHAR(20)` | Não | PK | Código do vendedor (`VEN-001`).
name | `VARCHAR(100)`  | Não  | - | Nome completo do vendedor.
region | `VARCHAR(50)` | Não | - | Região de atuação responsável (Default: `Geral`).
seniority | `VARCHAR(30)` | Sim | - | Senioridade: Júnior, Pleno, Sênior, Key Account.
hire_date | `DATE` | Sim | - | Data de contratação.

## 2. Tabelas Fato (Fact Tables)

### 2.1 `fact_sales`

Tabela Fato de transações comerciais. Granularidade: 1 linha por item de pedido (`item_id`).

Coluna | Tipo de Dado | Nulo? | Chave | Descrição / Regra de Negócio
|------| ------------ | ----- | ----- | -----------------------------|
`item_id` | `VARCHAR(30)` | Não | PK | Identificador único do item do pedido (`ITEM-500001`).
`order_id` | `VARCHAR(30)` | Não | - | Número do cabeçalho do pedido (`PED-100001`).
`product_id` | `VARCHAR(20)` | Não | FK | Referência para `dim_product(product_id)`.
`customer_id` | `VARCHAR(20)` | Não | FK | Referência para `dim_customer(customer_id)`.
`salesperson_id` | `VARCHAR(20)` | Não | FK | Referência para `dim_salesperson(salesperson_id)`.
`channel` | `VARCHAR(50)` | Não | - | Canal de venda (`Venda Direta`, `E-commerce B2B`, etc).
`order_date` | `DATE` | Não | - | Data em que o pedido foi emitido.
`status` | `VARCHAR(30)` | Não | - | Status operacional: `Entregue`, `Faturado`, `Cancelado`.
`quantity` | `INT` | Não | - | Quantidade vendida ($> 0$).
`unit_price` | `NUMERIC(12,2)` | Não | - | Preço unitário praticado na venda ($\ge 0$).
`unit_cost` | `NUMERIC(12,2)` | Não | - | Custo unitário no momento da venda ($\ge 0$).
`gross_revenue` | `NUMERIC(12,2)` | Não | - | Receita bruta total: $\text{quantity} \times \text{unit\_price}$.
`discount_amount` | `NUMERIC(12,2)` | Não | - | Valor concedido em desconto ($\ge 0$).
`net_revenue` | `NUMERIC(12,2)` | Não | - | Receita líquida faturada: $\text{gross\_revenue} - \text{discount\_amount}$.
`total_cost` | `NUMERIC(12,2)` | Não | - | Custo total dos itens: $\text{quantity} \times \text{unit\_cost}$.
`gross_margin` | `NUMERIC(12,2)` | Sim | - | Margem de contribuição bruta: $\text{net\_revenue} - \text{total\_cost}$.
`gross_margin_pct` | `NUMERIC(6,4)` | Sim | - | Margem bruta percentual: $\frac{\text{gross\_margin}}{\text{net\_revenue}}$.

### 2.2 `fact_targets`

Metas comerciais de faturamento estipuladas por mês e por vendedor.

Coluna | Tipo de Dado | Nulo? | Chave | Descrição / Regra de Negócio
|------| ------------ | ----- | ----- | -----------------------------|
`target_month` | `DATE` | Não | PK | Primeiro dia do mês de referência da meta (2024-01-01).
`salesperson_id` | `VARCHAR(20)` | Não | PK, FK | Referência para `dim_salesperson(salesperson_id)`.
`target_revenue` | `NUMERIC(12,2)` | Não | - | Valor em reais ($) estabelecido como meta mensal.

## 3. Tabela de Auditoria & Governança

### 3.1 `stg_data_quality_report`

Histórico de auditoria de qualidade gerado durante a execução do ETL.

Coluna | Tipo de Dado | Nulo? | Chave | Descrição / Regra de Negócio
|------| ------------ | ----- | ----- | -----------------------------|
dataset | `VARCHAR(50)` | Não | - | Nome do conjunto de dados auditado (`fact_sales_items`, `orders`).
total_records | `INT` | Não | - | Total de registros brutos recebidos na ingestão.
valid_records | `INT` | Não | - | Total de registros higienizados e carregados no DW.
rejected_records | `INT` | Não | - | Registros descartados por anomalias ou inconsistências.
quality_score_pct | `NUMERIC(5,2)` | Não | - | Percentual de acurácia: $\frac{\text{valid\_records}}{\text{total\_records}} \times 100$.
details | `TEXT` | Não | - | Log descritivo dos motivos de descarte.