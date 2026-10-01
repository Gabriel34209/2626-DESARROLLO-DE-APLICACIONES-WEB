import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        database="ferreteria",
        user="postgres",
        password="admin123",
        port="5432",
        client_encoding="utf8"
    )