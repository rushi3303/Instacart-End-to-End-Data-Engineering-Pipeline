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
    "aisles": ["aisle_id"],
    "departments": ["department_id"],
    "products": ["product_id"],
    "orders": ["order_id"],
    "order_products__prior": ["order_id", "product_id"],
    "order_products__train": ["order_id", "product_id"]
}

# ==========================================================
# Silver Validation
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
            text(f"""
                SELECT COUNT(*)
                FROM silver.{table};
            """)
        ).scalar()

        print(f"Total Rows : {total_rows}")

        if total_rows == 0:
            print("Table Status : EMPTY ❌")
        else:
            print("Table Status : OK ✅")

        # --------------------------------------------------
        # Null Check
        # --------------------------------------------------

        null_condition = " OR ".join(
            [f"{col} IS NULL" for col in pk]
        )

        null_rows = conn.execute(
            text(f"""
                SELECT COUNT(*)
                FROM silver.{table}
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
                    FROM silver.{table}
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
                WHERE layer_name='silver'
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

        bronze_rows = conn.execute(
            text(f"""
                SELECT COUNT(*)
                FROM bronze.{table};
            """)
        ).scalar()

        print(f"Bronze Rows          : {bronze_rows}")

        if bronze_rows == total_rows:
            print("Row Count Match      : YES ✅")
        else:
            print("Row Count Match      : NO ❌")

        # --------------------------------------------------
        # Top 5 Rows
        # --------------------------------------------------

        print("\nTop 5 Rows\n")

        result = conn.execute(
            text(f"""
                SELECT *
                FROM silver.{table}
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
            print("\nValidation Status : PASSED ✅")

        else:

            failed += 1
            print("\nValidation Status : FAILED ❌")

# ==========================================================
# Validation Summary
# ==========================================================

end_time = time.time()

print("\n" + "=" * 90)
print("VALIDATION SUMMARY")
print("=" * 90)

print(f"Tables Passed : {passed}")
print(f"Tables Failed : {failed}")

print(f"\nExecution Time : {round(end_time - start_time,2)} Seconds")

if failed == 0:
    print("\nOVERALL STATUS : PASSED ✅")
else:
    print("\nOVERALL STATUS : FAILED ❌")

print("=" * 90)
print("Silver Validation Completed Successfully")
print("=" * 90)



# from sqlalchemy import create_engine, text
# from urllib.parse import quote_plus

# from config.db_config import DB_CONFIG

# # ==========================================================
# # Database Connection
# # ==========================================================

# password = quote_plus(DB_CONFIG["password"])

# engine = create_engine(
#     f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
#     f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
# )

# # ==========================================================
# # Tables & Primary Keys
# # ==========================================================

# TABLES = {
#     "aisles": ["aisle_id"],
#     "departments": ["department_id"],
#     "products": ["product_id"],
#     "orders": ["order_id"],
#     "order_products__prior": ["order_id", "product_id"],
#     "order_products__train": ["order_id", "product_id"]
# }

# # ==========================================================
# # Validation
# # ==========================================================

# with engine.connect() as conn:

#     for table, pk in TABLES.items():

#         print("\n" + "=" * 80)
#         print(f"Table : {table}")

#         # --------------------------------------------------
#         # Row Count
#         # --------------------------------------------------

#         total_rows = conn.execute(
#             text(f"SELECT COUNT(*) FROM silver.{table};")
#         ).scalar()

#         print(f"\nTotal Rows : {total_rows}")

#         # --------------------------------------------------
#         # Null Check
#         # --------------------------------------------------

#         null_condition = " OR ".join([f"{col} IS NULL" for col in pk])

#         null_rows = conn.execute(
#             text(f"""
#                 SELECT COUNT(*)
#                 FROM silver.{table}
#                 WHERE {null_condition};
#             """)
#         ).scalar()

#         print(f"Null Rows : {null_rows}")

#         # --------------------------------------------------
#         # Duplicate Check
#         # --------------------------------------------------

#         partition_cols = ", ".join(pk)

#         duplicate_rows = conn.execute(
#             text(f"""
#                 SELECT COUNT(*)
#                 FROM
#                 (
#                     SELECT
#                         ROW_NUMBER() OVER(
#                             PARTITION BY {partition_cols}
#                         ) AS rn
#                     FROM silver.{table}
#                 ) t
#                 WHERE rn > 1;
#             """)
#         ).scalar()

#         print(f"Duplicate Rows : {duplicate_rows}")

#         # --------------------------------------------------
#         # Top 5 Rows
#         # --------------------------------------------------

#         print("\nTop 5 Rows\n")

#         result = conn.execute(
#             text(f"""
#                 SELECT *
#                 FROM silver.{table}
#                 LIMIT 5;
#             """)
#         )

#         for row in result:
#             print(row)

#         # --------------------------------------------------
#         # Validation Status
#         # --------------------------------------------------

#         if null_rows == 0 and duplicate_rows == 0:
#             print("\nValidation Status : PASSED ✅")
#         else:
#             print("\nValidation Status : FAILED ❌")

# print("\n" + "=" * 80)
# print("Silver Validation Completed Successfully")
# print("=" * 80)