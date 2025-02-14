from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api.db.schemas import Book, Genre, InMemoryDB  

router = APIRouter()


db = InMemoryDB()


db.books = {
    1: Book(id=1, title="The Hobbit", author="J.R.R. Tolkien", publication_year=1937, genre=Genre.FANTASY),
    2: Book(id=2, title="1984", author="George Orwell", publication_year=1949, genre=Genre.DYSTOPIAN),
    3: Book(id=3, title="To Kill a Mockingbird", author="Harper Lee", publication_year=1960, genre=Genre.FICTION),
}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    if book.id in db.books:
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    db.add_book(book)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=book.model_dump())


@router.get("/{book_id}")
async def get_book(book_id: int):
    book = db.books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/")
async def get_all_books():
    return list(db.books.values())


@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book):
    if book_id not in db.books:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = db.update_book(book_id, book)
    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_book.model_dump())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    if book_id not in db.books:
        raise HTTPException(status_code=404, detail="Book not found")
    del db.books[book_id]  
    return Response(status_code=status.HTTP_204_NO_CONTENT)
