import logging

from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from config.db_config import DB_CONFIG

from scripts.audit.audit_framework import run_etl_step


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
# Create Silver Schema
# =====================================================

def create_silver_schema(conn):

    conn.execute(text("""
        CREATE SCHEMA IF NOT EXISTS silver;
    """))

    

    logging.info("Silver schema is ready.")


# =====================================================
# Clean AISLES
# =====================================================

def clean_aisles(conn):

    logging.info("Cleaning aisles table...")

    conn.execute(text("""

        DROP TABLE IF EXISTS silver.aisles;

        CREATE TABLE silver.aisles AS

        SELECT DISTINCT

            aisle_id,

            TRIM(aisle) AS aisle

        FROM bronze.aisles

        WHERE aisle_id IS NOT NULL
          AND aisle IS NOT NULL;

    """))

    

    logging.info("aisles table completed.")


# =====================================================
# Clean DEPARTMENTS
# =====================================================

def clean_departments(conn):

    logging.info("Cleaning departments table...")

    conn.execute(text("""

        DROP TABLE IF EXISTS silver.departments;

        CREATE TABLE silver.departments AS

        SELECT DISTINCT

            department_id,

            TRIM(department) AS department

        FROM bronze.departments

        WHERE department_id IS NOT NULL
          AND department IS NOT NULL;

    """))

    

    logging.info("departments table completed.")

    # =====================================================
# Clean PRODUCTS
# =====================================================

def clean_products(conn):

    logging.info("Cleaning products table...")

    conn.execute(text("""

        DROP TABLE IF EXISTS silver.products;

        CREATE TABLE silver.products AS

        SELECT DISTINCT

            product_id,

            TRIM(product_name) AS product_name,

            aisle_id,

            department_id

        FROM bronze.products

        WHERE product_id IS NOT NULL
          AND product_name IS NOT NULL
          AND aisle_id IS NOT NULL
          AND department_id IS NOT NULL;

    """))

    

    logging.info("products table completed.")


# =====================================================
# Clean ORDERS
# =====================================================

def clean_orders(conn):

    logging.info("Cleaning orders table...")

    conn.execute(text("""

        DROP TABLE IF EXISTS silver.orders;

        CREATE TABLE silver.orders AS

        SELECT DISTINCT

            order_id,
            user_id,
            eval_set,
            order_number,
            order_dow,
            order_hour_of_day,
            days_since_prior_order

        FROM bronze.orders

        WHERE order_id IS NOT NULL
          AND user_id IS NOT NULL
          AND order_number > 0
          AND order_dow BETWEEN 0 AND 6
          AND order_hour_of_day BETWEEN 0 AND 23;

    """))

    

    logging.info("orders table completed.")


# =====================================================
# Clean ORDER_PRODUCTS__PRIOR
# =====================================================

def clean_prior(conn):

    logging.info("Cleaning order_products__prior table...")

    conn.execute(text("""

        DROP TABLE IF EXISTS silver.order_products__prior;

        CREATE TABLE silver.order_products__prior AS

        SELECT DISTINCT

            order_id,
            product_id,
            add_to_cart_order,
            reordered

        FROM bronze.order_products__prior

        WHERE order_id IS NOT NULL
          AND product_id IS NOT NULL
          AND add_to_cart_order > 0
          AND reordered IN (0,1);

    """))

    

    logging.info("order_products__prior completed.")


# =====================================================
# Clean ORDER_PRODUCTS__TRAIN
# =====================================================

def clean_train(conn):

    logging.info("Cleaning order_products__train table...")

    conn.execute(text("""

        DROP TABLE IF EXISTS silver.order_products__train;

        CREATE TABLE silver.order_products__train AS

        SELECT DISTINCT

            order_id,
            product_id,
            add_to_cart_order,
            reordered

        FROM bronze.order_products__train

        WHERE order_id IS NOT NULL
          AND product_id IS NOT NULL
          AND add_to_cart_order > 0
          AND reordered IN (0,1);

    """))

    

    logging.info("order_products__train completed.")

 # =====================================================
# Main Function
# =====================================================

def main():

    try:

        with engine.begin() as conn:

            logging.info("=" * 60)
            logging.info("Starting Bronze → Silver Transformation")

            create_silver_schema(conn)

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Silver",
                table_name="aisles",
                schema_name="silver",
                etl_function=clean_aisles
            )

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Silver",
                table_name="departments",
                schema_name="silver",
                etl_function=clean_departments
            )

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Silver",
                table_name="products",
                schema_name="silver",
                etl_function=clean_products
            )

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Silver",
                table_name="orders",
                schema_name="silver",
                etl_function=clean_orders
            )

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Silver",
                table_name="order_products__prior",
                schema_name="silver",
                etl_function=clean_prior
            )

            run_etl_step(
                conn=conn,
                pipeline_name="Instacart_ETL",
                layer_name="Silver",
                table_name="order_products__train",
                schema_name="silver",
                etl_function=clean_train
            )

            logging.info("=" * 60)
            logging.info("Silver Layer Completed Successfully")
            logging.info("=" * 60)

    except Exception as e:

        logging.error("=" * 60)
        logging.error("Bronze → Silver Transformation Failed")
        logging.error(e)
        logging.error("=" * 60)




# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()