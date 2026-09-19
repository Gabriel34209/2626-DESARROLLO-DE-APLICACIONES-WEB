from flask import Flask, render_template

# Inicialización de la aplicación Flask
app = Flask(__name__)

# 1. Ruta principal (Página informativa de Coca-Cola)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Ruta para el módulo de Productos
@app.route('/productos')
def productos():
    # Datos de ejemplo para representar la lista de productos
    lista_productos = [
        {'id': 1, 'nombre': 'Coca-Cola Original 300ml', 'precio': 0.50, 'categoria': 'Bebidas Gaseosas'},
        {'id': 2, 'nombre': 'Coca-Cola Sin Azúcar 1.25L', 'precio': 1.25, 'categoria': 'Bebidas Sin Azúcar'},
        {'id': 3, 'nombre': 'Coca-Cola Light 500ml', 'precio': 0.80, 'categoria': 'Bebidas Bajas en Calorías'}
    ]
    return render_template('productos.html', productos=lista_productos)

# 3. Ruta para el módulo de Clientes
@app.route('/clientes')
def clientes():
    # Datos de ejemplo para clientes/distribuidores
    lista_clientes = [
        {'id': 1, 'nombre': 'Tienda El Rosario', 'contacto': 'María López', 'ciudad': 'Quito'},
        {'id': 2, 'nombre': 'Supermercado Central', 'contacto': 'Carlos Gómez', 'ciudad': 'Guayaquil'}
    ]
    return render_template('clientes.html', clientes=lista_clientes)

# 4. Ruta para el módulo de Proveedores
@app.route('/proveedores')
def proveedores():
    # Datos de ejemplo para proveedores
    lista_proveedores = [
        {'id': 1, 'empresa': 'Embotelladora Nacional', 'telefono': '022345678', 'insumo': 'Envases PET'},
        {'id': 2, 'empresa': 'Distribuidora de Azúcar S.A.', 'telefono': '042987654', 'insumo': 'Materia Prima'}
    ]
    return render_template('proveedores.html', proveedores=lista_proveedores)

# 5. Ruta para el módulo de Facturación
@app.route('/facturacion')
def facturacion():
    # Datos de ejemplo para facturación
    lista_facturas = [
        {'factura_no': 'F001-00102', 'cliente': 'Tienda El Rosario', 'fecha': '2026-09-18', 'total': 45.00},
        {'factura_no': 'F001-00103', 'cliente': 'Supermercado Central', 'fecha': '2026-09-18', 'total': 180.50}
    ]
    return render_template('facturacion.html', facturas=lista_facturas)

# Ejecución del servidor local en modo depuración
if __name__ == '__main__':
    app.run(debug=True)
