from .conection import get_connection
import bcrypt
import psycopg2

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
    

def sign_in(email: str, password: str) -> bool:
    if not isinstance(email, str) or email.isspace() or email == "" or email.count('@') != 1:
        msg = 'Invalid email syntax.'
        return False, msg
    name, dom =  email.split('@')
    dom = f'@{dom}'
    if len(name) < 5 and '.' not in dom or dom.index('.') in (len(dom), 1):
        msg = 'Invalid email syntax'
        return False, msg
    if not isinstance(password, str) or len(password) < 5:
        msg = 'The password must contain at least 5 characters.'
        return False, msg

    ex = exists(email)
    if ex is None:
        msg = 'An error occurred while trying to connect to the database.'
        return False, msg
    if not ex:
        msg = 'The email is not registered.'
        return False, msg
    
    else:
        conn = get_connection()
        if conn is None:
            msg = 'An error occurred while trying to connect to the database.'
            return False, msg

        try: 
            cursor = conn.cursor()
            query = 'SELECT password FROM users WHERE email=%s'
            cursor.execute(query, (email,))
            data = cursor.fetchone()
        except psycopg2.Error as e:
            print(f'Error: {e.pgerror}')
            msg = 'An error ocurred while validating the data.'
            return False, msg
        finally:
            cursor.close()
            conn.close()

        hashed_password = data[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')): #checks if the password matches
            msg  = 'Success'
            return True, msg
        else: 
            msg = 'Incorrect password.'
            return False, msg
        
def register(name: str, email: str, password: str) -> bool:
    if not isinstance(name, str) or name.isdigit() or name.isspace() or name == "":
        msg = 'Invalid name'
        return False, msg
    if not isinstance(email, str) or email.isspace() or email == "" or email.count('@') != 1:
        msg = 'Invalid email syntax.'
        return False, msg
    front, dom =  email.split('@')
    dom = f'@{dom}'
    if len(front) < 5 and '.' not in dom or dom.index('.') in (len(dom), 1):
        msg = 'Invalid email syntax'
        return False, msg
    if not isinstance(password, str) or len(password) < 5:
        msg = 'The password must contain at least 5 characters.'
        return False, msg
    
    ex = exists(email)
    if ex is None:
        msg = 'An error occurred while trying to connect to the database.'
        return False
    if ex:
        msg = 'The email already exists.'
        return False, msg
    
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    password_str = password.decode('utf-8')
    conn = get_connection()
    if conn is None:
        msg = 'An error has occurred while trying to connect to the database.'
        return False
    try:
        cursor = conn.cursor()
        qry = 'INSERT INTO users (name, email, password) VALUES (%s,%s,%s);'
        cursor.execute(qry, (name, email, password_str))
        conn.commit()
        msg = 'Account created, please check your email.'
        return True, msg
    except psycopg2.Error as e:
        print(f'Error{e}')
        msg = 'An error has ocurred while creating the account.'
        return False, msg
    finally:
        cursor.close()
        conn.close()


def get_session_data(email: str):
    conn = get_connection()

    if conn is None:
        msg = 'An error has occurred while trying to connect to the database.'
        return None, msg
    try:
        cursor = conn.cursor()
        qry = 'SELECT user_id, name, verified FROM users WHERE email = %s'
        cursor.execute(qry, (email,))
        data = cursor.fetchone()
        return True, data
    except psycopg2.Error as e:
        print(f'Error: {e.pgerror}')
        msg = 'An error has ocurred while fetching the data.'
        return False, msg
    finally:
        cursor.close()
        conn.close()

def update_name(name: str):
    pass

def change_available(id_producto:int):
        conn = get_connection()

        if conn == None:
            pass
        else:
            cursor = conn.cursor()

            Ocultar = 'UPDATE product SET available = 1 WHERE product_id = %s;'

            cursor.execute(Ocultar, (id_producto,))

            conn.commit()
            cursor.close()
        conn.close()

