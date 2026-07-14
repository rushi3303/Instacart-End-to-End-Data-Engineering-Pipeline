import logging
import time
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from config.db_config import DB_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# =====================================================
# Incremental Load
# =====================================================

def incremental_product_load(conn):

    logging.info("Starting Incremental Load...")

    conn.execute(text("""

        INSERT INTO gold.product_dimension
        (
            product_id,
            product_name,
            aisle,
            department
        )

        SELECT
            p.product_id,
            p.product_name,
            a.aisle,
            d.department

        FROM silver.products p

        LEFT JOIN silver.aisles a
            ON p.aisle_id = a.aisle_id

        LEFT JOIN silver.departments d
            ON p.department_id = d.department_id

        WHERE NOT EXISTS
        (
            SELECT 1
            FROM gold.product_dimension g
            WHERE g.product_id = p.product_id
        );

    """))

    conn.commit()

    logging.info("Incremental Load Completed Successfully")

    # =====================================================
# Main Function
# =====================================================

def main():

    start = time.time()

    try:

        with engine.connect() as conn:

            incremental_product_load(conn)

            end = time.time()

            logging.info("=" * 60)
            logging.info("Incremental Load Completed Successfully")
            logging.info(f"Execution Time : {round(end-start,2)} Seconds")
            logging.info("=" * 60)

    except Exception as e:

        logging.error("=" * 60)
        logging.error("Incremental Load Failed")
        logging.error(e)
        logging.error("=" * 60)


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()