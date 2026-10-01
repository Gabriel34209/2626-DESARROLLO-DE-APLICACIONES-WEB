from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor
from conexion.conexion import obtener_conexion
from models import Usuario
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_123'

# --- CONFIGURACIÓN DE FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    usuario = None
    try:
        # Usa RealDictCursor para poder acceder por nombre de columna (ej: res['id'])
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
            res = cursor.fetchone()
            if res:
                # Soporta tanto 'usuario' como 'username'
                nombre_usuario = res.get('usuario') or res.get('username')
                usuario = Usuario(id=res['id'], usuario=nombre_usuario, password=res['password'])
    finally:
        conexion.close()
    return usuario

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


# --- MÓDULO AUTENTICACIÓN (LOGIN, REGISTRO, LOGOUT) ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = UsuarioForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO usuarios (usuario, username, password) VALUES (%s, %s, %s)',
                    (form.usuario.data, form.usuario.data, hashed_password)
                )
            conexion.commit()
            flash('Usuario registrado exitosamente. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conexion.rollback()
            flash('El nombre de usuario ya existe o ocurrió un error al registrar.', 'danger')
        finally:
            conexion.close()
            
    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        conexion = obtener_conexion()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM usuarios WHERE usuario = %s OR username = %s', (form.usuario.data, form.usuario.data))
                usuario_db = cursor.fetchone()
        finally:
            conexion.close()

        if usuario_db and check_password_hash(usuario_db['password'], form.password.data):
            nombre_usuario = usuario_db.get('usuario') or usuario_db.get('username')
            user_obj = Usuario(id=usuario_db['id'], usuario=nombre_usuario, password=usuario_db['password'])
            login_user(user_obj)
            flash(f'¡Bienvenido/a, {user_obj.usuario}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))


# --- MÓDULO PRODUCTOS (CRUD CON POSTGRESQL Y JOIN - RUTAS PROTEGIDAS) ---

@app.route('/productos')
@login_required
def productos():
    conexion = obtener_conexion()
    try:
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('''
                SELECT p.id, p.nombre, p.precio, p.stock, c.nombre AS categoria
                FROM productos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                ORDER BY p.id ASC
            ''')
            productos_db = cursor.fetchall()
    finally:
        conexion.close()
    return render_template('productos.html', productos=productos_db)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO productos (nombre, precio, stock, categoria_id)
                    VALUES (%s, %s, %s, %s)
                ''', (form.nombre.data, form.precio.data, form.stock.data, 1))
            conexion.commit()
        finally:
            conexion.close()
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    form = ProductoForm()
    conexion = obtener_conexion()
    
    if request.method == 'GET':
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
                producto = cursor.fetchone()
        finally:
            conexion.close()
            
        if producto:
            form.nombre.data = producto['nombre']
            form.precio.data = producto['precio']
            form.stock.data = producto['stock']
    
    if form.validate_on_submit():
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute('''
                    UPDATE productos 
                    SET nombre = %s, precio = %s, stock = %s 
                    WHERE id = %s
                ''', (form.nombre.data, form.precio.data, form.stock.data, id))
            conexion.commit()
        finally:
            conexion.close()
        return redirect(url_for('productos'))
        
    return render_template('formulario_producto.html', form=form, es_edicion=True)


@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
        conexion.commit()
    finally:
        conexion.close()
    return redirect(url_for('productos'))


# --- MÓDULO CLIENTES ---
@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html', clientes=clientes_lista)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
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
@login_required
def proveedores():
    return render_template('proveedores.html', proveedores=proveedores_lista)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
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
@login_required
def facturacion():
    return render_template('facturacion.html', facturas=facturas_lista)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
@login_required
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