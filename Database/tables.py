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
                DROP TABLE IF EXISTS usuarios;
                DROP TABLE IF EXISTS correos;
                DROP TABLE IF EXISTS productos;
                DROP TABLE IF EXISTS descripciones;
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
                    product_id INTEGER NOT NULL,
                    log VARCHAR(250) NOT NULL,
                    date TIMESTAMP NOT NULL,
                    CONSTRAINT product_fk FOREIGN KEY (product_id) 
                    REFERENCES product(product_id) ON DELETE CASCADE,
                    CONSTRAINT user_fk FOREIGN KEY (user_id)
                    REFERENCES users(user_id) ON DELETE CASCADE
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




