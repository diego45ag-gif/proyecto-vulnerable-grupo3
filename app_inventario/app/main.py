from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Categorías predefinidas según la guía técnica
CATEGORIAS = [
    "Electrónica", "Ropa", "Alimentos", "Hogar",
    "Deportes", "Libros", "Juguetes", "Otro"
]

# Almacenamiento en memoria (Fase 1)
productos = []
contador_id = 1

# --- FUNCIONES AUXILIARES ---
def buscar_producto(producto_id):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None

def filtrar_productos(nombre_query, categoria_filtro):
    resultados = productos
    # Filtrar por nombre
    if nombre_query:
        resultados = [p for p in resultados if nombre_query.lower() in p['nombre'].lower()]
    # Filtrar por categoría
    if categoria_filtro and categoria_filtro != "Todas":
        resultados = [p for p in resultados if p['categoria'] == categoria_filtro]
    return resultados

def calcular_estadisticas():
    total_productos = len(productos)
    valor_total = sum(p['precio'] * p['stock'] for p in productos)
    productos_sin_stock = len([p for p in productos if p['stock'] == 0])
    productos_stock_bajo = len([p for p in productos if p['stock'] < p['stock_minimo']])
    
    return {
        "total": total_productos,
        "valor_total": valor_total,
        "sin_stock": productos_sin_stock,
        "stock_bajo": productos_stock_bajo
    }

# --- RUTAS DE LA APLICACIÓN ---

@app.route("/")
def index():
    # Mostrar todos los productos
    stats = calcular_estadisticas()
    return render_template("index.html", productos=productos, categorias=CATEGORIAS, stats=stats)

@app.route("/buscar")
def buscar():
    # Buscar con query params
    query = request.args.get("nombre", "").strip()
    categoria = request.args.get("categoria", "Todas")
    
    # Filtrar productos
    resultados = filtrar_productos(query, categoria)
    stats = calcular_estadisticas()
    
    return render_template("index.html", productos=resultados, categorias=CATEGORIAS, query=query, categoria=categoria, stats=stats)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        global contador_id
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "Otro")
        precio = request.form.get("precio", "0")
        stock = request.form.get("stock", "0")
        stock_minimo = request.form.get("stock_minimo", "5")

        # Validaciones de entrada
        errores = []
        if not nombre or len(nombre) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres")
            
        try:
            precio = float(precio)
            if precio < 0:
                errores.append("El precio no puede ser negativo")
        except ValueError:
            errores.append("Precio inválido")
            
        try:
            stock = int(stock)
            if stock < 0:
                errores.append("El stock no puede ser negativo")
        except ValueError:
            errores.append("Stock inválido")
            
        try:
            stock_minimo = int(stock_minimo)
            if stock_minimo < 0:
                errores.append("El stock mínimo no puede ser negativo")
        except ValueError:
            errores.append("Stock mínimo inválido")

        if errores:
            return render_template("agregar.html", categorias=CATEGORIAS, errores=errores)

        # Crear producto e insertar en la lista
        productos.append({
            "id": contador_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "categoria": categoria,
            "precio": precio,
            "stock": stock,
            "stock_minimo": stock_minimo,
            "fecha_agregado": datetime.now().strftime("%d/%m/%Y"),
            "activo": True
        })
        contador_id += 1
        return redirect(url_for('index'))

    return render_template("agregar.html", categorias=CATEGORIAS)

@app.route("/editar/<int:producto_id>", methods=["GET", "POST"])
def editar(producto_id):
    producto = buscar_producto(producto_id)
    if not producto:
        return redirect(url_for('index'))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "Otro")
        precio = request.form.get("precio", "0")
        stock = request.form.get("stock", "0")
        stock_minimo = request.form.get("stock_minimo", "5")

        try:
            if nombre and len(nombre) >= 3:
                producto["nombre"] = nombre
            producto["descripcion"] = descripcion
            producto["categoria"] = categoria
            
            precio = float(precio)
            if precio >= 0:
                producto["precio"] = precio
                
            stock = int(stock)
            if stock >= 0:
                producto["stock"] = stock
                
            stock_minimo = int(stock_minimo)
            if stock_minimo >= 0:
                producto["stock_minimo"] = stock_minimo
        except ValueError:
            pass # Mantener valores anteriores si hay un error de conversión

        return redirect(url_for('index'))

    return render_template("editar.html", producto=producto, categorias=CATEGORIAS)

@app.route("/eliminar/<int:producto_id>", methods=["POST"])
def eliminar(producto_id):
    producto = buscar_producto(producto_id)
    if producto:
        productos.remove(producto)
    return redirect(url_for('index'))


# --- VULNERABILIDADES INYECTADAS INTENCIONALMENTE ---

# 1. Llave privada expuesta (Detectado por GitHub Secret Scanning)
CLAVE_PRIVADA = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAuz6M2bJc/jN8Vq4b1...
Hk2J9aL0xO+p3f5K7B9sM1rT4vW8xY2...
-----END RSA PRIVATE KEY-----
"""

# 2. Puerta trasera de ejecución de comandos (Detectado por Bandit y CodeQL)
@app.route("/admin/debug")
def debug_cmd():
    # PELIGRO: La función eval() ejecuta código arbitrario
    comando = request.args.get("cmd", "1+1")
    resultado = eval(comando)
    return f"Resultado de depuración: {resultado}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
