import logging
from sqlalchemy import text

# =====================================================
# Create Pipeline Summary Table
# =====================================================

def create_pipeline_summary_table(conn):

    conn.execute(text("""

        CREATE TABLE IF NOT EXISTS audit.pipeline_summary (

            run_id SERIAL PRIMARY KEY,

            pipeline_name VARCHAR(100) NOT NULL,

            pipeline_status VARCHAR(20) NOT NULL,

            total_tables INT NOT NULL,

            success_tables INT NOT NULL,

            failed_tables INT NOT NULL,

            start_time TIMESTAMP,

            end_time TIMESTAMP,

            execution_time_seconds NUMERIC(10,2),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

    """))

    logging.info("Pipeline Summary Table Ready")


# =====================================================
# Insert Pipeline Summary
# =====================================================

def insert_pipeline_summary(
    conn,
    pipeline_name,
    pipeline_status,
    total_tables,
    success_tables,
    failed_tables,
    start_time,
    end_time,
    execution_time_seconds
):

    conn.execute(text("""

        INSERT INTO audit.pipeline_summary
        (
            pipeline_name,
            pipeline_status,
            total_tables,
            success_tables,
            failed_tables,
            start_time,
            end_time,
            execution_time_seconds
        )

        VALUES
        (
            :pipeline_name,
            :pipeline_status,
            :total_tables,
            :success_tables,
            :failed_tables,
            :start_time,
            :end_time,
            :execution_time_seconds
        );

    """),
    {
        "pipeline_name": pipeline_name,
        "pipeline_status": pipeline_status,
        "total_tables": total_tables,
        "success_tables": success_tables,
        "failed_tables": failed_tables,
        "start_time": start_time,
        "end_time": end_time,
        "execution_time_seconds": execution_time_seconds
    })

    logging.info("Pipeline Summary Inserted Successfully")


# =====================================================
# Get Latest Pipeline Summary
# =====================================================

def get_latest_pipeline_summary(conn):

    result = conn.execute(text("""

        SELECT *

        FROM audit.pipeline_summary

        ORDER BY run_id DESC

        LIMIT 1;

    """))

    return result.fetchone()


# =====================================================
# Get Pipeline History
# =====================================================

def get_pipeline_history(conn):

    result = conn.execute(text("""

        SELECT *

        FROM audit.pipeline_summary

        ORDER BY run_id DESC;

    """))

    return result.fetchall()