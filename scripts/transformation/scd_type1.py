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
# SCD Type 1
# =====================================================

def scd_type1_product(conn):

    logging.info("Applying SCD Type 1 on Product Dimension...")

    conn.execute(text("""

        UPDATE gold.product_dimension

        SET product_name = UPPER(product_name);

    """))

    conn.commit()

    logging.info("SCD Type 1 Applied Successfully")


# =====================================================
# Main Function
# =====================================================

def main():

    start_time = time.time()

    try:

        with engine.connect() as conn:

            logging.info("=" * 60)
            logging.info("Starting SCD Type 1 Process")

            scd_type1_product(conn)

            end_time = time.time()

            execution_time = round(end_time - start_time, 2)

            logging.info("=" * 60)
            logging.info("SCD Type 1 Completed Successfully")
            logging.info(f"Execution Time : {execution_time} Seconds")
            logging.info("=" * 60)

    except Exception as e:

        logging.error("=" * 60)
        logging.error("SCD Type 1 Failed")
        logging.error(e)
        logging.error("=" * 60)


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()