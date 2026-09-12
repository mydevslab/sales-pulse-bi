# Documentação do Gerador de Dados Sintéticos | Nexa Distribuição

Este documento detalha as regras de negócio, premissas de modelagem e injeção de anomalias utilizadas no script `generator/data_generator.py`.

## 1. Visão Geral do Dataset

O dataset foi projetado para simular a operação comercial B2B da **Nexa Distribuição** ao longo de **24 meses** (01/01/2024 a 31/12/2025).

## Volumetria Gerada

- Pedidos (orders.csv): 50.000 cabeçalhos de pedidos.
- Itens de Pedidos (order_items.csv): ~150.000 itens operacionais.
- Clientes (customers.csv): 2.000 empresas B2B.
- Produtos (products.csv): 300 itens divididos em 10 categorias.
- Vendedores (salespeople.csv): 60 consultores em 5 regiões do Brasil.
- Metas (targets.csv): 1.440 registros (24 meses x 60 vendedores).

## 2. Regras e Sazonalidade Introduzidas

1. **Efeito Q4 (Sazonalidade Comercial B2B):** Pedidos nos meses de outubro, novembro e dezembro possuem probabilidade 25% maior de ocorrência, simulando encerramento de orçamento corporativo.

2. **Margens e Descontos:**

- Desconto médio variando entre 0% e 15%.
- Injeção de descontos pontuais agressivos de até 30% em 10% das vendas.
- Markups por categoria variando entre 25% e 110% sobre o custo base.

## 3. Anomalias Controladas para Data Quality (DQ)

Para demonstrar a eficácia da suite de testes de sanitização e do pipeline ETL, foram injetadas anomalias sintéticas intencionais nos arquivos brutos (data/raw/):

| Tabela | Anomalia Injetada |  Registros Afetados | Objetivo da Validação DQ
|--------|-------------------|---------------------|-------------------------|
products.csv | Categorias nulas (NaN) | 5 produtos | Validar substituição por valor padrão (Sem Categoria)
customers.csv | Regiões nulas (NaN) | 10 clientes | Validar fallback regional (Não Informado)
order_items.csv | Chaves primárias duplicadas (item_id) | 5 linhas | Testar desduplicação por chave
order_items.csv  | Quantidade negativa (quantity < 0)  | 1 linha | Tratar/filtrar registro inconsistente
order_items.csv  | Faturamento negativo (gross_revenue < 0)  | 1 linha  | Tratar/filtrar registro inconsistente
orders.csv  | Data futura fora do escopo (2030-01-01) | 2 pedidos  | Validar filtro de data limite do projeto