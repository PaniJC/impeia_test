# Importamos FastAPI
from fastapi import FastAPI
from routers import basic_auth, books_db


app = FastAPI()

# Routers
app.include_router(basic_auth.router)
app.include_router(books_db.router)




