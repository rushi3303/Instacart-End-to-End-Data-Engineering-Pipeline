from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from config.db_config import DB_CONFIG

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

tables = [
    "product_dimension",
    "order_fact",
    "customer_summary",
    "sales_summary"
]

with engine.connect() as conn:

    for table in tables:

        print("\n" + "=" * 70)
        print(f"Table : {table}")

        # ----------------------------
        # Row Count
        # ----------------------------

        result = conn.execute(text(f"""
            SELECT COUNT(*)
            FROM gold.{table};
        """))

        print("\nTotal Rows :", result.scalar())

        # ----------------------------
        # Top 5 Records
        # ----------------------------

        result = conn.execute(text(f"""
            SELECT *
            FROM gold.{table}
            LIMIT 5;
        """))

        print("\nTop 5 Rows\n")

        for row in result:
            print(row)

print("\n Gold Validation Completed Successfully")