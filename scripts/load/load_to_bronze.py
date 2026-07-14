import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config.db_config import DB_CONFIG

# Database Connection
password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# Project Path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

CSV_PATH = os.path.join(BASE_DIR, "data", "source", "csv")

csv_files = [
    "order_products__prior.csv",
    "order_products__train.csv"
]

for file in csv_files:

    table_name = file.replace(".csv", "")

    print(f"\n{'='*60}")
    print(f"Loading : {table_name}")

    file_path = os.path.join(CSV_PATH, file)

    try:

        first_chunk = True

        for chunk in pd.read_csv(file_path, chunksize=2000):

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

        print(f" {table_name} Loaded Successfully")

    except Exception as e:

        print(f" Error loading {table_name}")
        print(e)

print("\n Bronze Layer Loading Completed.")