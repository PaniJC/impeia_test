from pydantic import BaseModel

class Book(BaseModel):
    _id: str | None
    titulo:str
    autor_nombre:str
    autor_nacionalidad:str
    autor_fecha_nacimiento:str
    autor_genero:str
    nombre_editorial:str
    ubicacion_editorial:str
    precio:int
    cantidad_stock:int