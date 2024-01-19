from typing import Optional
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    
    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
    
class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1) 
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithalex',
                'description': 'A new description of a book',
                'rating': 5                
            }
        }
            



BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithalex', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithalex', 'A great book!', 5),
    Book(3, 'Computer Science Pro', 'codingwithalex', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get('/book/', status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int):
    books_to_rating = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_rating.append(book)
    return books_to_rating


@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def read_books(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")
    




@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_ad(new_book))



def find_book_ad(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1
    return book
        


@app.put('/book/update_book')
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not founde')


@app.delete('/books/{book_id}')
async def delete_book(book_id: int):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not founde')   










