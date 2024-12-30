from conection import get_connection
from psycopg2 import Error

def create_tables() -> bool:
    conn = get_connection()

    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        delete="""
                DROP TABLE IF EXISTS change_log;
                DROP TABLE IF EXISTS users;
                DROP TABLE IF EXISTS product;
                """
        
        delete2="""
                DROP TABLE change_log;
                """

        create = """
                CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    email VARCHAR(250) NOT NULL UNIQUE,
                    password VARCHAR(250) NOT NULL,
                    verified BOOL DEFAULT(False) 
                );
                CREATE TABLE IF NOT EXISTS product(
                    product_id SERIAL PRIMARY KEY,
                    product_name VARCHAR(100) NOT NULL,
                    price NUMERIC(10, 2) NOT NULL,
                    description VARCHAR(250) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    available BOOL DEFAULT(True),
                    CONSTRAINT positive_price CHECK(price>0)
                );
                CREATE TABLE IF NOT EXISTS change_log(
                    id_log SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    log VARCHAR(250) NOT NULL,
                    date TIMESTAMP NOT NULL
                );
                """
        cursor.execute(create)
        conn.commit()
        return True
    except Error as e:
        print(f'Error: {e.pgerror}')
        return False
    finally:
        cursor.close()
        conn.close()

create_tables()




