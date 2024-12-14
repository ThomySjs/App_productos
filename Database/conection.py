import psycopg2
import os

def get_connection():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        return conn
    except psycopg2.Error as e:
        print(e.pgerror)
        return None
    