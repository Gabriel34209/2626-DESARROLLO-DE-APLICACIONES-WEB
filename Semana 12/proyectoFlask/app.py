from flask import Flask, render_template, redirect, url_for, flash, request
from conexion.conexion import obtener_conexion
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_123'

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


# --- MÓDULO PRODUCTOS (CRUD CON MYSQL) ---

# 1. LISTAR (SELECT)
@app.route('/productos')
def productos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT * FROM productos')
        productos_db = cursor.fetchall()
    conexion.close()
    return render_template('productos.html', productos=productos_db)

# 2. AGREGAR (INSERT)
@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('''
                INSERT INTO productos (nombre, precio, categoria, stock, categoria_id)
                VALUES (%s, %s, %s, %s, 1)
            ''', (form.nombre.data, form.precio.data, form.categoria.data, form.stock.data))
        conexion.commit()
        conexion.close()
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)

# 3. MODIFICAR (UPDATE)
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    form = ProductoForm()
    conexion = obtener_conexion()
    
    if request.method == 'GET':
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
            producto = cursor.fetchone()
        conexion.close()
        
        if producto:
            form.nombre.data = producto['nombre']
            form.precio.data = producto['precio']
            form.categoria.data = producto['categoria']
            form.stock.data = producto['stock']
    
    if form.validate_on_submit():
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE productos 
                SET nombre = %s, precio = %s, categoria = %s, stock = %s 
                WHERE id = %s
            ''', (form.nombre.data, form.precio.data, form.categoria.data, form.stock.data, id))
        conexion.commit()
        conexion.close()
        return redirect(url_for('productos'))
        
    return render_template('formulario_producto.html', form=form, es_edicion=True)

# 4. ELIMINAR (DELETE)
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('productos'))


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