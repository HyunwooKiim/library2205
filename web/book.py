# web/borrowings.py
from fastapi import APIRouter, HTTPException
from service.book import insert_book, list_available_books, remove_book

router = APIRouter()

@router.post("/books")
def add_book(title: str, author: str):
    ok = insert_book(title, author)
    if not ok:
        raise HTTPException(status_code=400, detail="도서 등록 실패")
    return ok

@router.get("/books")
def get_books():
    return list_available_books()

@router.delete("/books/{book_id}")
def delete_book_api(book_id: int):
    ok = remove_book(book_id)
    if not ok:
        raise HTTPException(status_code=400, detail="삭제 실패(대출 불가 상태이거나 존재하지 않는 도서)")
    return ok