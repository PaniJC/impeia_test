### Books DB API ###
from fastapi import APIRouter, HTTPException
from db.models.books import Book
from db.client import db_client
from db.schemas.books import book_schema, books_schema 



router = APIRouter(prefix="/booksdb",
                   tags=["booksdb"],
                   responses={404:{"message":"Libro no encontrado"}})

books_list = []


@router.get("/", response_model=list[Book])
async def books():
    return books_schema(db_client.books.find())

@router.get("/title/{titulo}")
async def book(titulo:str):
    estado = search_book_by_title(titulo)
    return estado

@router.get("/author/{autor}")
async def book(autor:str):
    return books_schema(db_client.books.find({"autor_nombre":autor}))

@router.get("/countries/{country}")
async def book(country:str):
    return books_schema(db_client.books.find({"ubicacion_editorial":country}))


def search_book_by_title(titulo: str):
    try:
        resultado = db_client.books.find_one({"titulo":titulo})
        return Book(**book_schema(resultado))
    except:   
        return {"error":"No se ha encontrado el libro."} 

