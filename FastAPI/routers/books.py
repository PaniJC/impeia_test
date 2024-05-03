### Books API ###
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/books",
                   tags=["books"],
                   responses={404:{"message":"Libro no encontrado"}})

class User(BaseModel):
    id: int
    name:str
    surename:str
    url:str
    age:int

users_fake_mongo_db = [User(id = 1, name = "Juan Camilo",surename = "Paniagua Alvarez",url = "https://panijc.com/python",age = 42), User(id = 2, name = "Juan Sebastian",surename ="Paniagua Alvarez",url ="https://panijs.com/python",age =39), User(id = 3, name = "Jeronimo",surename ="Paniagua Naranjo",url ="https://panijero.com/python",age =13)]


@router.get("/")
async def users():
    return "Estoy en el router de los books"

@router.get("/{id}")
async def user(id:int, response_model=User,  status_code=200):
    users = filter(lambda user: user.id == id, users_fake_mongo_db)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404, detail="El libro NO existe")

# Iniciar el servidor: python -m uvicorn main:app --reload
# Server: http://127.0.0.1:8000 
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

# Entidad User
