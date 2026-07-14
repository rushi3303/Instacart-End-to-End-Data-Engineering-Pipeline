import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

from config.db_config import DB_CONFIG

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

tables = [
    "aisles",
    "departments",
    "products",
    "orders",
    "order_products__prior",
    "order_products__train"
]

for table in tables:

    print("\n" + "=" * 60)
    print(f"Table : {table}")

    # Row Count
    row_count = pd.read_sql(
        f"SELECT COUNT(*) AS total_rows FROM bronze.{table}",
        engine
    )
    print(row_count)

    # First 5 Rows
    sample = pd.read_sql(
        f"SELECT * FROM bronze.{table} LIMIT 5",
        engine
    )
    print(sample)

    # Null Values
    print("\nNull Values")
    print(sample.isnull().sum())

    # Columns
    print("\nColumns")
    print(sample.columns.tolist())

print("\n Bronze Validation Completed")