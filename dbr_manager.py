import json
import sqlite3



json_file_name = './data_with_coordinates.json'
# Datos del JSON

with open(json_file_name, "r", encoding="utf-8") as file:
    data = json.load(file)


# Base de datos relacional (SQLite)
conn_sqlite = sqlite3.connect('books.db')
c = conn_sqlite.cursor()

# Crear tabla
c.execute('''CREATE TABLE books
             (id INT PRIMARY KEY,
              titulo TEXT,
              autor_nombre TEXT,
              autor_nacionalidad TEXT,
              autor_fecha_nacimiento DATE,
              autor_genero TEXT,
              nombre_editorial TEXT,
              ubicacion_editorial TEXT,
              isbn TEXT,
              precio DECIMAL,
              cantidad_stock INT,
              coordenadas_editorial TEXT)''')

# Insertar datos
for book in data:
    c.execute('''INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (book['id'], book['titulo'], book['autor_nombre'], book['autor_nacionalidad'],
               book['autor_fecha_nacimiento'], book['autor_genero'], book['nombre_editorial'],
               book['ubicacion_editorial'], book['isbn'], book['precio'], book['cantidad_stock'], json.dumps(book['coordenadas_editorial'])))

conn_sqlite.commit()
conn_sqlite.close()

