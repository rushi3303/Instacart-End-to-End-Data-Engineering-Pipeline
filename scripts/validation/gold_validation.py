from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from config.db_config import DB_CONFIG

# ==========================================================
# Database Connection
# ==========================================================

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# ==========================================================
# Tables & Primary Keys
# ==========================================================

TABLES = {
    "product_dimension": ["product_id"],
    "order_fact": ["order_id", "product_id"],
    "customer_summary": ["user_id"],
    "sales_summary": ["department"]
}

# ==========================================================
# Gold Validation
# ==========================================================

with engine.connect() as conn:

    for table, pk in TABLES.items():

        print("\n" + "=" * 80)
        print(f"Table : {table}")

        # --------------------------------------------------
        # Row Count
        # --------------------------------------------------

        total_rows = conn.execute(
            text(f"SELECT COUNT(*) FROM gold.{table};")
        ).scalar()

        print(f"\nTotal Rows : {total_rows}")

        # --------------------------------------------------
        # Null Check
        # --------------------------------------------------

        null_condition = " OR ".join([f"{col} IS NULL" for col in pk])

        null_rows = conn.execute(
            text(f"""
                SELECT COUNT(*)
                FROM gold.{table}
                WHERE {null_condition};
            """)
        ).scalar()

        print(f"Null Rows : {null_rows}")

        # --------------------------------------------------
        # Duplicate Check
        # --------------------------------------------------

        partition_cols = ", ".join(pk)

        duplicate_rows = conn.execute(
            text(f"""
                SELECT COUNT(*)
                FROM
                (
                    SELECT
                        ROW_NUMBER() OVER(
                            PARTITION BY {partition_cols}
                        ) AS rn
                    FROM gold.{table}
                ) t
                WHERE rn > 1;
            """)
        ).scalar()

        print(f"Duplicate Rows : {duplicate_rows}")

        # --------------------------------------------------
        # Top 5 Rows
        # --------------------------------------------------

        print("\nTop 5 Rows\n")

        result = conn.execute(
            text(f"""
                SELECT *
                FROM gold.{table}
                LIMIT 5;
            """)
        )

        for row in result:
            print(row)

        # --------------------------------------------------
        # Validation Status
        # --------------------------------------------------

        if null_rows == 0 and duplicate_rows == 0:
            print("\nValidation Status : PASSED ✅")
        else:
            print("\nValidation Status : FAILED ❌")

print("\n" + "=" * 80)
print("Gold Validation Completed Successfully")
print("=" * 80)