import logging

from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from config.db_config import DB_CONFIG

from scripts.audit.audit_framework import run_etl_step

# =====================================================
# Incremental Metadata Functions
# =====================================================


def get_last_processed_key(conn, table_name):
    """
    Get last processed key from metadata.incremental_tracking
    """

    result = conn.execute(
        text("""
            SELECT last_processed_key
            FROM metadata.incremental_tracking
            WHERE layer_name = 'silver'
              AND table_name = :table_name;
        """),
        {"table_name": table_name}
    ).fetchone()

    if result is None:
        return 0

    return result[0]


def update_last_processed_key(conn, table_name, last_key):
    """
    Insert or Update metadata after successful load
    """

    conn.execute(
        text("""
            INSERT INTO metadata.incremental_tracking
            (
                layer_name,
                table_name,
                last_processed_key,
                last_run,
                status
            )
            VALUES
            (
                'silver',
                :table_name,
                :last_key,
                CURRENT_TIMESTAMP,
                'SUCCESS'
            )

            ON CONFLICT (layer_name, table_name)

            DO UPDATE
            SET
                last_processed_key = EXCLUDED.last_processed_key,
                last_run = EXCLUDED.last_run,
                status = EXCLUDED.status;
        """),
        {
            "table_name": table_name,
            "last_key": last_key
        }
    )

    
    

# =====================================================
# Helper Function
# =====================================================

def get_max_key(conn, schema_name, table_name, key_column):
    """
    Get maximum processed key
    """

    result = conn.execute(
        text(f"""
            SELECT COALESCE(MAX({key_column}),0)
            FROM {schema_name}.{table_name};
        """)
    ).scalar()

    return result

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

def create_silver_tables(conn):

    logging.info("Creating Silver tables...")

    conn.execute(text("""

    CREATE TABLE IF NOT EXISTS silver.aisles
    (
        aisle_id BIGINT PRIMARY KEY,
        aisle TEXT
    );

    CREATE TABLE IF NOT EXISTS silver.departments
    (
        department_id BIGINT PRIMARY KEY,
        department TEXT
    );

    CREATE TABLE IF NOT EXISTS silver.products
    (
        product_id BIGINT PRIMARY KEY,
        product_name TEXT,
        aisle_id BIGINT,
        department_id BIGINT
    );

    CREATE TABLE IF NOT EXISTS silver.orders
    (
        order_id BIGINT PRIMARY KEY,
        user_id BIGINT,
        eval_set TEXT,
        order_number BIGINT,
        order_dow BIGINT,
        order_hour_of_day BIGINT,
        days_since_prior_order DOUBLE PRECISION
    );

    CREATE TABLE IF NOT EXISTS silver.order_products__prior
    (
        order_id BIGINT,
        product_id BIGINT,
        add_to_cart_order BIGINT,
        reordered BIGINT,
        PRIMARY KEY(order_id, product_id)
    );

    CREATE TABLE IF NOT EXISTS silver.order_products__train
    (
        order_id BIGINT,
        product_id BIGINT,
        add_to_cart_order BIGINT,
        reordered BIGINT,
        PRIMARY KEY(order_id, product_id)
    );

    """))

    logging.info("Silver tables are ready.")

# =====================================================
# Clean AISLES
# =====================================================

