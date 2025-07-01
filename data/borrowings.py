import pymysql
import datetime

from data import con, cur
from cache import redis_client

def test():
    return "sqlite connect ok"

def borrow_book(borrower: str, title: str):
    # 1. 대출 가능한 도서(book_id) 찾기 (available=1인 경우만)
    cur.execute("SELECT book_id FROM books WHERE title = ? AND available = 1", (title,))
    row = cur.fetchone()
    if not row:
        return False  # 대출 가능한 도서 없음

    book_id = row[0]
    borrow_date = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        # 2. borrowings 테이블에 기록 추가
        cur.execute(
            "INSERT INTO borrowings (book_id, borrower, borrowed_at) VALUES (?, ?, ?)",
            (book_id, borrower, borrow_date)
        )
        # 3. books 테이블에서 해당 도서 대출 불가 처리
        cur.execute(
            "UPDATE books SET available = 0 WHERE book_id = ?",
            (book_id,)
        )
        con.commit()
        save_borrowed_book_to_redis(borrower, title)  # 대출 성공 시 Redis에 저장
        return True
    except Exception as e:
        print("대출 처리 오류:", e)
        con.rollback()
        return False

def save_borrowed_book_to_redis(borrower: str, title: str):
    key = f"borrower:{borrower}:books"
    redis_client.sadd(key, title)

def get_borrowings_by_month(borrow_month: str):
    """
    borrow_month: 'YYYY-MM' 형식 (예: '2024-07')
    """
    sql = """
        SELECT b.borrower, bk.title, bk.author
        FROM borrowings b
        JOIN books bk ON b.book_id = bk.book_id
        WHERE strftime('%Y-%m', b.borrowed_at) = ?
    """
    cur.execute(sql, (borrow_month,))
    rows = cur.fetchall()
    return [
        {"borrower": row[0], "title": row[1], "author": row[2]}
        for row in rows
    ]

def return_book(borrower: str, title: str):
    # 1. 해당 도서의 book_id 찾기 (대출자와 제목으로)
    cur.execute(
        "SELECT b.book_id FROM borrowings b JOIN books bk ON b.book_id = bk.book_id WHERE b.borrower = ? AND bk.title = ? ORDER BY b.borrowed_at DESC LIMIT 1",
        (borrower, title)
    )
    row = cur.fetchone()
    if not row:
        return False  # 해당 대출 기록 없음

    book_id = row[0]
    try:
        # 2. books 테이블에서 available=1로 변경
        cur.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
        con.commit()
        # 3. Redis에서 도서 제목 삭제
        from data.borrowers import remove_borrowed_book_from_redis
        remove_borrowed_book_from_redis(borrower, title)
        return True
    except Exception as e:
        print("반납 처리 오류:", e)
        con.rollback()
        return False

