from fastapi import FastAPI, Body
import logging


logger = logging.getLogger(name='MyLog')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('|%(asctime)s||%(name)s||%(levelname)s|\n%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )

stream_handler = logging.StreamHandler() 
stream_handler.setFormatter(formatter) 
logger.addHandler(stream_handler) 

app = FastAPI(title = "API Practice",
            version = "1.0")

BOOKS = [
    {'title': 'Mockingbird', 'author': 'Harper Lee', 'category': 'fiction'},
    {'title': 'MobyDick', 'author': 'Herman Melville', 'category': 'fiction'},
    {'title': '1984', 'author': 'George Owell', 'category': 'history'},
    {'title': 'Great Gatsby', 'author': 'Fitzgerald', 'category': 'fiction'},
    {'title': 'Frankenstien', 'author': 'Shelly', 'category': 'zombie'},
    {'title': 'HarryPotter', 'author': 'J.K.Rolling', 'category': 'fiction'}
]

@app.get('/')
async def first_api():
    return ("FastAPI 를 배워봅시다!")


@app.get('/api-endpoint')
async def first_api_endpoint():
    return ("내 api-endpoint !")

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get('/books/{book_title}')
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        else:
            return {'new_book': book_title}
        
@app.get('/books/{dynamic_param}')
async def test_dynamic_param(dynamic_param):
    return {'dynamic_param':dynamic_param}

@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return BOOKS

@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
    return BOOKS

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
    return BOOKS