def clean_aisles(conn):

    logging.info("Cleaning aisles table...")

    conn.execute(text("""

    TRUNCATE TABLE silver.aisles;

    INSERT INTO silver.aisles
    (
    aisle_id,
    aisle
    )

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

    TRUNCATE TABLE silver.departments;

    INSERT INTO silver.departments
    (
    department_id,
    department
    )

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

    # Read last processed key
    last_key = get_last_processed_key(
        conn,
        "products"
    )

    logging.info(f"Last Processed Product ID : {last_key}")

    conn.execute(
        text("""

        INSERT INTO silver.products
        (
            product_id,
            product_name,
            aisle_id,
            department_id
        )

        SELECT

            product_id,
            TRIM(product_name),
            aisle_id,
            department_id

        FROM bronze.products

        WHERE product_id > :last_key
          AND product_id IS NOT NULL
          AND product_name IS NOT NULL
          AND aisle_id IS NOT NULL
          AND department_id IS NOT NULL

        ON CONFLICT (product_id)

        DO UPDATE
        SET

            product_name = EXCLUDED.product_name,
            aisle_id = EXCLUDED.aisle_id,
            department_id = EXCLUDED.department_id;

        """),
        {
            "last_key": last_key
        }
    )

    latest_key = get_max_key(
        conn,
        "silver",
        "products",
        "product_id"
    )

    update_last_processed_key(
        conn,
        "products",
        latest_key
    )

    logging.info(f"Latest Product ID : {latest_key}")
    logging.info("products table completed.")

# =====================================================
# Clean ORDERS
# =====================================================
def clean_orders(conn):

    logging.info("Cleaning orders table...")

    # Read last processed key
    last_key = get_last_processed_key(conn, "orders")

    logging.info(f"Last Processed Order ID : {last_key}")

    # Incremental UPSERT
    conn.execute(
        text("""

        INSERT INTO silver.orders
        (
            order_id,
            user_id,
            eval_set,
            order_number,
            order_dow,
            order_hour_of_day,
            days_since_prior_order
        )

        SELECT

            order_id,
            user_id,
            eval_set,
            order_number,
            order_dow,
            order_hour_of_day,
            days_since_prior_order

        FROM bronze.orders

        WHERE order_id > :last_key
          AND order_id IS NOT NULL
          AND user_id IS NOT NULL
          AND order_number > 0
          AND order_dow BETWEEN 0 AND 6
          AND order_hour_of_day BETWEEN 0 AND 23

        ON CONFLICT (order_id)

        DO UPDATE
        SET

            user_id = EXCLUDED.user_id,
            eval_set = EXCLUDED.eval_set,
            order_number = EXCLUDED.order_number,
            order_dow = EXCLUDED.order_dow,
            order_hour_of_day = EXCLUDED.order_hour_of_day,
            days_since_prior_order = EXCLUDED.days_since_prior_order;

        """),
        {
            "last_key": last_key
        }
    )

    # Get latest processed key
    latest_key = get_max_key(
        conn,
        "silver",
        "orders",
        "order_id"
    )
    
    
    # Update metadata
    update_last_processed_key(
        conn,
        "orders",
        latest_key
    )

    logging.info(f"Latest Order ID : {latest_key}")
    logging.info("orders table completed.")

# =====================================================
# Clean ORDER_PRODUCTS__PRIOR
# =====================================================

def clean_prior(conn):

    logging.info("Cleaning order_products__prior table...")

    last_key = get_last_processed_key(
        conn,
        "order_products__prior"
    )

    logging.info(f"Last Processed Order ID : {last_key}")

    conn.execute(
        text("""

        INSERT INTO silver.order_products__prior
        (
            order_id,
            product_id,
            add_to_cart_order,
            reordered
        )

        SELECT

            order_id,
            product_id,
            add_to_cart_order,
            reordered

        FROM bronze.order_products__prior

        WHERE order_id > :last_key
          AND order_id IS NOT NULL
          AND product_id IS NOT NULL
          AND add_to_cart_order > 0
          AND reordered IN (0,1)

        ON CONFLICT (order_id, product_id)

        DO UPDATE
        SET

            add_to_cart_order = EXCLUDED.add_to_cart_order,
            reordered = EXCLUDED.reordered;

        """),
        {
            "last_key": last_key
        }
    )

    latest_key = get_max_key(
        conn,
        "silver",
        "order_products__prior",
        "order_id"
    )

    update_last_processed_key(
        conn,
        "order_products__prior",
        latest_key
    )

    logging.info(f"Latest Order ID : {latest_key}")
    logging.info("order_products__prior completed.")

# =====================================================
# Clean ORDER_PRODUCTS__TRAIN
# =====================================================

def clean_train(conn):

    logging.info("Cleaning order_products__train table...")

    last_key = get_last_processed_key(
        conn,
        "order_products__train"
    )

    logging.info(f"Last Processed Order ID : {last_key}")

    conn.execute(
        text("""

        INSERT INTO silver.order_products__train
        (
            order_id,
            product_id,
            add_to_cart_order,
            reordered
        )

        SELECT

            order_id,
            product_id,
            add_to_cart_order,
            reordered

        FROM bronze.order_products__train

        WHERE order_id > :last_key
          AND order_id IS NOT NULL
          AND product_id IS NOT NULL
          AND add_to_cart_order > 0
          AND reordered IN (0,1)

        ON CONFLICT (order_id, product_id)

        DO UPDATE
        SET

            add_to_cart_order = EXCLUDED.add_to_cart_order,
            reordered = EXCLUDED.reordered;

        """),
        {
            "last_key": last_key
        }
    )

    latest_key = get_max_key(
        conn,
        "silver",
        "order_products__train",
        "order_id"
    )

    update_last_processed_key(
        conn,
        "order_products__train",
        latest_key
    )

    logging.info(f"Latest Order ID : {latest_key}")
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
            create_silver_tables(conn)
            
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