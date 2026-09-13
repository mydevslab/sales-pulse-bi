# Dicionário de KPIs & Governança de Métricas | Sales Pulse BI

Este documento oficializa os padrões conceituais, fórmulas matemáticas e regras de negócio de todas as métricas utilizadas na camada SQL e no modelo semântico do Power BI.

## 1. Métricas Financeiras & Operacionais

### 1.1 Faturamento Bruto (Gross Revenue)

- **Descrição**: Valor total comercializado antes da aplicação de descontos comerciais.

- **Fórmula Matemática**:
$$\text{Gross Revenue} = \sum_{i \in \text{Vendas Validas}} (\text{quantity}_i \times \text{unit\_price}_i)$$

- **Filtro Aplicado**: Apenas pedidos com `status` em {`"Entregue", "Faturado"`}.
- **Tabela Origem:** `fact_sales`

### 1.2 Faturamento Líquido (Net Revenue)

- **Descrição**: Faturamento real retido pela empresa após concessão de descontos por volume ou negociação. É a métrica base para metas e comissionamento.
- **Fórmula Matemática**:
$$\text{Net Revenue} = \text{Gross Revenue} - \sum \text{discount\_amount}$$

- **Filtro Aplicado**: Pedidos faturados/entregues.

### 1.3 Margem Bruta ($ e %)

- **Descrição:** Lucro bruto absoluto gerado pelas vendas e seu respectivo percentual sobre a receita líquida.
- **Fórmulas Matemáticas:**

$$	\text{Gross Margin (\$)} = \text{Net Revenue} - \text{Total Cost}$$

$$\text{Gross Margin (\%) } = \frac{\text{Gross Margin (\$)}}{\text{Net Revenue}}$$

- **Regra de Alerta:** Caso o Gross Margin (%) consolidado mensal fique abaixo de $25\%$, ativa-se o indicador de atenção no BI.

### 1.4 Ticket Médio (Average Ticket)

- **Descrição:** Valor médio gasto por pedido faturado.
- **Fórmula Matemática:**
$$\text{Average Ticket} = \frac{\text{Net Revenue}}{\text{COUNT(DISTINCT } \text{order\_id})}$$

## 2. Métricas de Metas & Análise de Variação (Target & Variance)

### 2.1 Percentual de Atingimento da Meta (Target Achievement %)

- **Descrição**: Relação percentual entre o faturamento líquido realizado e a meta estipulada.
- **Fórmula Matemática:**
$$\text{Target Achievement (\%)} = \frac{\text{Net Revenue}}{\text{Total Target Revenue}}$$

- **Status de Meta:**
    - $\ge 100\%$: Meta Atingida (Verde)
    - $< 100\%$: Abaixo da Meta (Vermelho)

### 2.2 Desvio Absoluto de Meta (Target Variance Amount)

- **Descrição**: Diferença financeira em reais ($) entre o realizado e a meta.
- **Fórmula Matemática**:
$$\text{Target Variance Amount} = \text{Net Revenue} - \text{Total Target Revenue}$$

## 3. Inteligência Temporal (Time Intelligence)

### 3.1 Crescimento Mês a Mês (MoM Growth %)

- **Descrição:** Variação percentual da receita líquida em relação ao mês imediatamente anterior ($M - 1$).
- **Fórmula Matemática:**
$$\text{MoM Growth (\%)} = \frac{\text{Net Revenue}_t - \text{Net Revenue}_{t-1}}{\text{Net Revenue}_{t-1}} \times 100$$

## 3.2 Crescimento Ano a Ano (YoY Growth %)

- **Descrição:** Variação percentual da receita líquida em relação ao mesmo mês do ano anterior ($Y - 1$).
- **Fórmula Matemática:**
$$\text{YoY Growth (\%)} = \frac{\text{Net Revenue}_t - \text{Net Revenue}_{t-12}}{\text{Net Revenue}_{t-12}} \times 100$$

## 4. Métricas de Governança e Data Quality

### 4.1 Data Quality Score Global (%)

- **Descrição:** Índice percentual de acurácia dos dados processados pelo pipeline ETL.
- **Fórmula Matemática:**
$$\text{DQ Global Score (\%)} = \frac{\sum \text{valid\_records}}{\sum \text{total\_records}} \times 100$$
