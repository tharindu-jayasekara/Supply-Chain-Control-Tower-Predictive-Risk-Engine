import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect(r"D:\Portfolio Projects\Project_1\supply_chain.db")
cursor = conn.cursor()

# 1. Executive KPI Summary View
view_executive_kpis = """
CREATE VIEW IF NOT EXISTS v_executive_kpis AS
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(order_profit_per_order), 2) AS avg_profit_per_order,
    ROUND(AVG(is_delayed) * 100, 2) AS late_delivery_rate_pct,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days
FROM cleaned_supply_chain;
"""

# 2. Regional & Shipping Performance View
view_shipping_performance = """
CREATE VIEW IF NOT EXISTS v_shipping_performance AS
SELECT 
    market,
    order_region,
    shipping_mode,
    COUNT(order_id) AS total_shipments,
    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND(AVG(is_delayed) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(days_for_shipping_real), 2) AS avg_actual_shipping_days,
    ROUND(AVG(days_for_shipment_scheduled), 2) AS avg_scheduled_shipping_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_shipping_delay_days
FROM cleaned_supply_chain
GROUP BY market, order_region, shipping_mode;
"""

# 3. Financial Impact & Profitability View
view_financial_impact = """
CREATE VIEW IF NOT EXISTS v_financial_impact AS
SELECT 
    order_status,
    is_delayed,
    COUNT(order_id) AS order_count,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(order_profit_per_order), 2) AS net_profit,
    ROUND(AVG(order_item_discount_rate) * 100, 2) AS avg_discount_pct,
    ROUND(AVG(benefit_per_order), 2) AS avg_benefit_per_order
FROM cleaned_supply_chain
GROUP BY order_status, is_delayed;
"""

# 4. Product Category Delay Risk View
view_product_risk = """
CREATE VIEW IF NOT EXISTS v_product_risk AS
SELECT 
    category_name,
    COUNT(order_id) AS total_orders_placed,
    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS total_delayed_orders,
    ROUND(AVG(is_delayed) * 100, 2) AS category_delay_rate_pct,
    ROUND(SUM(sales), 2) AS total_category_sales
FROM cleaned_supply_chain
GROUP BY category_name
HAVING total_orders_placed >= 50;
"""

# Execute view creation scripts
views = [
    ("v_executive_kpis", view_executive_kpis),
    ("v_shipping_performance", view_shipping_performance),
    ("v_financial_impact", view_financial_impact),
    ("v_product_risk", view_product_risk)
]

for name, query in views:
    cursor.execute(f"DROP VIEW IF EXISTS {name};") # Fresh recreate
    cursor.execute(query)
    print(f"Successfully created SQL View: '{name}'")

query = 'SELECT Market, COUNT(*) FROM cleaned_supply_chain GROUP BY Market ORDER BY COUNT(*) DESC;'
df = pd.read_sql_query(query, conn)
print(df.head())

conn.commit()
conn.close()