from data.borrowers import get_borrowed_books_by_borrower, remove_borrowed_book_from_redis

def get_borrower_books_service(borrower: str):
    return get_borrowed_books_by_borrower(borrower)

def remove_borrowed_book_service(borrower: str, title: str):
    return remove_borrowed_book_from_redis(borrower, title)