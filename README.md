# SalesPulse BI | Plataforma de Analytics para Performance Comercial B2B

## 📌 Visão Geral do Projeto

O **SalesPulse BI** é uma solução corporativa end-to-end de Analytics Engineer e Business Intelligence projetada para a **Nexa Distribuição**, uma empresa fictícia do segmento B2B.

O objetivo deste repositório é demonstrar a construção de uma plataforma analítica completa: desde a ingestão de dados brutos e validação automatizada de qualidade (Data Quality), passando por modelagem dimensional em **PostgreSQL** (Star Schema), até a entrega de **Views SQL** otimizadas e **Dashboards Executivos no Power BI**.

🛠️ Tech Stack & Ferramentas

- **Linguagem & Processamento:**  Python 3.12+, Pandas, SQLAlchemy
- **Testes & Qualidade:** Pytest
- **Banco de Dados & DW:** PostgreSQL 15, Docker & Docker Compose
- **Visualização & Modelagem:** Power BI, DAX
- **Controle de Versão:** Git (Conventional Commits)

## 📂 Estrutura do Projeto

```
sales-pulse-bi/
├── data/
│   ├── raw/                  # Dados brutos em CSV
│   ├── staging/              # Dados em processo de limpeza
│   └── processed/            # Dados sanitizados finais
├── etl/                      # Pipeline ETL modular em Python
├── generator/                # Gerador de dados sintéticos B2B
├── sql/                      # DDLs, Views e Queries análiticas
├── tests/                    # Testes automatizados de Data Quality
├── powerbi/                  # Medias DAX e documentação visual
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
python -m venv .venv

# No Windows: .venv\Scripts\activate
# No Linux/Mac: source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Licença
Este projeto está sob a licença [MIT](LICENSE).