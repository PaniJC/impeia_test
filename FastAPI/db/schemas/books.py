def book_schema(book) -> dict:
    return {"_id":str(book["_id"]),
        "titulo": book["titulo"],
        "autor_nombre":book["autor_nombre"],
        "autor_nacionalidad":book["autor_nacionalidad"],
        "autor_fecha_nacimiento":str(book["autor_fecha_nacimiento"])[:10],
        "autor_genero":book["autor_genero"],
        "nombre_editorial":book["nombre_editorial"],
        "ubicacion_editorial":book["ubicacion_editorial"],
        "precio":int(book["precio"]),
        "cantidad_stock":int(book["cantidad_stock"])}


def books_schema(books) -> list:
    return [book_schema(book) for book in books]
