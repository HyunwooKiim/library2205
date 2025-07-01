from data import borrowings as data
from cache import borrower as cache
from data.borrowings import borrow_book, get_borrowings_by_month, return_book


def test():
    db_test = data.test()
    redis_test = cache.test()
    return {"sqlite": db_test, "redis": redis_test}


def borrow_book_service(borrower: str, title: str):
    return borrow_book(borrower, title)


def list_borrowings_by_month(borrow_month: str):
    return get_borrowings_by_month(borrow_month)


def return_book_service(borrower: str, title: str):
    return return_book(borrower, title)

