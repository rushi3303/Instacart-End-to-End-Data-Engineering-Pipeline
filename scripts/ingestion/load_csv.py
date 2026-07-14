import pandas as pd
import os

# Project root path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# CSV folder path
CSV_PATH = os.path.join(BASE_DIR, "data", "source", "csv")

# All CSV files
files = [
    "aisles.csv",
    "departments.csv",
    "products.csv",
    "orders.csv",
    "order_products__prior.csv",
    "order_products__train.csv"
]

for file in files:
    file_path = os.path.join(CSV_PATH, file)

    df = pd.read_csv(file_path)

    print("=" * 60)
    print(f"File Name : {file}")
    print(f"Rows      : {df.shape[0]}")
    print(f"Columns   : {df.shape[1]}")
    print(df.head())