import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "mysql.railway.internal"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASS", "aYkEPORYTNdnxqhWMlmgLoVKyQIYKLeM"),
        database=os.environ.get("DB_NAME", "railway"),
        port=int(os.environ.get("DB_PORT", 3306))
    )
