from psycopg_pool import ConnectionPool
from app.config.settings import settings
from pgvector.psycopg import register_vector

def configure_connection(conn):
    return register_vector(conn)


pool = ConnectionPool(
    conninfo=(
        f"host={settings.DB_HOST} "
        f"port={settings.DB_PORT} "
        f"dbname={settings.DB_NAME} "
        f"user={settings.DB_USER} "
        f"password={settings.DB_PASSWORD}"
    ),
    min_size=2,
    max_size=10,
    configure=configure_connection
)