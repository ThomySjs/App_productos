import psycopg2
import os

query = """ 
        CREATE TABLE usuario (
            id_usuario SERIAL PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE NOT NULL,
            correo VARCHAR(255) UNIQUE NOT NULL,
            contrasenia VARCHAR(50) NOT NULL
        );

        CREATE TABLE producto (
            id_producto SERIAL PRIMARY KEY,
            nombre_producto VARCHAR(50) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            descripcion VARCHAR(300) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            disponible BOOLEAN NOT NULL DEFAULT FALSE
        );
"""

try:
    con = psycopg2.connect(os.getenv("DATABASE_URL"))
except psycopg2.Error as err:
    print(f'Error: {err}')

cursor = con.cursor()
cursor.execute("")
resultado = cursor.fetchall()
con.close()

print(resultado)