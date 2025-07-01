# 도서 대출 관리 시스템
* 도서관에서 사용할 수 있는 도서 대출 관리 API 구현
* 참고사항
  * 아래 내용 충족하고 정상적으로 동작하도록 개발
    * all or nothing 개발 원칙이겠지만, 성적 부여를 위해 **한 만큼 점수 부여**
  * 채팅창 등을 사용하여 및 다른 학생들과 의견을 주고 받는 행위 적발시 **부정 행위 처리(0점)**
  * sql 쿼리 직접 사용(ORM 기능 사용시 감점)
  * web, service, data, cache 계층 나눠서 개발(막코딩시 감점)
  * 주어진 환경(fastapi, uvicorn, SQLite, redis과 같은 라이브러리 및 pycharm IDE 등)에서만 개발하기
  * 모두 구현하고, ***10:25 ~ 10:30 사이에 PR 날리기***
    * 정해진 시간 외에 PR시 감점
    * 깃허브 정책에 의해 PR 내역은 삭제되지 않으니 유의!!
  * 예외처리는 선택사항(구현시 기능별 추가 점수, 최대 100점을 초과할x 수 없음)

| 연번 | 기능                                                      | URL                                   | HTTP   | return                                    | TABLE(SQLite)     | KEY(Redis)                  |
|----|---------------------------------------------------------|---------------------------------------|--------|-------------------------------------------|-------------------|-----------------------------|
| 1  | 도서 제목(title), 도서 저자(author)를 받아 해당 도서를 등록한다.            | `/books`                              | post   | true / false                              | books             | -                           |
| 2  | 대출 가능한 도서 목록을 조회한다.                                     | `/books`                              | get    | `[{title:책제목, author:저자}]`                | books             | -                           |
| 3  | 도서 아이디(book_id)를 받아 대출 가능한 상태라면 해당 도서를 삭제한다.            | `/books/{book_id}`                    | delete | true / false                              | books             | -                           |
| 4  | 대출자 이름(borrower), 도서 제목(title)을 받아 해당 도서를 대출 처리한다.      | `/borrows`                            | post   | true / false                              | books, borrowings | -                           |
| 5  | 대출자의 대출한 도서 제목을 저장한다.                                | `/borrows`                            | =      | =                                         | -                 | `borrower:{borrower}:books` |
| 6  | 대출이 있었던 월(borrow_month)을 받아 해당 월에 대출이 있었던 책들의 목록을 조회한다. | `/borrows/month`<br>`/{borrow_month}` | get    | `[{borrower: 대출자, title:책제목, author:저자]`  | borrowings        | -                           |
| 7  | 대출자 이름(borrower)을 받아 해당 대출자의 기록을 조회한다.                  | `/borrowers`<br>`/{borrower}/books`   | get    | `{borrower:대출자, books:[책제목1, 책제목2 ...] }` | -                 | `borrower:{borrower}:books`                |
| 8  | 대출자 이름(borrower), 도서 제목(title)을 받아 해당 도서를 반납 처리한다.      | `/return`                             | post   | true/false                                | book, borrowings |  - |
| 9  | 대출자의 대출한 도서 제목을 삭제한다.                                   | `/return`                             | =      | =                                         | -                 | `borrower:{borrower}:books`                |
         

# 환경세팅 및 제출 방법
1. PyCharm 으로 진행
2. 본 레파지토리 fork 후 clone
3. 메뉴 → 설정 → 프로젝트 → 파이썬 인터프리터 → 인터프리터 추가 → 로컬 인터프리터 → 버전 3.12 추가
4. (좌측 하단 터미널 클릭 후) pip install -r requirements.txt
5. 개발 후 commit → github push
6. 깃헙 사이트의 레파지토리 들어가서 Pull Request 버튼 클릭
7. 제목에 ***학번 이름*** (제일 중요!!)

