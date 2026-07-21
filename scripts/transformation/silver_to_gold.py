import logging

from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from config.db_config import DB_CONFIG


from scripts.audit.audit_framework import run_etl_step

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)


def create_gold_schema(conn):

    conn.execute(text("""
        CREATE SCHEMA IF NOT EXISTS gold;
    """))

    

    logging.info("Gold Schema Created Successfully")


# =====================================================
# Product Dimension
# =====================================================

def create_product_dimension(conn):

    logging.info("Creating Product Dimension...")

    conn.execute(text("""
        DROP TABLE IF EXISTS gold.product_dimension;
    """))

    conn.execute(text("""

        CREATE TABLE gold.product_dimension AS

        SELECT
            p.product_id,
            p.product_name,
            a.aisle,
            d.department

        FROM silver.products p

        LEFT JOIN silver.aisles a
            ON p.aisle_id = a.aisle_id

        LEFT JOIN silver.departments d
            ON p.department_id = d.department_id;

    """))

    logging.info("Product Dimension Created Successfully")

# =====================================================
# Main Function
# =====================================================

def main():
    
    try:

        with engine.begin() as conn:

            logging.info("=" * 60)
            logging.info("Starting Silver → Gold Transformation")

            create_gold_schema(conn)

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Gold",
                table_name="product_dimension",
                schema_name="gold",
                etl_function=create_product_dimension
            )

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Gold",
                table_name="order_fact",
                schema_name="gold",
                etl_function=create_order_fact
            )

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Gold",
                table_name="customer_summary",
                schema_name="gold",
                etl_function=create_customer_summary
            )

            run_etl_step(
               conn=conn,
               pipeline_name="Instacart_ETL",
               layer_name="Gold",
               table_name="sales_summary",
              schema_name="gold",
               etl_function=create_sales_summary
)



            logging.info("=" * 60)
            logging.info("Gold Layer Completed Successfully")
            logging.info("=" * 60)

    except Exception as e:

        logging.error("=" * 60)
        logging.error("Gold Layer Failed")
        logging.error(e)
        logging.error("=" * 60)

# =====================================================
# Order Fact
# =====================================================

def create_order_fact(conn):

    logging.info("Creating Order Fact Table...")

    conn.execute(text("""

        DROP TABLE IF EXISTS gold.order_fact;

        CREATE TABLE gold.order_fact AS

        SELECT

            o.order_id,
            o.user_id,
            o.order_number,
            o.order_dow,
            o.order_hour_of_day,
            o.eval_set,

            op.product_id,
            p.product_name,

            op.add_to_cart_order,
            op.reordered

        FROM silver.orders o

        INNER JOIN silver.order_products__prior op
            ON o.order_id = op.order_id

        INNER JOIN silver.products p
            ON op.product_id = p.product_id;

    """))

    logging.info("Order Fact Table Created Successfully")

# =====================================================
# Customer Summary
# =====================================================

def create_customer_summary(conn):

    logging.info("Creating Customer Summary...")

    conn.execute(text("""

        DROP TABLE IF EXISTS gold.customer_summary;

        CREATE TABLE gold.customer_summary AS

        SELECT

            user_id,
            COUNT(DISTINCT order_id) AS total_orders,
            MAX(order_number) AS last_order_number

        FROM silver.orders

        GROUP BY user_id;

    """))

    logging.info("Customer Summary Created Successfully")

# =====================================================
# Sales Summary
# =====================================================

def create_sales_summary(conn):

    logging.info("Creating Sales Summary...")

    conn.execute(text("""

        DROP TABLE IF EXISTS gold.sales_summary;

        CREATE TABLE gold.sales_summary AS

        SELECT

            p.department,
            COUNT(*) AS total_products_sold,
            COUNT(DISTINCT o.order_id) AS total_orders

        FROM gold.order_fact o

        INNER JOIN gold.product_dimension p
            ON o.product_id = p.product_id

        GROUP BY p.department

        ORDER BY total_orders DESC;

    """))

    logging.info("Sales Summary Created Successfully")

# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()