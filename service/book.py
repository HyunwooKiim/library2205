from data import book as data
from data.book import get_available_books, delete_book

def insert_book(title: str, author: str) -> bool:
    return data.insert_book(title, author)

def list_available_books():
    return get_available_books()

def remove_book(book_id: int):
    return delete_book(book_id)