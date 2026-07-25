from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config.db_config import DB_CONFIG

password = quote_plus(DB_CONFIG["password"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

with engine.connect() as conn:
    print("✅ Database Connected Successfully!")