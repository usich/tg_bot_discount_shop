import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_URL = os.environ.get("DB_URL")
DB_URL_ALEMBIC = os.environ.get("DB_URL_ALEMBIC")
PGADMIN_USER = os.environ.get("PGADMIN_USER")
PGADMIN_PASSWORD = os.environ.get("PGADMIN_PASSWORD")

URL_1C_API = os.environ.get("URL_1C_API")
USER_1C_API = os.environ.get("USER_1C_API")
PSW_1C_API = os.environ.get("PSW_1C_API")
