"""FastAPI Bookstore REST API Application."""

import uvicorn
from fastapi import FastAPI, HTTPException, status
from bookstore.models import Book

app = FastAPI(
    title="Bookstore API", 
    description="Bookstore REST API", 
    version="1.0.0"
)

# In-memory storage
books_db = dict[int, Book] = {}

@app.get("/books", response_model=list[Book], status_code=status.HTTP_200_OK) 
def get_books(author: str | None = None) -> list[Book]: 
    """Obtiene todos los libros, con filtro opcional por autor (case-insensitive).""" 
    if author: 
        return [b for b in books_db.values() if b.author.lower() == author.lower()] 
    return list(books_db.values())
# 

@app.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int) -> Book:
    """Obtiene un libro específico por su ID. Retorna 404 Not Found si no existe."""
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    return books_db[book_id]


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: Book) -> Book:
    """Crea un nuevo registro de libro. Retorna 201 Created o 400/422 si hay errores."""
    if book.id in books_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ID {book.id} already exists",
        )
    books_db[book.id] = book
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int) -> None:
    """Elimina un libro por ID. Retorna 204 No Content en éxito o 404 Not Found."""
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    del books_db[book_id]


