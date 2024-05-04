from pymongo import MongoClient

# Base de datos local
db_client = MongoClient().books_db

## Base de datos remota
#db_client = MongoClient('mongodb+srv://admin:admin@cluster0.wjdbbxg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0').books_db
