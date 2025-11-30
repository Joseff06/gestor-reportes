import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
import motor.motor_asyncio

# 1. Cargar variables del archivo .env
load_dotenv()

# --- CONFIGURACIÓN SQL (PostgreSQL) ---
sql_user = os.getenv("SQL_USER")
sql_pass = os.getenv("SQL_PASSWORD")
sql_host = os.getenv("SQL_HOST")
sql_port = os.getenv("SQL_PORT")
sql_db = os.getenv("SQL_DB")

# Construcción dinámica de la URL
SQL_URL = f"postgresql://{sql_user}:{sql_pass}@{sql_host}:{sql_port}/{sql_db}"

sql_engine = create_engine(SQL_URL)

def get_sql_session():
    with Session(sql_engine) as session:
        yield session

# --- CONFIGURACIÓN NOSQL (MongoDB) ---
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_db_name = os.getenv("MONGO_DB")
mongo_collection_name = os.getenv("MONGO_COLLECTION")

# Construcción dinámica de la URL
MONGO_URL = f"mongodb://{mongo_host}:{mongo_port}"

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client[mongo_db_name]

# Colección dinámica
pedidos_collection = mongo_db[mongo_collection_name]