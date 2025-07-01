from fastapi import APIRouter, HTTPException
from service.borrowers import get_borrower_books_service, remove_borrowed_book_service

router = APIRouter()

@router.get("/borrowers/{borrower}/books")
def get_borrower_books(borrower: str):
    books = get_borrower_books_service(borrower)
    return {"borrower": borrower, "books": books}

@router.post("/return")
def return_book(borrower: str, title: str):
    ok = remove_borrowed_book_service(borrower, title)
    if not ok:
        raise HTTPException(status_code=400, detail="반납 실패(해당 도서 없음)")
    return ok