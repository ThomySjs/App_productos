from .conection import get_connection
import bcrypt
import psycopg2
import datetime

class Products():
    """ This class contains all the products queries. """
    @staticmethod
    def get_products(*args) -> tuple:
        """ Return True and the data ordered by the parameter, False and error message if the query fails."""
        conn = get_connection()
        order = args[0]

        if conn is None:
            msg = 'An error has occurred while trying to connect to the database.'
            return (None, msg)
        try:
            cursor = conn.cursor()
            qry = f"""
            SELECT product_id, product_name, price, category, available
            FROM product 
            ORDER BY {order};"""
            cursor.execute(qry)
            data = cursor.fetchall()
            return (True, data)
        except psycopg2.Error as e:
            print(f'Error: {e}')
            msg = 'An error has ocurred while fetching the data.'
            return (False, msg)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_product(name, price, desc, category, available) -> tuple:
        print(name, price, desc, category, available)
        conn = get_connection()

        if conn is None:
            msg = 'An error has occurred while trying to connect to the database.'
            return (None, msg)
        try:
            cursor = conn.cursor()
            qry = """
            INSERT INTO product (product_name, price, description, category, available)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(qry, (name, price, desc, category, available))
            conn.commit()  # Asegúrate de confirmar los cambios
            return True, 'Product added!'
        except psycopg2.Error as e:
            print(f'Error: {e}')
            msg = 'An error has ocurred while adding the product.'
            return (False, msg)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_product(id) -> tuple:
        conn = get_connection()

        if conn is None:
            msg = 'An error occurred while trying to connect to the database.'
            return (False, msg)
        try:

            cursor = conn.cursor()
            qry = """
            DELETE FROM product
            WHERE product_id = %s;
            """
            cursor.execute(qry, (id, ))
            conn.commit()
            if cursor.rowcount == 0:
                msg = 'Product id not found.'
                return (False, msg)
            msg = 'Product deleted!'
            return (True, msg)
        except psycopg2.Error as e:
            print(f'Error: {e}')
            msg = f'An error ocurrrd while deleting the product.\n Error code: {e.pgcode}'
            return (False, msg)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def modify_products(id: int, name: str, price: float, description: str, category: str, available: bool) -> tuple:
        conn = get_connection()

        if conn is None:
            msg = 'An error occurred while trying to connect to the database.'
            return (False, msg)
        try:
            cursor = conn.cursor()

            qry = """ 
            UPDATE product SET product_name = %s, price = %s, description = %s, category = %s, available = %s 
            WHERE product_id = %s;
            """
            cursor.execute(qry, (name, price, description, category, available, id))
            conn.commit()
            if cursor.rowcount == 0:
                msg = 'Product not found'
                return (False, msg)
            msg = 'Product modified.'
            return (True, msg)
        except psycopg2.Error as e:
            print(f'Error code: {e.pgerror}')
            msg = f'An error ocurrrd while modifying the product.\n Error code: {e.pgcode}'
            return (False, msg)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_description(*args) -> tuple:
        """ Return True and the description, False and error message if the query fails."""
        conn = get_connection()
        id = args[0]

        if conn is None:
            msg = 'An error has occurred while trying to connect to the database.'
            return (None, msg)
        try:
            cursor = conn.cursor()
            qry = """
            SELECT description
            FROM product 
            WHERE product_id = %s
            """
            cursor.execute(qry, (id,))
            data = cursor.fetchall()
            return (True, data)
        except psycopg2.Error as e:
            print(f'Error: {e}')
            msg = f'An error has ocurred while fetching the data.\n Error code: {e.pgcode}'
            return (False, msg)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_last_id():
        conn = get_connection()

        if conn is None:
            return None
        try:
            cursor = conn.cursor()

            qry = """
            SELECT product_id 
            FROM product
            ORDER BY product_id
            DESC LIMIT 1;
            """
            cursor.execute(qry)
            data = cursor.fetchall()
            return data
        except psycopg2.Error as e:
            print(f'Error: {e.pgerror}')
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_product_name(id:int):
        conn = get_connection()

        if conn is None:
            return None
        try:
            cursor = conn.cursor()

            qry = """
            SELECT product_name 
            FROM product
            WHERE product_id = %s;
            """
            cursor.execute(qry, (id,))
            data = cursor.fetchone()
            return data
        except psycopg2.Error as e:
            print(f'Error: {e.pgerror}')
            return False
        finally:
            cursor.close()
            conn.close()

class Users():
    @staticmethod
    def exists(email: str) -> bool:
        """ True if the email exists in the database, False if not"""
        conn = get_connection()
        if conn is None:
            return None
        try: 
            cursor = conn.cursor()
            query = 'SELECT COUNT(user_id) FROM users WHERE email=%s;'
            cursor.execute(query, (email,))
            data = cursor.fetchone()
            if 0 in data:
                return False
            return True
        except psycopg2.Error as e:
            print(f'Error: {e.pgerror}')
            return None
        finally:
            cursor.close()
            conn.close()

        
    @staticmethod
    def sign_in(email: str, password: str) -> tuple:
        if not isinstance(email, str) or email.isspace() or email == "" or email.count('@') != 1:
            msg = 'Invalid email syntax.'
            return (False, msg)
        name, dom =  email.split('@')
        dom = f'@{dom}'
        if len(name) < 5 and '.' not in dom or dom.index('.') in (len(dom), 1):
            msg = 'Invalid email syntax'
            return (False, msg)
        if not isinstance(password, str) or len(password) < 5:
            msg = 'The password must contain at least 5 characters.'
            return (False, msg)

        ex = Users.exists(email)
        if ex is None:
            msg = 'An error occurred while trying to connect to the database.'
            return (False, msg)
        if not ex:
            msg = 'The email is not registered.'
            return (False, msg)
        
        else:
            conn = get_connection()
            if conn is None:
                msg = 'An error occurred while trying to connect to the database.'
                return (False, msg)

            try: 
                cursor = conn.cursor()
                query = 'SELECT password FROM users WHERE email=%s'
                cursor.execute(query, (email,))
                data = cursor.fetchone()
            except psycopg2.Error as e:
                print(f'Error: {e.pgerror}')
                msg = 'An error ocurred while validating the data.'
                return (False, msg)
            finally:
                cursor.close()
                conn.close()

            hashed_password = data[0]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')): #checks if the password matches
                msg  = 'Success'
                return (True, msg)
            else: 
                msg = 'Incorrect password.'
                return (False, msg)
    
    @staticmethod
    def register(name: str, email: str, password: str) -> tuple:
        if not isinstance(name, str) or name.isdigit() or name.isspace() or name == "":
            msg = 'Invalid name'
            return (False, msg)
        if not isinstance(email, str) or email.isspace() or email == "" or email.count('@') != 1:
            msg = 'Invalid email syntax.'
            return (False, msg)
        front, dom =  email.split('@')
        dom = f'@{dom}'
        if len(front) < 5 and '.' not in dom or dom.index('.') in (len(dom), 1):
            msg = 'Invalid email syntax'
            return (False, msg)
        if not isinstance(password, str) or len(password) < 5:
            msg = 'The password must contain at least 5 characters.'
            return (False, msg)
        
        ex = Users.exists(email)
        if ex is None:
            msg = 'An error occurred while trying to connect to the database.'
            return False
        if ex:
            msg = 'The email already exists.'
            return (False, msg)
        
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_str = password.decode('utf-8')
        conn = get_connection()
        if conn is None:
            msg = 'An error has occurred while trying to connect to the database.'
            return (False, msg)
        try:
            cursor = conn.cursor()
            qry = 'INSERT INTO users (name, email, password) VALUES (%s,%s,%s);'
            cursor.execute(qry, (name, email, password_str))
            conn.commit()
            msg = 'Account created, please check your email.'
            return (True, msg)
        except psycopg2.Error as e:
            print(f'Error: {e}')
            msg = 'An error has ocurred while creating the account.'
            return (False, msg)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_session_data(email: str) -> tuple:
        conn = get_connection()

        if conn is None:
            msg = 'An error has occurred while trying to connect to the database.'
            return (None, msg)
        try:
            cursor = conn.cursor()
            qry = 'SELECT user_id, name, verified FROM users WHERE email = %s'
            cursor.execute(qry, (email,))
            data = cursor.fetchone()
            return (True, data)
        except psycopg2.Error as e:
            print(f'Error: {e.pgerror}')
            msg = 'An error has ocurred while fetching the data.'
            return (False, msg)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_name(name: str):
        pass

class Log():
    @staticmethod
    def add_log(user_id: int, log: str , date: datetime):
        conn = get_connection()

        if conn is None:
            return None
        try:
            cursor = conn.cursor()

            qry = """
            INSERT INTO change_log (user_id, log, date)
            VALUES (%s, %s, %s);
            """
            cursor.execute(qry, (user_id, log, date))
            conn.commit()
            return True
        except psycopg2.Error as e:
            print(f'Error: {e.pgerror}')
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_logs():
        conn = get_connection()

        if conn is None:
            return None
        try:
            cursor = conn.cursor()

            qry = """
            SELECT change_log.user_id, name, log, date
            FROM change_log
            JOIN users ON users.user_id = change_log.user_id;
            """
            cursor.execute(qry)
            data = cursor.fetchall()
            return True, data
        except psycopg2.Error as e:
            print(f'Error: {e.pgerror}')
            msg = f'Error: {e.pgcode}'
            return False, msg
        finally:
            cursor.close()
            conn.close()

