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
# Metadata Table
# =====================================================

def create_metadata_table(conn):

    logging.info("Creating Metadata Table...")

    conn.execute(text("""

        CREATE TABLE IF NOT EXISTS gold.etl_metadata (

            run_id SERIAL PRIMARY KEY,

            process_name VARCHAR(100),

            layer VARCHAR(50),

            status VARCHAR(20),

            execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

    """))

    conn.commit()

    logging.info("Metadata Table Created Successfully")

# =====================================================
# Insert Metadata
# =====================================================

def insert_metadata(conn):

    logging.info("Inserting Metadata...")

    conn.execute(text("""

        INSERT INTO gold.etl_metadata
        (
            process_name,
            layer,
            status
        )

        VALUES
        (
            'ETL Pipeline',
            'Gold',
            'Success'
        );

    """))

    conn.commit()

    logging.info("Metadata Inserted Successfully")

# =====================================================
# Main Function
# =====================================================

def main():

    start = time.time()

    try:

        with engine.connect() as conn:

            create_metadata_table(conn)

            insert_metadata(conn)

            logging.info(f"Completed in {round(time.time()-start,2)} Seconds")

    except Exception as e:

        logging.error(e)


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()