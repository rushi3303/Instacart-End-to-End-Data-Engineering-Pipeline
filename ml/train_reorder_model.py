# =====================================================
# Customer Reorder Prediction - Basic ML Model
# =====================================================

import os
import pickle

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# =====================================================
# File Paths
# =====================================================

ORDERS_PATH = "data/source/csv/orders.csv"

TRAIN_PATH = (
    "data/source/csv/order_products__train.csv"
)

MODEL_DIR = "ml/models"

MODEL_PATH = (
    "ml/models/reorder_model.pkl"
)


# =====================================================
# Load Data
# =====================================================

print("\nLoading Instacart data...\n")

orders = pd.read_csv(
    ORDERS_PATH,
    usecols=[
        "order_id",
        "order_number",
        "order_dow",
        "order_hour_of_day",
        "days_since_prior_order"
    ]
)

order_products = pd.read_csv(
    TRAIN_PATH,
    usecols=[
        "order_id",
        "product_id",
        "add_to_cart_order",
        "reordered"
    ]
)

print(
    f"Orders loaded: {len(orders):,}"
)

print(
    f"Product-order records loaded: "
    f"{len(order_products):,}"
)


# =====================================================
# Merge Data
# =====================================================

print("\nMerging order and product data...\n")

df = order_products.merge(
    orders,
    on="order_id",
    how="inner"
)

print(
    f"Merged records: {len(df):,}"
)


# =====================================================
# Basic Feature Engineering
# =====================================================

print("\nCreating features...\n")

features = [
    "order_number",
    "order_dow",
    "order_hour_of_day",
    "days_since_prior_order",
    "add_to_cart_order"
]

X = df[features].copy()

y = df["reordered"]


# =====================================================
# Handle Missing Values
# =====================================================

X["days_since_prior_order"] = (
    X["days_since_prior_order"].fillna(0)
)


# =====================================================
# Train / Test Split
# =====================================================

print("Splitting data...\n")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print(
    f"Training records: {len(X_train):,}"
)

print(
    f"Testing records: {len(X_test):,}"
)


# =====================================================
# Train Model
# =====================================================

print("\nTraining Logistic Regression model...\n")

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# =====================================================
# Predictions
# =====================================================

print("Generating predictions...\n")

y_pred = model.predict(
    X_test
)


# =====================================================
# Evaluation
# =====================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


# =====================================================
# Display Results
# =====================================================

print("\n=====================================================")
print("CUSTOMER REORDER PREDICTION MODEL")
print("=====================================================")

print(
    f"Accuracy  : {accuracy:.4f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)


# =====================================================
# Save Model
# =====================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print(
    f"\nModel saved successfully: "
    f"{MODEL_PATH}"
)

print("\nML training completed successfully!")