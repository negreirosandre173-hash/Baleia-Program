import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

try:
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Conexão bem-sucedida! Versão do banco: {db_version[0]}")
    cursor.close()
    connection.close()
    print("Conexão fechada.")

except Exception as error:
    print(f"Erro ao conectar: {error}")
