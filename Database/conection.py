import psycopg2
import os
from dotenv import load_dotenv


def get_connection():
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        return conn
    except psycopg2.Error as e:
        print(e.pgerror)
        return None
    