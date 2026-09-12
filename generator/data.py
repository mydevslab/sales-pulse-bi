import os
import random
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Semente para Reprodutibilidade
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

START_DATE = datetime(2024, 1, 1)
DAYS_PERIOD = 730  # (24 meses (2024 - 2025))

REGIONS = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
CHANNELS = ["Venda Direta / KAM", "E-commerce B2B", "Representantes", "Inside Sales"]
CATEGORIES = [
    "Equipamentos Industr%iais", "EPIs", "Embalagens", "Químicos e Limpeza", "Ferramentas", "Automação", "Suprimentos TI", "Manutenção (MRO)", "Logística & Paletização", "Escritório & Corporativo"
]


def generate_dimensions() -> tuple[list[dict], list[dict], list[dict]]:
    """Gera Dados sintéticos para vendedores, Produtos e Clientes"""
    logging.info("Gerando dados dimensionais (Vendedores, Produtos, Clientes)")

    # 1. Vendedores (60)
    salespeople = []
    
    for i in range(1, 61):
        salespeople.append({
            "salesperson_id": f"VEN-{i:03d}",
            "name": f"Vendedor {i}",
            "region": random.choice(REGIONS),
            "seniority": random.choice(["Júnior", "Pleno", "Sênior", "Key Account"]),
            "hire_date": (START_DATE - timedelta(days=random.randint(100, 1500))).strftime("%Y-%m-%d")
        })
    
    pd.DataFrame(salespeople).to_csv(f"{OUTPUT_DIR}/salespeople.csv", index=False)

    # 2. Produtos (300)
    products = []
    
    for i in range(1, 301):
        cat = random.choice(CATEGORIES)
        base_cost = round(random.uniform(15.0, 1200.0), 2)
        markup = random.uniform(1.25, 2.10)
        unit_price = round(base_cost * markup, 2)

        products.append({
            "product_id": f"PROD-{i:04d}",
            "product_name": f"Produto {cat[:3].upper()}-{i:04d}",
            "category": cat,
            "unit_cost": base_cost,
            "unit_price": unit_price 
        })
    
    # Injeção de Anomalia DQ: 5 produtos sem categoria (Nulls)
    for p in products [:5]:
        p["category"] = None

    pd.DataFrame(products).to_csv(f"{OUTPUT_DIR}/products.csv", index=False)

    # 3. Clientes (2.000)
    customers = []

    segment_weights = {"Corporativo": 0.2, "Médio Porte": 0.5, "Pequeno Porte": 0.3}

    for i in range(1, 2001):
        segment = random.choices(list(segment_weights.keys()), weights=list(segment_weights.values()))[0]
        
        customers.append({
            "customer_id": f"CLI-{i:05d}",
            "company_name": f"Empresa {i} {segment}",
            "segment": segment,
            "region": random.choice(REGIONS),
            "state": random.choice(["SP", "RJ", "MG", "PR", "SC", "RS", "BA", "PE", "GO", "AM"]),
            "created_at": (START_DATE - timedelta(days=random.randint(10, 1000))).strftime("%Y-%m-%d")
        }),
    
    # Injeção de Anomalia DQ: 10 cliente sem região (Nulls)
    for c in customers[:10]:
        c["region"] = None

    pd.DataFrame(customers).to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)

    return salespeople, products, customers


