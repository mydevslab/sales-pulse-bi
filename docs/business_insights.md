# Relatório de Diagnóstico Comercial & Insights de Negócio | Nexa Distribuição

**Destinatário:** Diretoria Comercial & Conselho Executivo
**Elaborado por:** Analista de Analytics / BI
**Período Analisado:** 01/01/2024 a 31/12/2025 (24 Meses)

## 1. Resumo Executivo (Executive Summary)

A análise consolidada das operações comerciais da Nexa Distribuição revela um faturamento sólido e atingimento global de metas em diversos períodos. No entanto, o diagnóstico detalhado por granularidade de item de pedido e por canal indicou uma séria erosão da margem bruta corporativa, provocada pela concessão desmedida de descontos comerciais na Região Nordeste e pela baixa rentabilidade da categoria de maior volume (Suprimentos TI).

## 2. Diagnóstico dos 8 Insights de Alto Impacto

### 💡 Insight 1: Concessão Distorcida de Descontos na Região Nordeste
- **Diagnóstico:** A região Nordeste superou a meta de faturamento ($104\%$ de atingimento), porém registrou a menor margem bruta corporativa ($22,1\%$).
- **Causa Raiz:** Vendedores concederam descontos médios superiores a $20\%$ nas últimas semanas dos meses para garantir o fechamento de metas individuais.
- **Ação Recomendada:** Bloquear descontos acima de $12\%$ no ERP sem a aprovação formal do Diretor Comercial.

💡 Insight 2: Categoria "Campeã de Faturamento, Vilã de Margem"
- **Diagnóstico**: A categoria Suprimentos TI responde por $18\%$ da receita líquida total, mas gera apenas $6\%$ da margem bruta em reais ($).
- **Causa Raiz:** Alta concorrência de mercado e aumento dos custos de fornecedores internacionais.
- **Ação Recomendada:** Implementar estratégia de cross-selling associando a compra de Suprimentos TI à categoria de Equipamentos Industriais (margem média de $42\%$).

### 💡 Insight 3: Concentração de Receita nos Top 5% de Clientes (Curva de Pareto)
- **Diagnóstico:** Apenas $5\%$ da base de clientes B2B ativos representam $48\%$ da receita líquida acumulada.
- **Risco de Negócio:** A perda de 2 a 3 contas Key Accounts traria impacto crítico no fluxo de caixa.
- **Ação Recomendada:** Criar um programa de fidelização VIP com contratos de fornecimento plurianuais e atendimento dedicado por KAMs.

### 💡 Insight 4: Alta Eficiência Comercial no Canal E-commerce B2B

- **Diagnóstico:** O canal digital apresentou o maior Ticket Médio ($+34\%$ em relação ao Inside Sales) e a melhor margem operacional.
- **Causa Raiz:** Compras autônomas de reposição sem intermediação de vendedores (redução do custo de venda).
- **Ação Recomendada:** Direcionar clientes de Pequeno e Médio Porte (PMEs) para realizarem compras recorrentes na plataforma e-commerce.

### 💡 Insight 5: Ramp-up Lento da Equipe Comercial Júnior
- **Diagnóstico:** Vendedores de nível Júnior demoram em média 8 meses para atingir $100\%$ da meta mensal.
- **Ação Recomendada:** Criar um programa de job shadowing estruturado de 12 semanas em parceria com consultores de nível Sênior.

### 💡 Insight 6: Sazonalidade Acentuada no 4º Trimestre (Q4)
- **Diagnóstico:** Há um pico de $30\%$ no volume de pedidos entre Outubro e Dezembro, causando sobrecarga e atrasos na Logística.
- **Ação Recomendada:** Ofertar campanhas de antecipação de compras no início do Q3 com descontos progressivos escalonados.

### 💡 Insight 7: Prejuízo Operacional em Pedidos de Pequeno Valor
- **Diagnóstico:** Pedidos de valor inferior a $R\$ 500,00$ geram margem líquida negativa devido ao custo do frete fracionado B2B.
- **Ação Recomendada:** Fixar valor de pedido mínimo de $R\$ 800,00$ para concessão de frete grátis.

### 💡 Insight 8: Prevenção de Impacto Financeiro via Data Quality Engine
- **Diagnóstico:** O módulo de Data Quality interceptou e tratou anomalias nos dados brutos (chaves duplicadas e receitas negativas).
- **Impacto:** A higienização automática impediu a distorção reportada de mais de $R\$ 1,2 \text{ milhão}$ nas DREs analíticas.

## 3. Matriz de Recomendações Táticas & Estratégicas

| Prioridade | Iniciativa | Área Responsável | Prazo | Impacto Estimado |
|----------| -----------| -----------------| ----- | ----------------|
| Alta | Trava de alçada de descontos no Nordeste | Comercial / TI | 15 dias | $+ 3,5\%$ de Margem Bruta na região |
| Alta | Fixação de pedido mínimo para frete grátis | Logística / Comercial | 30 dias | Redução de $12\%$ no custo de frete |
| Média | Programa VIP de Retenção de Key Accounts | Customer Success | 45 dias | Mitigação de risco de churn B2B |
| Média | Migração de PMEs para E-commerce B2B | Marketing Digital | 60 dias | Aumento de $15\%$ no Ticket Médio PME |