from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from config.db_config import DB_CONFIG


# =====================================================
# Database Connection
# =====================================================

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:"
    f"{DB_CONFIG['port']}/"
    f"{DB_CONFIG['database']}"
)


# =====================================================
# Test PostgreSQL Connection
# =====================================================

def test_connection():

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("SELECT current_database();")
            )

            database_name = result.scalar()

            print(
                f"Connected Successfully to PostgreSQL Database: "
                f"{database_name}"
            )

    except Exception as e:

        print(f"Database Connection Failed: {e}")


# =====================================================
# Get Top Products
# =====================================================

def get_top_products(limit):

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        p.product_id,
                        p.product_name,
                        COUNT(*) AS total_orders

                    FROM gold.order_fact AS o

                    INNER JOIN gold.product_dimension AS p
                        ON o.product_id = p.product_id

                    GROUP BY
                        p.product_id,
                        p.product_name

                    ORDER BY
                        total_orders DESC

                    LIMIT :limit;
                """),
                {"limit": limit}
            )

            return result.fetchall()

    except Exception as e:

        print(
            f"Error while fetching Top Products: {e}"
        )

        return []


# =====================================================
# Get Sales Summary
# =====================================================

def get_sales_summary():

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        department,
                        total_products_sold,
                        total_orders

                    FROM gold.sales_summary

                    ORDER BY
                        total_orders DESC;
                """)
            )

            return result.fetchall()

    except Exception as e:

        print(
            f"Error while fetching Sales Summary: {e}"
        )

        return []

# =====================================================
# Get Customer Summary
# =====================================================

def get_customer_summary(limit=10):

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        user_id,
                        total_orders,
                        last_order_number

                    FROM gold.customer_summary

                    ORDER BY
                        total_orders DESC

                    LIMIT :limit;
                """),
                {"limit": limit}
            )

            return result.fetchall()

    except Exception as e:

        print(
            f"Error while fetching Customer Summary: {e}"
        )

        return []


# =====================================================
# Get Product History (SCD Type 2)
# =====================================================

def get_product_history(product_id):

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        product_id,
                        product_name,
                        department,
                        aisle,
                        effective_date,
                        end_date,
                        is_current

                    FROM gold.product_dimension_history

                    WHERE product_id = :product_id

                    ORDER BY
                        effective_date ASC;
                """),
                {"product_id": product_id}
            )

            return result.fetchall()

    except Exception as e:

        print(
            f"Error while fetching Product History: {e}"
        )

        return []


# =====================================================
# Get ETL Status (Latest Run)
# =====================================================

def get_etl_status(limit=10):

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        pipeline_name,
                        layer_name,
                        table_name,
                        status,
                        rows_processed,
                        start_time,
                        end_time,
                        execution_time_seconds,
                        error_message

                    FROM audit.audit_log

                    ORDER BY
                        audit_id DESC

                    LIMIT :limit;
                """),
                {"limit": limit}
            )

            return result.fetchall()

    except Exception as e:

        print(
            f"Error while fetching ETL Status: {e}"
        )

        return []


# =====================================================
# Get ETL History (Grouped by Run Date)
# =====================================================

def get_etl_history(limit=5):

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        DATE(start_time) AS run_date,
                        COUNT(*) AS total_tables,
                        SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) AS success_tables,
                        SUM(CASE WHEN status != 'Success' THEN 1 ELSE 0 END) AS failed_tables,
                        SUM(rows_processed) AS total_rows_processed,
                        ROUND(SUM(execution_time_seconds)::numeric, 2) AS total_execution_time

                    FROM audit.audit_log

                    GROUP BY
                        DATE(start_time)

                    ORDER BY
                        run_date DESC

                    LIMIT :limit;
                """),
                {"limit": limit}
            )

            return result.fetchall()

    except Exception as e:

        print(
            f"Error while fetching ETL History: {e}"
        )

        return []


# =====================================================
# Get Data Quality Status
# =====================================================

def get_data_quality_status():

    try:

        with engine.connect() as conn:

            file_stats = conn.execute(
                text("""
                    SELECT
                        COUNT(*) AS total_files,
                        SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_files,
                        SUM(CASE WHEN status != 'SUCCESS' THEN 1 ELSE 0 END) AS failed_files,
                        MAX(last_loaded) AS latest_load_time
                    FROM metadata.file_tracking;
                """)
            ).fetchone()

            audit_stats = conn.execute(
                text("""
                    SELECT
                        layer_name,
                        COUNT(*) AS total_tables,
                        SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) AS success_tables,
                        SUM(CASE WHEN status != 'Success' THEN 1 ELSE 0 END) AS failed_tables,
                        MAX(end_time) AS latest_time
                    FROM (
                        SELECT DISTINCT ON (layer_name, table_name)
                            layer_name, table_name, status, end_time
                        FROM audit.audit_log
                        ORDER BY layer_name, table_name, end_time DESC
                    ) sub
                    GROUP BY layer_name;
                """)
            ).fetchall()

            return {
                "file_stats": file_stats,
                "audit_stats": audit_stats
            }

    except Exception as e:

        print(
            f"Error while fetching Data Quality Status: {e}"
        )

        return None


# =====================================================
# Get Rejected Records Summary
# =====================================================

def get_rejected_records():

    try:

        with engine.connect() as conn:

            audit_failures = conn.execute(
                text("""
                    SELECT
                        layer_name,
                        table_name,
                        status,
                        error_message,
                        end_time
                    FROM audit.audit_log
                    WHERE status != 'Success'
                       OR error_message IS NOT NULL
                    ORDER BY end_time DESC;
                """)
            ).fetchall()

            file_failures = conn.execute(
                text("""
                    SELECT
                        file_name,
                        status,
                        last_loaded
                    FROM metadata.file_tracking
                    WHERE status != 'SUCCESS';
                """)
            ).fetchall()

            return {
                "audit_failures": audit_failures,
                "file_failures": file_failures
            }

    except Exception as e:

        print(
            f"Error while fetching Rejected Records: {e}"
        )

        return None

def execute_read_only_query(sql):
    """
    Executes only safe read-only SQL queries.
    """

    sql_clean = sql.strip().lower()

    # Only SELECT / WITH queries are allowed
    if not (sql_clean.startswith("select") or sql_clean.startswith("with")):
        return {
            "success": False,
            "error": "Only read-only SELECT queries are allowed."
        }

    # Block dangerous SQL operations
    blocked_keywords = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "grant ",
        "revoke ",
        "execute ",
        "call "
    ]

    if any(keyword in sql_clean for keyword in blocked_keywords):
        return {
            "success": False,
            "error": "Unsafe SQL operation detected."
        }

    # Prevent multiple statements
    if ";" in sql_clean.rstrip(";"):
        return {
            "success": False,
            "error": "Multiple SQL statements are not allowed."
        }

    try:

        with engine.connect() as conn:

            result = conn.execute(text(sql))

            rows = result.fetchall()
            columns = result.keys()

            data = [
                dict(zip(columns, row))
                for row in rows
            ]

            return {
                "success": True,
                "data": data
            }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
