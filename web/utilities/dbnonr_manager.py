import json
from pymongo import MongoClient
from datetime import datetime

json_file_name = './data_with_coordinates.json'
# Datos del JSON

with open(json_file_name, "r", encoding="utf-8") as file:
    data = json.load(file)

for book in data:
    birth_date = datetime.strptime(book['autor_fecha_nacimiento'], '%Y-%m-%d')
    book['autor_fecha_nacimiento'] = birth_date    

# Base de datos NoSQL (MongoDB)
client = MongoClient('mongodb+srv://admin:admin@cluster0.wjdbbxg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client['books_db']
collection = db['books']

# Insertar datos
collection.insert_many(data)

client.close()