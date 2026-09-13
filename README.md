# SalesPulse BI | Plataforma de Analytics para Performance Comercial B2B

## 📌 Visão Geral do Projeto

O **SalesPulse BI** é uma solução corporativa *end-to-end* de Analytics Engineer e Business Intelligence projetada para a **Nexa Distribuição**, uma empresa fictícia do segmento B2B.

O objetivo deste repositório é demonstrar a construção de uma plataforma analítica completa: desde a ingestão de dados brutos e validação automatizada de qualidade (*Data Quality*), passando por modelagem dimensional em **PostgreSQL** (*Star Schema*), até a entrega de **Views SQL** com *Window Functions* e desenvolvimento de um **modelo semântico no Power BI** alimentado por uma biblioteca completa de medias DAX.

## 🛠️ Tech Stack & Ferramentas

- **Linguagem & Processamento:**  Python 3.10+, Pandas, SQLAlchemy
- **Testes & Qualidade:** Pytest
- **Banco de Dados & DW:** PostgreSQL 15, Docker & Docker Compose
- **SQL Analítico:** PostgreSQL (CTEs, Window Functions `LAG`, `OVER`, `RANK`)
- **Visualização & Modelagem:** Power BI (DAX, Star Shcema Modeling)
- **Controle de Versão:** Git (Conventional Commits)

## 📐 Arquitetura da Solução

```
[ Fontes RAW: CSV ]
        │
        ▼
┌──────────────────────────┐
│ ETL Pipeline (Python)    │
│ - extract.py             │
│ - validate.py (Pytest)   │
│ - transform.py           │
│ - load.py (SQLAlchemy)   │
└─────────┬────────────────┘
        │
        ▼
┌──────────────────────────┐
│ PostgreSQL Data Warehouse│
│ - Star Schema            │
│ - Analytical Views       │
│ - Performance Indexes    │
└─────────┬────────────────┘
        │
        ▼
┌──────────────────────────┐
│ Power BI Semantic Model  │
│ - Calendar & Star Schema │
│ - DAX Measures Library   │
│ - Executive Dashboards   │
└──────────────────────────┘
```


## 📂 Estrutura do Projeto

```
sales-pulse-bi/
├── data/
│   ├── raw/                  # Dados brutos em CSV
│   ├── staging/              # Dados em processo de limpeza
│   └── processed/            # Dados sanitizados finais
├── etl/
│   ├── config.py             # Configurações de ambiente
│   ├── extract.py            # Extração de dados brutos
│   ├── validate.py           # Engine de Data Quality
│   ├── transform.py          # Regras dimensionais e fatos
│   ├── load.py               # Carregamento no PostgreSQL
│   └── pipeline.py           # Orquestrador mestre       
├── generator/                # Gerador de dados sintéticos B2B
│   └── data_generator.py     # Gerador de dados sintéticos B2B
├── sql/                      # DDLs, Views e Queries análiticas
│   ├── ddl/                  # Scripts DDL Star Schema
│   ├── views/                # Views analíticas
│   └── analytics/            # Queries com Window Functions
├── tests/                    # Testes automatizados de Data Quality
│   └── test_data_quality.py  # Testes automatizados Pytest
├── powerbi/                  # Medias DAX e documentação visual
│   ├── dax/                  # Medidas DAX (.dax)
│   └── docs/                 # Guia das páginas do Dashboard
├── docs/                     # Dicionário de dados, KPIs e Insights
├── docker-compose.yml        # Setup do ambiente PostgreSQL
├── requirements.txt          # Dependências Python
├── .env.example              # Exemplo de variáveis de ambiente
└── README.md                 # Documentação principal

```

## 🚀 Como Executar o Projeto (Em Desenvolviment)

### 1. Clonar o repositório e criar ambiente virtual

```
git clone https://github.com/mydevslab/sales-pulse-bi.git
cd sales-pulse-bi

# Criar e ativar o ambiente virtual 
python -m venv venv

# No Windows: .venv\Scripts\activate
# No Linux/Mac: source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Gerar os dados Sintéticos Brutos

`python generator/data_generator.py`

### 3. Executar a Suíte de Teste de Data Quality (Pytest)

`python -m pytest tests/`

### 4. Subir o Data Warehose PostgreSQL (Docker)

`docker-compose up -d`

### 5. Executar o Pipeline ETL

`python -m etl.pipeline`

### 6. Testar as Views Analíticas e Queries no PostgreSQL

Você pode se conectar ao banco via terminal ou DBeaver na porta 5433:

- **Host:** `localhost`
- **Porta:** `5433`
- **Banco:** `nexa_dw`
- **Usuário:** `dw_admin`
- **Senha:** `dw_secure_password123`

### 7. Conectar o Power BI ao PostgreSQL

No Power BI Desktop, vá em *Obter Dados* > *Banco de Dados SQL* > *Conectar*.

Preencha os campos:
- **Servidor:** `localhost, 5433`
- **Banco de dados:** `nexa_dw`
- **Modo de conectividade:** *Importar*
- Autentique com as credenciais acima

### 8. Desenvolver os Dashboards no Power BI

No Power BI Desktop:
- Importe as tabelas do modelo dimensional do PostgreSQL
- Construa as relações no modelo
- Crie as medidas DAX a partir da biblioteca em ./powerbi/dax/

### 9. Publicar os Dashboards no Power BI

No Power BI Service:
- Publique o relatório .pbix no Workspace desejado
- Configure a atualização agendada para sincronizar com o PostgreSQL (via Gateway de Dados Local se necessário)
- Compartilhe com os usuários e defina permissões

Se você estiver usando o Power BI para criar o dashboard, siga estes passos:

- Importe as tabelas do PostgreSQL para o Power BI (Get Data > SQL Server database)
- Verifique se as relações entre as tabelas estão corretas
- Crie as medidas DAX usando as fórmulas fornecidas
- Construa os visuais e organize-os no dashboard

## 📊 Governança de Métricas Principais

- **Faturamento Bruto (Gross Revenue):**
$$\text{Gross Revenue} = \sum (\text{quantity} \times \text{unit\_price})$$

- **Faturamento Líquido (Net Revenue):**
$$\text{Net Revenue} = \text{Gross Revenue} - \text{Total Discounts}$$

- **Margem Bruta (%):**
$$\text{Gross Margin(\%)} = \frac{\text{Net Revenue} - \text{Total Cost}}{\text{Net Revenue}}$$

- **Atingimento da Meta (%):**
$$\text{Target Archievement(\%)}=\frac{\text{Net Revenue}}{\text{Target Revenue}}$$


## 📝 Licença
Este projeto está sob a licença [MIT](LICENSE).