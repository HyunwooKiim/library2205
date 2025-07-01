from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service import borrowings as service
from service.borrowings import borrow_book_service, list_borrowings_by_month, return_book_service

router = APIRouter(prefix="/borrows")

@router.get("")
def test():
    return service.test()

@router.post("")
def borrow_book_api(borrower: str, title: str):
    ok = borrow_book_service(borrower, title)
    if not ok:
        raise HTTPException(status_code=400, detail="대출 실패(대출 불가 도서)")
    return ok

@router.get("/month/{borrow_month}")
def get_borrowings_by_month_api(borrow_month: str):
    """
    borrow_month: 'YYYY-MM' 형식 (예: '2024-07')
    """
    result = list_borrowings_by_month(borrow_month)
    return result
