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
# Audit Table
# =====================================================

def create_audit_table(conn):

    logging.info("Creating Audit Table...")

    conn.execute(text("""

        CREATE TABLE IF NOT EXISTS gold.audit_log (

            audit_id SERIAL PRIMARY KEY,

            process_name VARCHAR(100),

            table_name VARCHAR(100),

            status VARCHAR(20),

            rows_processed INT,

            execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

    """))

    conn.commit()

    logging.info("Audit Table Created Successfully")


# =====================================================
# Insert Audit Log
# =====================================================

def insert_audit_log(conn):

    logging.info("Inserting Audit Log...")

    result = conn.execute(text("""
        SELECT COUNT(*)
        FROM gold.product_dimension;
    """))

    rows = result.scalar()

    conn.execute(text("""

        INSERT INTO gold.audit_log
        (
            process_name,
            table_name,
            rows_processed,
            status
        )

        VALUES
        (
            'Gold Load',
            'product_dimension',
            :rows,
            'Success'
        );

    """), {"rows": rows})

    conn.commit()

    logging.info("Audit Log Inserted Successfully")    

# =====================================================
# Main Function
# =====================================================

def main():

    start = time.time()

    try:

        with engine.connect() as conn:

            create_audit_table(conn)

            insert_audit_log(conn)



            logging.info(f"Completed in {round(time.time()-start,2)} Seconds")

    except Exception as e:

        logging.error(e)


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()   