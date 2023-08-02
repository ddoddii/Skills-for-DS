from fastapi import FastAPI , Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title = "API Practice 2",
    version = "1.0"
)

class Book:
    id : int
    title : str 
    author : str
    description :str
    rating : float
    
    def __init__(self,id,title,author,description,rating):
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
    rating: float = Field(gt=0, lt=6)
    
    class Config:
        schema_extra = {
            'example': {
                'title' : 'A new book',
                'author' : 'Put in Author',
                'description' : 'New description of book',
                'rating' : 'Put in rating from 0~6',
            }
        }
        

BOOKS = [
    Book(1,"Mockingbird","Harper Lee","How to kill a mockingbird",4),
    Book(2,"MobyDick","Herman Melville","Book about whales",3),
    Book(3,"1984","George Owell","Book about distopia",4.5),
    Book(4,"Great Gatsby","Fitzgerald","Gatsby's life story",5),
    Book(5,"Harry Potter","J.K.Rolling","Harry going to Hogwarts",5),
    Book(6,"Frankenstien","Shelly","Zombie book",2)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

#Path 로 validate 하는 방법 : book_id 가 0 보다 크도록 함
#찾고자 하는 id 가 없을 때 404 에러 
@app.get("/books/{book_id}")
async def read_book(book_id : int =Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail = "Item not found")

@app.post("/create_book")
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.dict())
    #print(type(new_book))
    BOOKS.append(find_book_id(new_book))
    return BOOKS

# id 를 기존에 존재하는 것 + 1 로 하고 싶을 때 적용하는 함수
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.get("/books/")
async def read_book_by_rating(book_rating:float = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
    return BOOKS

@app.delete("/books/{book_id}")
async def delete_book(book_id:int = Path(gt=0)):
    books_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            books_changed = True
            break
    if not books_changed:
        raise HTTPException(status_code=404, detail = 'Item not found')
    return BOOKS