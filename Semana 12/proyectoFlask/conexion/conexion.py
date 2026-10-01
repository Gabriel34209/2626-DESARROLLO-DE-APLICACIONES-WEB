import os
import psycopg2

def obtener_conexion():
    # Intenta leer DATABASE_URL si existe en Render; si no, usa el host por defecto
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        return psycopg2.connect(database_url)
    else:
        return psycopg2.connect(
            host=os.environ.get('DB_HOST', 'dpg-daurfmo473hc73cbkil0-a.oregon-postgres.render.com'),
            database=os.environ.get('DB_NAME', 'ferreteria_q3gn'),
            user=os.environ.get('DB_USER', 'admin_cocacola'),
            password=os.environ.get('DB_PASSWORD', 'KD9a2j4KCL6929tzCAehbXMMbb3O1CsR'),
            port=os.environ.get('DB_PORT', '5432')
        )