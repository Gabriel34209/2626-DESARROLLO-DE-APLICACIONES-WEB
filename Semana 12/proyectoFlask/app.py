from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# Clave secreta necesaria para la protección CSRF de Flask-WTF
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_123'

# --- Listas de datos en memoria ---
productos_lista = [
    {"nombre": "Coca-Cola Original 300ml", "precio": 0.50, "categoria": "Bebidas", "stock": 50},
    {"nombre": "Coca-Cola Sin Azúcar 1.25L", "precio": 1.25, "categoria": "Bebidas", "stock": 30},
    {"nombre": "Coca-Cola Sabor Original 2L", "precio": 2.00, "categoria": "Bebidas", "stock": 0},
    {"nombre": "Fanta Naranja 500ml", "precio": 0.75, "categoria": "Bebidas", "stock": 15}
]

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


# --- MÓDULO PRODUCTOS ---
@app.route('/productos')
def productos():
    return render_template('productos.html', productos=productos_lista)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_producto = {
            "nombre": form.nombre.data,
            "precio": form.precio.data,
            "categoria": form.categoria.data,
            "stock": form.stock.data
        }
        productos_lista.append(nuevo_producto)
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