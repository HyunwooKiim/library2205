from cache import redis_client
from data import con, cur

def get_borrowed_books_by_borrower(borrower: str):
    key = f"borrower:{borrower}:books"
    return list(redis_client.smembers(key))

def remove_borrowed_book_from_redis(borrower: str, title: str):
    key = f"borrower:{borrower}:books"
    # 1. DB에서 해당 도서의 book_id 찾기
    cur.execute(
        "SELECT b.book_id FROM borrowings b JOIN books bk ON b.book_id = bk.book_id WHERE b.borrower = ? AND bk.title = ? ORDER BY b.borrowed_at DESC LIMIT 1",
        (borrower, title)
    )
    row = cur.fetchone()
    if not row:
        return False

    book_id = row[0]
    try:
        # 2. books 테이블에서 available=1로 변경
        cur.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
        # 3. borrowings 테이블에서 해당 대출 기록 삭제
        cur.execute("DELETE FROM borrowings WHERE book_id = ? AND borrower = ?", (book_id, borrower))
        con.commit()
        # 4. Redis에서 도서 제목 삭제
        redis_client.srem(key, title)
        return True
    except Exception as e:
        print("반납 처리 오류:", e)
        con.rollback()
        return False