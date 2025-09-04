import psycopg2
from dotenv import load_dotenv
import os

load_dotenv() 

DB=os.getenv("DB_NAME")
USER=os.getenv("DB_USER")
PASSWORD=os.getenv("DB_PASSWORD")
HOST=os.getenv("DB_HOST")
PORT=os.getenv("DB_PORT")

SCHEMA_FILE = "database/schema.sql"

with open(SCHEMA_FILE, "r") as f: 
    schema_sql = f.read()


with psycopg2.connect(
    database= DB,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
) as conn: 
    with conn.cursor() as cur: 
        try:
            for statement in schema_sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    cur.execute(stmt + ";")
            conn.commit()
            print("Schema executed successfully")

        except Exception as e: 
            print("Error while executing schema:", e)
            conn.rollback()