def generate_sales_and_targets() -> None:
    """Gera o histórico de 50.000 pedidos, ~150.000 itens e metas mensais"""
    logging.info("Gerando 50k pedidos, itens e materiais mensais...")

    df_prod = pd.read_csv(f"{OUTPUT_DIR}/products.csv")
    df_cust = pd.read_csv(f"{OUTPUT_DIR}/customers.csv")
    df_sales = pd.read_csv(f"{OUTPUT_DIR}/salespeople.csv")

    prod_list = df_prod.to_dict('records')
    cust_list = df_cust['customer_id'].tolist()
    sales_list = df_sales['salesperson_id'].tolist()

    orders = []
    order_items = []

    order_counter = 100000
    item_counter = 500000

    # 50k pedidos
    for i in range(50000):
        order_counter += 1
        order_id = f"PED-{order_counter}"

        days_offset = random.randint(0, DAYS_PERIOD - 1)
        order_date = START_DATE + timedelta(days=days_offset)

        # Padrão B2B: 25% dos pedidos são redirecionados para o Q4 (Out-Dez)
        if random.random() < 0.25:
            q4_days = [d for d in range (DAYS_PERIOD) if (START_DATE + timedelta(days=d)).month in [10, 11, 12]]
            if q4_days:
                order_date = START_DATE + timedelta(days=random.choice(q4_days))

        customer_id = random.choice(cust_list)
        salesperson_id = random.choice(sales_list)
        channel = random.choice(CHANNELS)

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "salesperson_id": salesperson_id,
            "channel": channel,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "status": random.choices(["Entregue", "Faturado", "Cancelado"], weights=[0.85, 0.12, 0.03])[0]
        })

        # Cada pedido possui entre 1 e 5 itens
        num_items = random.randint(1, 5)
        
        for _ in range(num_items):
            item_counter += 1
            prod = random.choice(prod_list)
            qty = random.randint(1, 50)

            # Desconto médio de 0% a 15% (com surtos de até 30%)
            disc_pct = round(random.uniform(0.0, 0.15) if random.random() > 0.1 else random.uniform(0.15, 0.30), 4)
            unit_price = float(prod['unit_price']) if pd.notnull(prod['unit_price']) else 100.0
            unit_cost = float(prod['unit_cost']) if pd.notnull(prod['unit_cost']) else 50.0

            gross_revenue = round(qty * unit_price, 2)
            discount_amount = round(gross_revenue * disc_pct, 2)
            net_revenue = round(gross_revenue - discount_amount, 2)
            total_cost = round(qty * unit_cost, 2)

            order_items.append({
                "item_id": f"ITEM-{item_counter}",
                "order_id": order_id,
                "product_id": prod['product_id'],
                "quantity": qty,
                "unit_price": unit_price,
                "unit_cost": unit_cost,
                "gross_revenue": gross_revenue,
                "discount_amount": discount_amount,
                "net_revenue": net_revenue,
                "total_cost": total_cost
            })

        # Log de progresso a cada 10.ooo pedidos para dar feedback visual
        if i % 10000 == 0:
            logging.info("Progresso: % d / 50.000 pedidos processados...", i)

    df_orders = pd.DataFrame(orders)
    df_items = pd.DataFrame(order_items)

    # INJESTÃO CONTROLADA DE ANOMALIAS PARA TESTES DE DATA QUALITY
    # 1. Duplicidade de Item ID (5 registros)
    df_items = pd.concat([df_items, df_items.iloc[:5]], ignore_index=True)

    # 2. Valores Negativos / Inconsistentes (3 registros)
    df_orders.loc[10, 'gross_revenue'] = 500.00
    df_items.loc[15, 'quantity'] = -10

    # 3. Data Futura Inválida (2 registros em Orders)
    df_orders.loc[20, 'order_date'] = '2030-01-01'
        
    df_orders.to_csv(f"{OUTPUT_DIR}/orders.csv", index=False)
    df_items.to_csv(f"{OUTPUT_DIR}/order_items.csv", index=False)

    # Metas Mensais por Vendedor (24 meses x 60 vendedores)
    targets = []
    months = pd.date_range(start="2024-01-01", periods=24, freq="MS")

    for m in months:
        for sp in sales_list:
            base_target = random.uniform(40000, 120000)
            targets.append({
                "target_mount": m.strftime("%Y-%m-%d"),
                "salesperson_id": sp,
                "target_revenue": round(base_target, 2),
            })

    pd.DataFrame(targets).to_csv(f"{OUTPUT_DIR}/targets.csv", index=False)

    logging.info("Geração finalizada com sucesso! Arquivos armazenados em %s", OUTPUT_DIR)


if __name__ == "__main__":
    generate_dimensions()
    generate_sales_and_targets()
