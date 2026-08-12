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
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/"
    f"{DB_CONFIG['database']}"
)


# =====================================================
# SCD Type 2
# =====================================================

def scd_type2_product(conn):

    logging.info("Starting SCD Type 2 Process...")


    # =================================================
    # STEP 1: Close old records where data has changed
    # =================================================

    update_result = conn.execute(text("""

        UPDATE gold.product_dimension_history h

        SET
            end_date = CURRENT_DATE - 1,
            is_current = FALSE

        FROM
        (
            SELECT
                p.product_id,
                p.product_name,
                d.department,
                a.aisle

            FROM silver.products p

            INNER JOIN silver.departments d
                ON p.department_id = d.department_id

            INNER JOIN silver.aisles a
                ON p.aisle_id = a.aisle_id

        ) s

        WHERE h.product_id = s.product_id

        AND h.is_current = TRUE

        AND
        (
            h.product_name IS DISTINCT FROM s.product_name
            OR h.department IS DISTINCT FROM s.department
            OR h.aisle IS DISTINCT FROM s.aisle
        );

    """))

    logging.info(
        f"Old records closed: {update_result.rowcount}"
    )


    # =================================================
    # STEP 2: Insert new records
    # New product OR changed product
    # =================================================

    insert_result = conn.execute(text("""

        INSERT INTO gold.product_dimension_history
        (
            product_id,
            product_name,
            department,
            aisle,
            effective_date,
            end_date,
            is_current
        )

        SELECT
            s.product_id,
            s.product_name,
            s.department,
            s.aisle,
            CURRENT_DATE,
            NULL,
            TRUE

        FROM
        (
            SELECT
                p.product_id,
                p.product_name,
                d.department,
                a.aisle

            FROM silver.products p

            INNER JOIN silver.departments d
                ON p.department_id = d.department_id

            INNER JOIN silver.aisles a
                ON p.aisle_id = a.aisle_id

        ) s

        LEFT JOIN gold.product_dimension_history h

            ON h.product_id = s.product_id

            AND h.is_current = TRUE

        WHERE h.product_id IS NULL

        OR
        (
            h.product_name IS DISTINCT FROM s.product_name
            OR h.department IS DISTINCT FROM s.department
            OR h.aisle IS DISTINCT FROM s.aisle
        );

    """))

    logging.info(
        f"New records inserted: {insert_result.rowcount}"
    )


    # =================================================
    # Commit Transaction
    # =================================================


    logging.info(
        "SCD Type 2 Process Completed Successfully"
    )


# =====================================================
# Main Function
# =====================================================

def main():

    start_time = time.time()

    try:

        with engine.begin() as conn:

            logging.info("=" * 70)
            logging.info(
                "Starting Product Dimension SCD Type 2"
            )
            logging.info("=" * 70)

            scd_type2_product(conn)

            execution_time = round(
                time.time() - start_time,
                2
            )

            logging.info("=" * 70)
            logging.info(
                "Product Dimension SCD Type 2 Completed Successfully"
            )
            logging.info(
                f"Execution Time: {execution_time} Seconds"
            )
            logging.info("=" * 70)


    except Exception as e:

        logging.error("=" * 70)
        logging.error("SCD Type 2 Process Failed")
        logging.error(str(e))
        logging.error("=" * 70)

        raise


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":
    main()