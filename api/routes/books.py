from fastapi import APIRouter, HTTPException, status

from typing import OrderedDict

from pydantic import BaseModel
from fastapi.responses import JSONResponse

from api.db.schemas import Book, Genre, InMemoryDB

from pydantic import BaseModel

router = APIRouter()

class Book(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int
    genre: str

books = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "publication_year": 1937, "genre": "Fantasy"},
    {"id": 2, "title": "1984", "author": "George Orwell", "publication_year": 1949, "genre": "Dystopian"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "publication_year": 1960, "genre": "Fiction"},
]


router = APIRouter()

db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )

@router.get("/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/")
def get_all_books():
    return books  # Return all books



@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db.update_book(book_id, book).model_dump(),
    )


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int):
    global books
    books = [book for book in books if book["id"] != book_id]
    return {"message": "Book deleted successfully"}  

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if book_id in db.books:
        del db.books[book_id]  # Properly delete from InMemoryDB
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Book not found")
