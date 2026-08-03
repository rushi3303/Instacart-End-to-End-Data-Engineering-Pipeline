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
# Incremental Metadata Functions
# =====================================================

def get_last_processed_key(conn, table_name):
    result = conn.execute(
        text("""
            SELECT last_processed_key
            FROM metadata.incremental_tracking
            WHERE layer_name = 'gold'
              AND table_name = :table_name;
        """),
        {"table_name": table_name}
    ).fetchone()

    if result is None:
        return 0

    return result[0]

def update_last_processed_key(conn, table_name, last_key):

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
                'gold',
                :table_name,
                :last_key,
                CURRENT_TIMESTAMP,
                'SUCCESS'
            )

            ON CONFLICT(layer_name, table_name)

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

def get_max_key(conn, schema_name, table_name, key_column):

    result = conn.execute(
        text(f"""
            SELECT COALESCE(MAX({key_column}),0)
            FROM {schema_name}.{table_name};
        """)
    ).scalar()

    return result  

def create_gold_tables(conn):

    logging.info("Creating Gold tables...")

    conn.execute(text("""

    CREATE TABLE IF NOT EXISTS gold.product_dimension
    (
        product_id BIGINT PRIMARY KEY,
        product_name TEXT,
        aisle TEXT,
        department TEXT
    );

    CREATE TABLE IF NOT EXISTS gold.order_fact
    (
        order_id BIGINT,
        user_id BIGINT,
        order_number BIGINT,
        order_dow BIGINT,
        order_hour_of_day BIGINT,
        eval_set TEXT,
        product_id BIGINT,
        product_name TEXT,
        add_to_cart_order BIGINT,
        reordered BIGINT,
        PRIMARY KEY(order_id, product_id)
    );

    CREATE TABLE IF NOT EXISTS gold.customer_summary
    (
        user_id BIGINT PRIMARY KEY,
        total_orders BIGINT,
        last_order_number BIGINT
    );

    CREATE TABLE IF NOT EXISTS gold.sales_summary
    (
        department TEXT PRIMARY KEY,
        total_products_sold BIGINT,
        total_orders BIGINT
    );

    """))

    logging.info("Gold tables are ready.")

      
# =====================================================
# Product Dimension
# =====================================================

def create_product_dimension(conn):

    logging.info("Creating Product Dimension...")

    last_key = get_last_processed_key(
        conn,
        "product_dimension"
    )

    logging.info(f"Last Processed Product ID : {last_key}")

    conn.execute(
        text("""

        INSERT INTO gold.product_dimension
        (
            product_id,
            product_name,
            aisle,
            department
        )

        SELECT

            p.product_id,
            p.product_name,
            a.aisle,
            d.department

        FROM silver.products p

        LEFT JOIN silver.aisles a
            ON p.aisle_id = a.aisle_id

        LEFT JOIN silver.departments d
            ON p.department_id = d.department_id

        WHERE p.product_id > :last_key

        ON CONFLICT (product_id)

        DO UPDATE
        SET

            product_name = EXCLUDED.product_name,
            aisle = EXCLUDED.aisle,
            department = EXCLUDED.department;

        """),
        {
            "last_key": last_key
        }
    )

    latest_key = get_max_key(
        conn,
        "gold",
        "product_dimension",
        "product_id"
    )

    update_last_processed_key(
        conn,
        "product_dimension",
        latest_key
    )
    product_count = conn.execute(
    text("""
        SELECT COUNT(*)
        FROM gold.product_dimension;
    """)
    ).scalar()

    logging.info(f"Product Dimension Rows : {product_count}")
    logging.info(f"Latest Product ID : {latest_key}")
    logging.info("Product Dimension Completed Successfully")

# =====================================================
# Main Function
# =====================================================

