import logging
import time
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from config.db_config import DB_CONFIG


# =====================================================
# Logging Configuration
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
# Production SCD Type 1
# =====================================================

def scd_type1_product(conn):

    logging.info("Applying Production SCD Type 1 on Product Dimension...")

    result = conn.execute(
        text("""
            UPDATE gold.product_dimension AS g

            SET
                product_name = s.product_name,
                department   = s.department,
                aisle        = s.aisle

            FROM
            (
                SELECT
                    p.product_id,
                    p.product_name,
                    d.department,
                    a.aisle

                FROM silver.products AS p

                INNER JOIN silver.departments AS d
                    ON p.department_id = d.department_id

                INNER JOIN silver.aisles AS a
                    ON p.aisle_id = a.aisle_id

            ) AS s

            WHERE g.product_id = s.product_id

            AND
            (
                g.product_name IS DISTINCT FROM s.product_name
                OR g.department IS DISTINCT FROM s.department
                OR g.aisle IS DISTINCT FROM s.aisle
            );
        """)
    )

    

    logging.info(f"Rows Updated: {result.rowcount}")
    logging.info("Production SCD Type 1 Applied Successfully")


# =====================================================
# Main Function
# =====================================================

def main():

    start_time = time.time()

    try:

        with engine.begin() as conn:

            logging.info("=" * 70)
            logging.info("Starting Production SCD Type 1 Process")

            scd_type1_product(conn)

            execution_time = round(
                time.time() - start_time,
                2
            )

            logging.info("=" * 70)
            logging.info("Production SCD Type 1 Completed Successfully")
            logging.info(
                f"Execution Time: {execution_time} Seconds"
            )
            logging.info("=" * 70)

    except Exception as e:

        logging.error("=" * 70)
        logging.error("Production SCD Type 1 Failed")
        logging.error(str(e))
        logging.error("=" * 70)

        raise


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":
    main()