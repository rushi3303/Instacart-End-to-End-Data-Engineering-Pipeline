from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import time

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

start_time = time.time()

passed = 0
failed = 0

with engine.connect() as conn:

    for table, pk in TABLES.items():

        print("\n" + "=" * 90)
        print(f"TABLE : {table.upper()}")
        print("=" * 90)

        # --------------------------------------------------
        # Row Count
        # --------------------------------------------------

        total_rows = conn.execute(
            text(f"SELECT COUNT(*) FROM gold.{table};")
        ).scalar()

        print(f"Total Rows : {total_rows}")

        if total_rows == 0:
            print("Table Status : EMPTY ")
        else:
            print("Table Status : OK ")

        # --------------------------------------------------
        # Null Check
        # --------------------------------------------------

        null_condition = " OR ".join(
            [f"{col} IS NULL" for col in pk]
        )

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
                       {partition_cols}
                   FROM gold.{table}
                   GROUP BY {partition_cols}
                   HAVING COUNT(*) > 1
                ) t;
             """)
        ).scalar()

        print(f"Duplicate Rows : {duplicate_rows}")

        # --------------------------------------------------
        # Metadata Validation
        # --------------------------------------------------

        metadata = conn.execute(
            text("""
                SELECT
                    last_processed_key,
                    status
                FROM metadata.incremental_tracking
                WHERE layer_name='gold'
                AND table_name=:table;
            """),
            {
                "table": table
            }
        ).fetchone()

        if metadata:

            print(f"Metadata Status      : {metadata.status}")
            print(f"Last Processed Key   : {metadata.last_processed_key}")

        # --------------------------------------------------
        # Audit Validation
        # --------------------------------------------------

        audit = conn.execute(
            text("""
                SELECT
                    status
                FROM audit.audit_log
                WHERE table_name=:table
                ORDER BY end_time DESC
                LIMIT 1;
            """),
            {
                "table": table
            }
        ).scalar()

        print(f"Latest Audit Status  : {audit}")

        # --------------------------------------------------
        # Row Count Comparison
        # --------------------------------------------------

        if table == "product_dimension":

            silver_rows = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM silver.products;
                """)
            ).scalar()

            print(f"Silver product Rows          : {silver_rows}")

        elif table == "order_fact":

            silver_rows = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM silver.order_products__prior;
                """)
            ).scalar()

            print(f"Silver order Rows            : {silver_rows}")

        elif table == "customer_summary":

            silver_rows = conn.execute(
                text("""
                    SELECT COUNT(DISTINCT user_id)
                    FROM silver.orders;
                """)
            ).scalar()

            print(f"Distinct Users               : {silver_rows}")

        elif table == "sales_summary":

            silver_rows = conn.execute(
                text("""
                    SELECT COUNT(DISTINCT department_id)
                    FROM silver.products;
                 """)
            ).scalar()

            print(f"Distinct Departments         : {silver_rows}")
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

        if (
            total_rows > 0
            and null_rows == 0
            and duplicate_rows == 0
        ):

            passed += 1
            print("\nValidation Status : PASSED ")

        else:

            failed += 1
            print("\nValidation Status : FAILED ")

# ==========================================================
# Summary
# ==========================================================

end_time = time.time()

print("\n" + "=" * 90)
print("VALIDATION SUMMARY")
print("=" * 90)

print(f"Tables Passed : {passed}")
print(f"Tables Failed : {failed}")

print(f"\nExecution Time : {round(end_time - start_time,2)} Seconds")

if failed == 0:
    print("\nOVERALL STATUS : PASSED ")
else:
    print("\nOVERALL STATUS : FAILED ")

print("=" * 90)
print("Gold Validation Completed Successfully")
print("=" * 90)