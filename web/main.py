import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import requests
from forms.forms import LoginForm
import plotly.graph_objs as go

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['GOOGLE_MAPS_API_KEY'] = 'AIzaSyDNkH7VWTtOIJ2PGnFYxCBV018pG74rGeI'

posts = []
password_r = r'45s\7809n\\’78{\9'

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

def obtener_codigo_pais(nombre_pais=None):
    try:
        response = requests.get('https://flagcdn.com/es/codes.json')
        response.raise_for_status() 
        codigos_pais = response.json()

        if nombre_pais:
            for codigo, nombre in codigos_pais.items():
                if nombre.lower() == nombre_pais.lower():
                    return codigo
            return None  # Si no se encuentra el país
        else:
            return codigos_pais
    except Exception as e:
        print(f'Error al obtener los códigos de país: {e}')
        return None

### Filtro para moneda   ###
@app.template_filter('format_currency')
def format_currency(value):
    return "${:,.2f}".format(value)

### Ruta básica que nos debe redireccionar al template del login   ###
@app.route("/")
def index():
    return redirect("/login/")

### Definiciones para el template de Login y el acceso al Dashboard   ###
@app.route("/login/", methods=["GET", "POST"])
def show_login_form():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        if name == 'admin' and password == password_r:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('dashboard'))
    return render_template("login.html", form=form)


### Definiciones dashboard   ###
@app.route("/dashboard/")
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    rows = cur.fetchall()
    rows_with_country_code = []


    for row in rows:
        nombre_pais = row['ubicacion_editorial']
        codigo_pais = obtener_codigo_pais(nombre_pais)
        if codigo_pais:
            url_imagen = f"https://flagcdn.com/16x12/{codigo_pais.lower()}.png"
            print(f"URL de la imagen: {url_imagen}")
        else:
            print("País no encontrado.")

        row_data = dict(row)
        row_data['codigo_pais'] = url_imagen
        rows_with_country_code.append(row_data)

    ### Consulta para conocer la cantidad de libros por ubicación de la editorial   ###
    cur.execute('''SELECT ubicacion_editorial, SUM(cantidad_stock) AS total_libros, coordenadas_editorial 
        FROM books 
        GROUP BY ubicacion_editorial''')
    editoriales = cur.fetchall()

    ### Consulta para conocer el autor mas viejo   ###
    cur.execute('''SELECT autor_nombre, MIN(autor_fecha_nacimiento) AS fecha_nacimiento
        FROM books
        GROUP BY autor_nombre
        ORDER BY fecha_nacimiento ASC
        LIMIT 1''')
    autor_mayor_edad = cur.fetchone()

    ### Consulta para conocer el autor mas joven   ###
    cur.execute('''SELECT autor_nombre, MAX(autor_fecha_nacimiento) AS fecha_nacimiento
        FROM books
        GROUP BY autor_nombre
        ORDER BY fecha_nacimiento DESC
        LIMIT 1''')
    autor_menor_edad = cur.fetchone()

    ### Consulta los títulos y sus respectivas cantidades   ###
    cur.execute("SELECT titulo, cantidad_stock FROM books")
    resultados = cur.fetchall()

    ### Consulta los valores de: libro mas barato, mas costoso y el precio promedio de una obra literaria   ###
    cur.execute("""
        SELECT 
            AVG(precio) AS promedio_costo,
            MIN(precio) AS valor_minimo,
            MAX(precio) AS valor_maximo
        FROM 
            books
    """)
    valores_libros = cur.fetchone()

    ### Cerramos la conexión   ###
    conn.close()

    ### Procesamiento de los resultados para la gráfica   ###
    titulos = [row[0] for row in resultados]
    cantidades_stock = [row[1] for row in resultados]

    # Creación del gráfico   #
    figura = go.Figure(data=[go.Bar(x=titulos, y=cantidades_stock, text=cantidades_stock, textposition='auto')])

    # Personalización del gráfico   #
    figura.update_layout(
        title="Cantidad de Stock por Libro",
        xaxis_title="Libro",
        yaxis_title="Cantidad en Stock"
    )

     # Conversión a dict para manipularlo adecuadamente   #
    grafico_dict = figura.to_dict()

    ### Renderizado del template dashboard, con el envío de todas las variables con los valores obtenidos a través de las múltiples consultas   ###
    return render_template('dashboard.html', rows=rows_with_country_code, editoriales=editoriales, autor_mayor_edad = autor_mayor_edad, autor_menor_edad = autor_menor_edad, grafico_dict=grafico_dict, valores_libros=valores_libros)


if __name__ == '__main__':
    app.run(debug=True)
