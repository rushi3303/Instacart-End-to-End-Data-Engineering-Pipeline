
import logging
import os
from datetime import datetime
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.dialects.postgresql import insert

from config.db_config import DB_CONFIG

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

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
# Check File Changed
# =====================================================

def is_file_changed(file_path, conn):

    file_name = os.path.basename(file_path)

    current_modified = datetime.fromtimestamp(
        os.path.getmtime(file_path)
    ).replace(microsecond=0)
    current_size = os.path.getsize(file_path)

    result = conn.execute(
        text("""
            SELECT last_modified,
                   file_size
            FROM metadata.file_tracking
            WHERE file_name = :file_name
        """),
        {
            "file_name": file_name
        }
    ).fetchone()

    if result is None:
        return True

    if result[0] is None:
        return True

    
    stored_modified = result[0].replace(microsecond=0)
    stored_size = result[1]

    return (
        stored_modified != current_modified
        or
        stored_size != current_size
    )
    


# =====================================================
# Update File Tracking
# =====================================================

def update_file_tracking(file_path, conn):

    file_name = os.path.basename(file_path)

    current_modified = datetime.fromtimestamp(
        os.path.getmtime(file_path)
    ).replace(microsecond=0)
    current_size = os.path.getsize(file_path)
    conn.execute(
        text("""
            INSERT INTO metadata.file_tracking
            (
                file_name,
                last_modified,
                last_loaded,
                status,
                file_size
            )

            VALUES
            (
                :file_name,
                :last_modified,
                CURRENT_TIMESTAMP,
                'SUCCESS',
                :file_size
            )

            ON CONFLICT (file_name)

            DO UPDATE SET

                last_modified = EXCLUDED.last_modified,
                last_loaded = CURRENT_TIMESTAMP,
                status = 'SUCCESS',
                file_size = EXCLUDED.file_size
        """),
        {
            "file_name": file_name,
            "last_modified": current_modified,
            "file_size": current_size
        }
    )

# =====================================================
# Load Bronze Layer
# =====================================================

for file in csv_files:

    table_name = file.replace(".csv", "")
    file_path = os.path.join(CSV_PATH, file)

    if not os.path.exists(file_path):
        logging.warning(f"{file} not found. Skipping...")
        continue
    
    logging.info("=" * 60)
    logging.info(f"Processing : {table_name}")

    try:

        with engine.begin() as conn:

            # -----------------------------------------
            # Skip if file is unchanged
            # -----------------------------------------
            if not is_file_changed(file_path, conn):

                logging.info(f"{file} unchanged. Skipping...")

                continue

            # -----------------------------------------
            # Load Bronze Table
            # -----------------------------------------
            metadata = MetaData(schema="bronze")

            table = Table(
                table_name,
                metadata,
                autoload_with=conn
            )

            total_rows = 0

            for chunk in pd.read_csv(
                file_path,
                chunksize=50000
            ):

                records = chunk.to_dict(
                    orient="records"
                )

                stmt = insert(table).values(records)

                pk_columns = [
                    col.name
                    for col in table.primary_key.columns
                ]

                stmt = stmt.on_conflict_do_nothing(
                    index_elements=pk_columns
                )

                conn.execute(stmt)

                total_rows += len(chunk)

                logging.info(
                    f"{table_name} : {total_rows} rows processed"
                )

            # -----------------------------------------
            # Update Metadata
            # -----------------------------------------
            update_file_tracking(
                file_path,
                conn
            )

            logging.info(
                f"{table_name} Loaded Successfully"
            )

    except Exception as e:

        logging.exception(
            f"Error loading {table_name}: {e}"
        )

logging.info("=" * 60)
logging.info("Bronze Layer Loading Completed.")










# import logging
# import os
# from datetime import datetime
# import pandas as pd
# from sqlalchemy import create_engine, MetaData, Table, text
# from sqlalchemy.dialects.postgresql import insert
# from urllib.parse import quote_plus
# from config.db_config import DB_CONFIG


# # =====================================================
# # Database Connection
# # =====================================================

# password = quote_plus(DB_CONFIG["password"])

# engine = create_engine(
#     f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
#     f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
# )


# # =====================================================
# # Check File Change
# # =====================================================

# def is_file_changed(file_path, conn):

#     file_name = os.path.basename(file_path)

#     current_modified = datetime.fromtimestamp(
#         os.path.getmtime(file_path)
#     )

#     result = conn.execute(
#         text("""
#             SELECT last_modified
#             FROM metadata.file_tracking
#             WHERE file_name = :file_name
#         """),
#         {"file_name": file_name}
#     ).fetchone()

#     if result is None:
#         return True
#     stored_modified = result[0].replace(microsecond=0)
#     return result[0] != current_modified


# # =====================================================
# # Update File Tracking
# # =====================================================

# def update_file_tracking(file_path, conn):

#     file_name = os.path.basename(file_path)

#     current_modified = datetime.fromtimestamp(
#         os.path.getmtime(file_path)
#     ).replace(microsecond=0)

#     conn.execute(
#         text("""
#             INSERT INTO metadata.file_tracking
#             (
#                 file_name,
#                 last_modified,
#                 last_loaded,
#                 status
#             )

#             VALUES
#             (
#                 :file_name,
#                 :last_modified,
#                 CURRENT_TIMESTAMP,
#                 'SUCCESS'
#             )

#             ON CONFLICT (file_name)
#             DO UPDATE
#             SET
#                 last_modified = EXCLUDED.last_modified,
#                 last_loaded = CURRENT_TIMESTAMP,
#                 status = 'SUCCESS'
#         """),
#         {
#             "file_name": file_name,
#             "last_modified": current_modified
#         }
#     )
# # =====================================================
# # Project Path
# # =====================================================

# BASE_DIR = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "..", "..")
# )

# CSV_PATH = os.path.join(BASE_DIR, "data", "source", "csv")

# csv_files = [
#     "aisles.csv",
#     "departments.csv",
#     "products.csv",
#     "orders.csv",
#     "order_products__prior.csv",
#     "order_products__train.csv"
# ]

# # =====================================================
# # Load Bronze Layer
# # =====================================================

# for file in csv_files:

#     table_name = file.replace(".csv", "")

#     print("\n" + "=" * 60)
#     print(f"Processing : {table_name}")


#     file_path = os.path.join(CSV_PATH, file)

#     try:

#         with engine.begin() as conn:

#          if not is_file_changed(file_path, conn):
#             print(f"{file} unchanged. Skipping...")
#             continue
#          metadata = MetaData(schema="bronze")

#          table = Table(
#             table_name,
#             metadata,
#             autoload_with=conn
#          )

#          for chunk in pd.read_csv(file_path, chunksize=50000):

#             # Convert DataFrame chunk to list of dictionaries
#             records = chunk.to_dict(orient="records")

#             # Create INSERT statement
#             stmt = insert(table).values(records)

#             # Get Primary Key columns dynamically
#             pk_columns = [col.name for col in table.primary_key.columns]

#             # Ignore duplicate records
#             stmt = stmt.on_conflict_do_nothing(
#                index_elements=pk_columns
#             )

#             # Execute INSERT
            
#             conn.execute(stmt)
            

#             print(f"Loaded {len(chunk)} rows...")
#         update_file_tracking(file_path, conn)
#         print(f"{table_name} Loaded Successfully")

#     except Exception as e:

#         print(f"Error loading {table_name}")
#         print(e)

# print("\nBronze Layer Loading Completed.")