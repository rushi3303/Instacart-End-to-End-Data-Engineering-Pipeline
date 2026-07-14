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
# SCD Type 2 Demo
# =====================================================

def scd_type2_demo(conn):

    logging.info("Applying SCD Type 2...")

    conn.execute(text("""

        ALTER TABLE gold.product_dimension

        ADD COLUMN IF NOT EXISTS effective_date DATE DEFAULT CURRENT_DATE;

    """))

    conn.execute(text("""

        ALTER TABLE gold.product_dimension

        ADD COLUMN IF NOT EXISTS end_date DATE;

    """))

    conn.execute(text("""

        ALTER TABLE gold.product_dimension

        ADD COLUMN IF NOT EXISTS is_current BOOLEAN DEFAULT TRUE;

    """))

    conn.commit()

    logging.info("SCD Type 2 Columns Added Successfully")


# =====================================================
# Main Function
# =====================================================

def main():

    start = time.time()

    try:

        with engine.connect() as conn:

            scd_type2_demo(conn)

            logging.info(f"Completed in {round(time.time()-start,2)} Seconds")

    except Exception as e:

        logging.error(e)


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()