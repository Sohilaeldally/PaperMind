from psycopg_pool import ConnectionPool
from app.config.settings import settings


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
)