def main():
    
    try:

        with engine.begin() as conn:

            logging.info("=" * 60)
            logging.info("Starting Silver → Gold Transformation")

            create_gold_schema(conn)
            create_gold_tables(conn)

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

    last_key = get_last_processed_key(
        conn,
        "order_fact"
    )

    logging.info(f"Last Processed Order ID : {last_key}")

    conn.execute(
        text("""

        INSERT INTO gold.order_fact
        (
            order_id,
            user_id,
            order_number,
            order_dow,
            order_hour_of_day,
            eval_set,
            product_id,
            product_name,
            add_to_cart_order,
            reordered
        )

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
            ON op.product_id = p.product_id

        WHERE o.order_id > :last_key

        ON CONFLICT (order_id, product_id)

        DO UPDATE
        SET

            user_id = EXCLUDED.user_id,
            order_number = EXCLUDED.order_number,
            order_dow = EXCLUDED.order_dow,
            order_hour_of_day = EXCLUDED.order_hour_of_day,
            eval_set = EXCLUDED.eval_set,
            product_name = EXCLUDED.product_name,
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
        "orders",
        "order_id"
    )

    update_last_processed_key(
        conn,
        "order_fact",
        latest_key
    )
    order_fact_count = conn.execute(
    text("""
        SELECT COUNT(*)
        FROM gold.order_fact;
    """)
    ).scalar()

    logging.info(f"Order Fact Rows : {order_fact_count}")
    logging.info(f"Latest Order ID : {latest_key}")
    logging.info("Order Fact Completed Successfully")

# =====================================================
# Customer Summary
# =====================================================

def create_customer_summary(conn):

    logging.info("Creating Customer Summary...")

    last_key = get_last_processed_key(
        conn,
        "customer_summary"
    )

    logging.info(f"Last Processed Order ID : {last_key}")

    conn.execute(
        text("""

        INSERT INTO gold.customer_summary
        (
            user_id,
            total_orders,
            last_order_number
        )

        SELECT

            user_id,
            COUNT(order_id) AS total_orders,
            MAX(order_number) AS last_order_number

        FROM silver.orders

        WHERE order_id > :last_key

        GROUP BY user_id

        ON CONFLICT (user_id)

        DO UPDATE
        SET

            total_orders =
                gold.customer_summary.total_orders +
                EXCLUDED.total_orders,

            last_order_number =
                GREATEST(
                    gold.customer_summary.last_order_number,
                    EXCLUDED.last_order_number
                );

        """),
        {
            "last_key": last_key
        }
    )

    latest_key = get_max_key(
        conn,
        "silver",
        "orders",
        "order_id"
    )

    update_last_processed_key(
        conn,
        "customer_summary",
        latest_key
    )
    customer_count = conn.execute(
    text("""
        SELECT COUNT(*)
        FROM gold.customer_summary;
    """)
    ).scalar()

    logging.info(f"Customer Summary Rows : {customer_count}")
    logging.info(f"Latest Order ID : {latest_key}")
    logging.info("Customer Summary Completed Successfully")

# =====================================================
# Sales Summary
# =====================================================

def create_sales_summary(conn):

    logging.info("Creating Sales Summary...")

    last_key = get_last_processed_key(
        conn,
        "sales_summary"
    )

    logging.info(f"Last Processed Order ID : {last_key}")

    conn.execute(
        text("""

        INSERT INTO gold.sales_summary
        (
            department,
            total_products_sold,
            total_orders
        )

        SELECT

            p.department,
            COUNT(*) AS total_products_sold,
            COUNT(DISTINCT o.order_id) AS total_orders

        FROM gold.order_fact o

        INNER JOIN gold.product_dimension p
            ON o.product_id = p.product_id

        WHERE o.order_id > :last_key

        GROUP BY p.department

        ON CONFLICT (department)

        DO UPDATE
        SET

            total_products_sold =
                gold.sales_summary.total_products_sold +
                EXCLUDED.total_products_sold,

            total_orders =
                gold.sales_summary.total_orders +
                EXCLUDED.total_orders;

        """),
        {
            "last_key": last_key
        }
    )

    latest_key = get_max_key(
        conn,
        "silver",
        "orders",
        "order_id"
    )

    update_last_processed_key(
        conn,
        "sales_summary",
        latest_key
    )
    sales_count = conn.execute(
    text("""
        SELECT COUNT(*)
        FROM gold.sales_summary;
    """)
    ).scalar()

    logging.info(f"Sales Summary Rows : {sales_count}")
    logging.info(f"Latest Order ID : {latest_key}")
    logging.info("Sales Summary Completed Successfully")

# =====================================================
# Driver Code
# =====================================================

if __name__ == "__main__":

    main()