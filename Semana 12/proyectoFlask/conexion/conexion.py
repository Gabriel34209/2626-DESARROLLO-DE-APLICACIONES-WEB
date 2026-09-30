import pymysql

def obtener_conexion():
    """Establece y retorna la conexión a la base de datos MySQL en XAMPP."""
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Por defecto en XAMPP está vacío
        database='ferreteria',
        cursorclass=pymysql.cursors.DictCursor
    )