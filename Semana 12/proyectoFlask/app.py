import os
import sqlite3
from flask import Flask, render_template, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_123'

# --- CONFIGURACIÓN DE BASE DE DATOS SQLITE ---
DATA_DIR = os.path.join(app.root_path, 'data')
DB_PATH = os.path.join(DATA_DIR, 'ferreteria.db')

def get_db_connection():
    """Establece conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre como diccionario
    return conn

def init_db():
    """Crea la estructura de la base de datos si no existe."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crear tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    
    # Insertar datos de prueba iniciales si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO productos (nombre, precio, categoria, stock)
            VALUES (?, ?, ?, ?)
        ''', [
            ("Coca-Cola Original 300ml", 0.50, "Bebidas", 50),
            ("Coca-Cola Sin Azúcar 1.25L", 1.25, "Bebidas", 30),
            ("Coca-Cola Sabor Original 2L", 2.00, "Bebidas", 0),
            ("Fanta Naranja 500ml", 0.75, "Bebidas", 15)
        ])
    
    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar
init_db()


# --- DATOS EN MEMORIA (Para otros módulos) ---
clientes_lista = [
    {"nombre": "Tienda El Roble", "contacto": "Carlos Mendoza", "ciudad": "Puyo"},
    {"nombre": "Supermercado Central", "contacto": "María López", "ciudad": "Tena"},
    {"nombre": "Distribuidora Amazonía", "contacto": "Juan Pérez", "ciudad": "Macas"}
]

proveedores_lista = [
    {"empresa": "Embotelladora del Mando S.A.", "telefono": "022345678", "insumo": "Envases PET y Latas"},
    {"empresa": "Azucarera Valdez", "telefono": "042889900", "insumo": "Materia Prima (Endulzantes)"},
    {"empresa": "Transportes del Oriente", "telefono": "0991234567", "insumo": "Logística y Distribución"}
]

facturas_lista = [
    {"factura_no": "001-001-00123", "cliente": "Tienda El Roble", "fecha": "2026-09-20", "total": 150.00},
    {"factura_no": "001-001-00124", "cliente": "Supermercado Central", "fecha": "2026-09-21", "total": 320.50},
    {"factura_no": "001-001-00125", "cliente": "Distribuidora Amazonía", "fecha": "2026-09-22", "total": 85.00}
]


@app.route('/')
def index():
    return render_template('index.html')


# --- MÓDULO PRODUCTOS (CON SQLITE REAL) ---
@app.route('/productos')
def productos():
    conn = get_db_connection()
    productos_db = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos_db)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO productos (nombre, precio, categoria, stock)
            VALUES (?, ?, ?, ?)
        ''', (form.nombre.data, form.precio.data, form.categoria.data, form.stock.data))
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)


# --- MÓDULO CLIENTES ---
@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=clientes_lista)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def formulario_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = {
            "nombre": form.nombre.data,
            "contacto": form.contacto.data,
            "ciudad": form.ciudad.data
        }
        clientes_lista.append(nuevo_cliente)
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)


# --- MÓDULO PROVEEDORES ---
@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=proveedores_lista)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def formulario_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_proveedor = {
            "empresa": form.empresa.data,
            "telefono": form.telefono.data,
            "insumo": form.insumo.data
        }
        proveedores_lista.append(nuevo_proveedor)
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form)


# --- MÓDULO FACTURACIÓN ---
@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=facturas_lista)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def formulario_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        nueva_factura = {
            "factura_no": form.factura_no.data,
            "cliente": form.cliente.data,
            "fecha": form.fecha.data,
            "total": form.total.data
        }
        facturas_lista.append(nueva_factura)
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)