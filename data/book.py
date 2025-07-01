from data import con, cur

def insert_book(title: str, author: str):
    sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
    try:
        cur.execute(sql, (title, author))
        con.commit()
        return True
    except Exception:
        con.rollback()
        return False

def get_available_books():
    sql = "SELECT title, author FROM books WHERE available = 1"
    cur.execute(sql)
    rows = cur.fetchall()
    books = [{"title": row[0], "author": row[1]} for row in rows]
    print("대출 가능 도서 목록:", books)  # 로그 출력
    return books

def delete_book(book_id: int):
    sql = "DELETE FROM books WHERE book_id = ? AND available = 1"
    try:
        cur.execute(sql, (book_id,))
        print("삭제 시도:", book_id, "삭제된 행:", cur.rowcount)
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("도서 삭제 오류:", e)
        con.rollback()
        return False