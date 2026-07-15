import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from config.db_config import DB_CONFIG

# =====================================================
# Database Connection
# =====================================================

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# =====================================================
# Project Path
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CSV_PATH = os.path.join(BASE_DIR, "data", "source", "csv")

csv_files = [
    "aisles.csv",
    "departments.csv",
    "products.csv",
    "orders.csv",
    "order_products__prior.csv",
    "order_products__train.csv"
]

# =====================================================
# Load Bronze Layer
# =====================================================

for file in csv_files:

    table_name = file.replace(".csv", "")

    print("\n" + "=" * 60)
    print(f"Processing : {table_name}")

    # -----------------------------------------
    # Skip loading if table already has data
    # -----------------------------------------

    with engine.connect() as conn:

        result = conn.execute(text(f"""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'bronze'
                AND table_name = '{table_name}'
            );
        """))

        table_exists = result.scalar()

        if table_exists:

            row_count = conn.execute(
                text(f"SELECT COUNT(*) FROM bronze.{table_name}")
            ).scalar()

            if row_count > 0:

                print(f"{table_name} already contains {row_count} rows.")
                print("Skipping loading...")

                continue

    file_path = os.path.join(CSV_PATH, file)

    try:

        first_chunk = True

        for chunk in pd.read_csv(file_path, chunksize=5000):

            chunk.to_sql(
                table_name,
                engine,
                schema="bronze",
                if_exists="replace" if first_chunk else "append",
                index=False,
                method="multi"
            )

            first_chunk = False

            print(f"Loaded {len(chunk)} rows...")

        print(f"{table_name} Loaded Successfully")

    except Exception as e:

        print(f"Error loading {table_name}")
        print(e)

print("\nBronze Layer Loading Completed.")