# Importamos FastAPI
from fastapi import FastAPI
from routers import books,authors


app = FastAPI()

# Routers
app.include_router(books.router)
app.include_router(authors.router)



