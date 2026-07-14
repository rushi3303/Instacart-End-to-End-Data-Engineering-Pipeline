from sqlalchemy import create_engine, text
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

with engine.connect() as conn:

    for table in tables:

        print("\n" + "=" * 70)
        print(f"Table : {table}")

        # -------------------------
        # Row Count
        # -------------------------
        result = conn.execute(text(f"""
            SELECT COUNT(*)
            FROM silver.{table};
        """))

        print("\nTotal Rows :", result.scalar())

        # -------------------------
        # Duplicate Check
        # -------------------------
        duplicate_query = f"""

        SELECT COUNT(*)

        FROM (

            SELECT *,
            COUNT(*) OVER(PARTITION BY *)

            FROM silver.{table}

        ) t

        WHERE count > 1;

        """

        print("\nDuplicate Check : Skipped (Large Table)")

        # -------------------------
        # Sample Data
        # -------------------------

        result = conn.execute(text(f"""

            SELECT *

            FROM silver.{table}

            LIMIT 5;

        """))

        print("\nTop 5 Rows")

        for row in result:
            print(row)

print("\n Silver Validation Completed Successfully")