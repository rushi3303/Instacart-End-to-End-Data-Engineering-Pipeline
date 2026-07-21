import logging
import time
from datetime import datetime
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
# Create Audit Schema & Table
# =====================================================

def create_audit_table(conn):

    logging.info("Creating Audit Schema & Table...")

    conn.execute(text("""

        CREATE SCHEMA IF NOT EXISTS audit;

        CREATE TABLE IF NOT EXISTS audit.audit_log (

            audit_id SERIAL PRIMARY KEY,

            pipeline_name VARCHAR(100) NOT NULL,

            layer_name VARCHAR(50) NOT NULL,

            table_name VARCHAR(100) NOT NULL,

            status VARCHAR(20) NOT NULL,

            rows_processed BIGINT DEFAULT 0,

            start_time TIMESTAMP,

            end_time TIMESTAMP,

            execution_time_seconds NUMERIC(10,2),

            error_message TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

    """))

    logging.info("Audit Table Created Successfully")


# =====================================================
# Get Row Count
# =====================================================

def get_row_count(conn, schema_name, table_name):

    result = conn.execute(text(f"""
        SELECT COUNT(*)
        FROM {schema_name}.{table_name};
    """))

    return result.scalar()


# =====================================================
# Insert Audit Log
# =====================================================

def insert_audit_log(
    conn,
    pipeline_name,
    layer_name,
    table_name,
    status,
    rows_processed,
    start_time,
    end_time,
    execution_time_seconds,
    error_message=None
):

    conn.execute(text("""

        INSERT INTO audit.audit_log
        (
            pipeline_name,
            layer_name,
            table_name,
            status,
            rows_processed,
            start_time,
            end_time,
            execution_time_seconds,
            error_message
        )

        VALUES
        (
            :pipeline_name,
            :layer_name,
            :table_name,
            :status,
            :rows_processed,
            :start_time,
            :end_time,
            :execution_time_seconds,
            :error_message
        );

    """),
    {
        "pipeline_name": pipeline_name,
        "layer_name": layer_name,
        "table_name": table_name,
        "status": status,
        "rows_processed": rows_processed,
        "start_time": start_time,
        "end_time": end_time,
        "execution_time_seconds": execution_time_seconds,
        "error_message": error_message
    })

    logging.info(f"Audit Log Inserted : {table_name}")


# =====================================================
# Generic ETL Runner
# =====================================================

def run_etl_step(
    conn,
    pipeline_name,
    layer_name,
    table_name,
    schema_name,
    etl_function
):

    start_time = datetime.now()
    start = time.time()

    try:

        logging.info("=" * 60)
        logging.info(f"Starting {table_name}")

        # Execute ETL Function
        etl_function(conn)

        # Get Row Count
        rows = get_row_count(
            conn,
            schema_name,
            table_name
        )

        end_time = datetime.now()

        execution_time = round(
            time.time() - start,
            2
        )

        # Success Audit
        insert_audit_log(
            conn=conn,
            pipeline_name=pipeline_name,
            layer_name=layer_name,
            table_name=table_name,
            status="Success",
            rows_processed=rows,
            start_time=start_time,
            end_time=end_time,
            execution_time_seconds=execution_time,
            error_message=None
        )

        logging.info(f"{table_name} Completed Successfully")
        logging.info("=" * 60)

    except Exception as e:

        end_time = datetime.now()

        execution_time = round(
            time.time() - start,
            2
        )

        # Failed Audit
        insert_audit_log(
            conn=conn,
            pipeline_name=pipeline_name,
            layer_name=layer_name,
            table_name=table_name,
            status="Failed",
            rows_processed=0,
            start_time=start_time,
            end_time=end_time,
            execution_time_seconds=execution_time,
            error_message=str(e)
        )

        logging.error(f"{table_name} Failed")
        logging.error(e)

        raise


# =====================================================
# Main Function
# =====================================================

def main():

    try:

        with engine.begin() as conn:

            create_audit_table(conn)

            logging.info("=" * 60)
            logging.info("Audit Framework Ready")
            logging.info("=" * 60)

    except Exception as e:

        logging.error(e)


# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()