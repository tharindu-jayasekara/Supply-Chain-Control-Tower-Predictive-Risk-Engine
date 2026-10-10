# 🌐 Supply Chain Control Tower & Predictive Risk Engine

An end-to-end supply chain analytics and machine learning control tower built to monitor executive KPIs, diagnose operational and financial bottlenecks, and proactively predict shipment delays.

---

## 🚀 Project Overview
Supply chain disruptions cause substantial financial and operational drag. This project integrates a robust SQL-backed data pipeline, a machine learning risk classifier, and an interactive multi-page Power BI executive dashboard to transform raw transaction records into actionable intelligence.

### 🛠️ Tech Stack
* **Data Processing & ML:** Python (Pandas, NumPy, Scikit-Learn)
* **Database Management:** SQLite (`supply_chain.db`) with optimized SQL Views
* **Data Visualization & BI:** Power BI Desktop (DAX, Custom Conditional Formatting)
* **Dataset:** DataCo Smart Supply Chain Dataset (180K+ records)

---

## 📐 System Architecture & Workflow

1. **Data Engineering & Storage:** Raw data ingestion, missing value treatment, and date parsing handled via Python, persisting into a centralized SQLite database.
2. **SQL Optimization Layer:** Creation of pre-aggregated views (`v_executive_kpis`, `v_shipping_performance`, `v_financial_impact`, `v_product_risk`) to optimize report refresh performance.
3. **Predictive Analytics (ML):** A Random Forest classification model trained on operational features to score order-level delay probabilities prior to shipping.
4. **Executive Dashboard:** A 3-page interactive Power BI Control Tower providing high-level overview, bottleneck drill-downs, and actionable high-risk queue alerts.

---

## 📊 Power BI Dashboard Structure

* **Page 1: Executive Control Tower Overview**
  * Core global KPIs (Total Revenue, Total Profit, On-Time Delivery Rate %, Average Delay Days).
  * Geospatial logistics mapping (`order_region` / `order_country`) color-coded by late delivery rates.
  * Sales volume vs. monthly late risk trends and shipping mode efficiency comparisons.
* **Page 2: Financial & Operational Bottlenecks**
  * Profit-at-risk calculations isolating financial loss due to delayed orders.
  * Operational order status matrices and category-level discount rate impact scatter plots.
* **Page 3: Predictive Delay Risk & Actionable Alerts**
  * High-risk pending order queue driven by machine learning probability scores (`delay_probability_%`).
  * Risk distribution filters allowing operations teams to target interventions on shipments with >70% predicted delay risk.

---

## 🤖 Machine Learning Model Performance

* **Algorithm:** Random Forest Classifier (`scikit-learn`)
* **Features Used:** Market, Order Region, Shipping Mode, Payment Type, Category Name, Scheduled Shipping Days, Order Quantity, Sales, and Discount Rate.
* **Evaluation Metric:** **0.745 ROC-AUC Score** (demonstrating robust discriminative capacity for supply chain risk ranking).
* **Output Table:** Predictions are written back directly into SQLite as `predicted_order_delays`.
