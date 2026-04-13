import pymysql
from pymysql import connect
from pymysql.cursors import DictCursor


class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password='root',
            database='book_store',
            cursorclass=DictCursor
        )

    def cursor(self):
        return self.conn.cursor()

    def login(self, login, password):
        with self.cursor() as cur:
            cur.execute("select * from users where username = %s and password = %s", (login, password))
            return cur.fetchone()

    def get_all_books(self):
        with self.cursor() as cur:
            cur.execute("select * from books")
            return cur.fetchall()

    def get_all_authors(self):
        with self.cursor() as cur:
            cur.execute("select author from books")
            return cur.fetchall()

    def insert_book(self, book_name, price, author, image, discount):
        with self.cursor() as cur:
            print(image)
            cur.execute("insert into books(book_name, price, author, image, discount) "
                        "values (%s, %s, %s, %s, %s)" , (book_name, price, author, image, discount))
        self.conn.commit()


    def edit_book(self, book_id, book_name, price, author, image, discount):
        with self.cursor() as cur:
            cur.execute("update books set book_name = %s, price = %s, author = %s, image = %s, discount = %s where book_id = %s", (book_name, price, author, image, discount, book_id))
        self.conn.commit()


    def delete_book(self, book_id):
        with self.cursor() as cur:
            cur.execute("delete from books where book_id = %s", book_id)
        self.conn.commit()

    def search_books_by_author(self, author):
        with self.conn.cursor() as cur:
            cur.execute("select * from books where author = %s", author)
            return cur.fetchall()

    def create_order(self, books, user_id, total):
        with self.cursor() as cur:
            cur.execute(
                "INSERT INTO orders (user_id, total_sum, order_date, order_status) VALUES (%s, %s, NOW(), 'new')",
                (user_id, total)
            )
            order_id = cur.lastrowid

            for book in books:
                cur.execute(
                    "INSERT INTO order_items (order_id, book_id, quntity) VALUES (%s, %s, 1)",
                    (order_id, book["book_id"])
                )

        self.conn.commit()

    def get_all_orders(self):
        with self.cursor() as cur:
            cur.execute("""
                        SELECT o.order_id, u.username, o.total_sum, o.order_date, o.order_status
                        FROM orders o
                                 JOIN users u ON o.user_id = u.user_id
                        ORDER BY o.order_date DESC
                        """)
            return cur.fetchall()

    def update_order_status(self, order_id, status):
        with self.cursor() as cur:
            cur.execute("update orders set order_status = %s where order_id = %s", (status, order_id))
        self.conn.commit()

    def get_orders_by_user_id(self, user_id):
        with self.cursor() as cur:
            cur.execute("select order_id, total_sum, order_date, order_status from orders where user_id = %s", user_id)
            return cur.fetchall()

dao=Database()
