import sqlite3
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Step 1: Fetch Cleaned Data from SQLite
db_path = r"D:\Portfolio Projects\Project_1\supply_chain.db"
conn = sqlite3.connect(db_path)

print("Fetching dataset...")
df = pd.read_sql("SELECT * FROM cleaned_supply_chain", conn)

# Step 2: Define Target and Features
# Target: is_delayed (1 = Delayed, 0 = On-Time)
target_col = "is_delayed"

# Key operational predictors available prior to/at shipping time
feature_cols = [
    "market",
    "order_region",
    "shipping_mode",
    "type",  # Payment type
    "category_name",
    "days_for_shipment_scheduled",
    "order_item_quantity",
    "sales",
    "order_item_discount_rate"
]

X = df[feature_cols]
y = df[target_col]

# Identify categorical and numerical columns
cat_features = ["market", "order_region", "shipping_mode", "type", "category_name"]
num_features = ["days_for_shipment_scheduled", "order_item_quantity", "sales", "order_item_discount_rate"]

# Step 3: Preprocessing Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features)
    ]
)

# Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Step 5: Build and Train Model Pipeline
print("Training Random Forest Delay Prediction Model...")
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1))
])

model_pipeline.fit(X_train, y_train)

# Step 6: Model Evaluation
y_pred = model_pipeline.predict(X_test)
y_proba = model_pipeline.predict_proba(X_test)[:, 1]

print("\n--- Model Evaluation Performance ---")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# Step 7: Batch Prediction on Entire Dataset & SQLite Output
print("\nGenerating risk scores across full dataset...")
df["predicted_delay_flag"] = model_pipeline.predict(X)
df["delay_probability_%"] = np.round(model_pipeline.predict_proba(X)[:, 1] * 100, 2)

# Select key columns to export for Power BI
export_cols = [
    "order_id",
    "order_item_id",
    "order_date_dateorders",
    "market",
    "order_region",
    "shipping_mode",
    "category_name",
    "sales",
    "is_delayed",
    "predicted_delay_flag",
    "delay_probability_%"
]

output_df = df[export_cols]

# Save to SQLite table
output_df.to_sql("predicted_order_delays", conn, if_exists="replace", index=False)
print("Predictions saved successfully to table: 'predicted_order_delays'")

conn.close()