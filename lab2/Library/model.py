from psycopg2.extras import execute_values

class Model:
    def __init__(self, conn, conn_time):
        self.conn = conn
        self.conn_time = conn_time

    def read_member(self, name, surname):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM members WHERE name=(%s) AND surname=(%s);", (name, surname))
        member = cur.fetchall()
        return member

    def read_members(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM members;")
        members = cur.fetchall()
        return members

    def create_member(self, name, surname, phone, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO public.members(name, surname, phone_number, email) VALUES (%s, %s, %s, %s);", (name, surname, phone, email))

    def update_member(self, id, name, surname, phone, email):
        cur = self.conn.cursor()
        cur.execute("UPDATE public.members SET name=(%s), surname=(%s), phone_number=(%s), email=(%s)  WHERE id=(%s);", (name, surname, phone, email, id))

    def delete_member(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM abonnements WHERE member_id=(%s);", (id,))
        abonnement = cur.fetchall()
        if abonnement:
            return False
        else:
            cur.execute("DELETE FROM public.members WHERE id=(%s);", (id,))
            return True

    def read_author(self, name, surname):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM authors WHERE name=(%s) AND surname=(%s);", (name, surname))
        author = cur.fetchall()
        return author

    def read_authors(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM authors;")
        authors = cur.fetchall()
        return authors

    def create_author(self, name, surname):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO public.authors(name, surname) VALUES (%s, %s);", (name, surname))

    def update_author(self, id, name, surname):
        cur = self.conn.cursor()
        cur.execute("UPDATE public.authors SET name=(%s), surname=(%s) WHERE id=(%s);", (name, surname, id))

    def delete_author(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM authors_books WHERE author_id=(%s);", (id,))
        book = cur.fetchall()
        if book:
            return False
        else:
            cur.execute("DELETE FROM public.authors WHERE id=(%s);", (id,))
            return True

    def read_book(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM books WHERE name=(%s);", (name,))
        book = cur.fetchall()
        return book

    def read_books(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return books

    def create_book(self, name, isbn, year):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO public.books(name, isbn, year_of_publication) VALUES (%s, %s, %s);", (name, isbn, year))

    def update_book(self, id, name, isbn, year):
        cur = self.conn.cursor()
        cur.execute("UPDATE public.books SET name=(%s), isbn=(%s), year_of_publication=(%s) WHERE id=(%s);", (name, isbn, year, id))

    def delete_book(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM abonnements WHERE book_id=(%s);", (id,))
        abonnement = cur.fetchall()
        cur.execute("SELECT 1 FROM authors_books WHERE book_id=(%s);", (id,))
        author = cur.fetchall()
        if abonnement or author:
            return False
        else:
            cur.execute("DELETE FROM public.books WHERE id=(%s);", (id,))
            return True

    def read_abonnement(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM abonnements WHERE id=(%s);", (id,))
        abonnement = cur.fetchall()
        return abonnement

    def read_abonnements(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM abonnements;")
        abonnements = cur.fetchall()
        return abonnements

    def create_abonnement(self, member_id, book_id, date_of_issue, date_of_return, is_returned):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM members WHERE id=(%s);", (member_id,))
        member = cur.fetchall()
        cur.execute("SELECT 1 FROM books WHERE id=(%s);", (book_id,))
        book = cur.fetchall()
        if not member or not book:
            return False
        else:
            cur.execute("INSERT INTO public.abonnements(member_id, book_id, date_of_issue, date_of_return, is_returned) VALUES (%s, %s, %s, %s, %s);", (member_id, book_id, date_of_issue, date_of_return, is_returned))
            return True

    def update_abonnement(self, id, member_id, book_id, date_of_issue, date_of_return, is_returned):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM members WHERE id=(%s);", (member_id,))
        member = cur.fetchall()
        cur.execute("SELECT 1 FROM books WHERE id=(%s);", (book_id,))
        book = cur.fetchall()
        if not member or not book:
            return False
        else:
            cur.execute("UPDATE public.abonnements SET member_id=(%s), book_id=(%s), date_of_issue=(%s), date_of_return=(%s), is_returned=(%s) WHERE id=(%s);", (member_id, book_id, date_of_issue, date_of_return, is_returned, id))
            return True

    def delete_abonnement(self, id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM public.abonnements WHERE id=(%s);", (id,))

    def read_authors_books(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM authors_books;")
        authors_books = cur.fetchall()
        return authors_books

    def create_author_book(self, author_id, book_id):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM authors WHERE id=(%s);", (author_id,))
        author = cur.fetchall()
        cur.execute("SELECT 1 FROM books WHERE id=(%s);", (book_id,))
        book = cur.fetchall()
        if not author or not book:
            return False
        else:
            cur.execute("INSERT INTO public.authors_books(author_id, book_id) VALUES (%s, %s);", (author_id, book_id))
            return True

    def update_author_book(self, id, author_id, book_id):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM authors WHERE id=(%s);", (author_id,))
        author = cur.fetchall()
        cur.execute("SELECT 1 FROM books WHERE id=(%s);", (book_id,))
        book = cur.fetchall()
        if not author or not book:
            return False
        else:
            cur.execute("UPDATE public.authors_books SET author_id=(%s), book_id=(%s) WHERE id=(%s);", (author_id, book_id, id))
            return True

    def delete_author_book(self, id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM public.authors_books WHERE id=(%s);", (id,))


    def generate_members(self, quant):
        cur = self.conn.cursor()
        cur.execute("select chr(trunc(65+random()*25)::int) || chr(trunc(97+random()*25)::int) || chr(trunc(97+random()*25)::int), chr(trunc(65+random()*25)::int) || chr(trunc(97+random()*25)::int) || chr(trunc(97+random()*25)::int), trunc(random()*900+100)::varchar || '-' ||trunc(random()*900+100)::varchar || '-' ||trunc(random()*9000+1000)::varchar, chr(trunc(97+random()*25)::int) || chr(trunc(97+random()*25)::int) || '@' || chr(trunc(97+random()*25)::int) from generate_series(1,(%s));", (quant,))
        members = cur.fetchall()
        execute_values(cur, "INSERT INTO public.members(name, surname, phone_number, email) VALUES %s", members)

    def generate_authors(self, quant):
        cur = self.conn.cursor()
        cur.execute("select chr(trunc(65+random()*25)::int) || chr(trunc(97+random()*25)::int) || chr(trunc(97+random()*25)::int), chr(trunc(65+random()*25)::int) || chr(trunc(97+random()*25)::int) || chr(trunc(97+random()*25)::int) from generate_series(1,(%s));", (quant,))
        authors = cur.fetchall()
        execute_values(cur, "INSERT INTO public.authors(name, surname) VALUES %s", authors)

    def generate_books(self, quant):
        cur = self.conn.cursor()
        cur.execute("select chr(trunc(65+random()*25)::int) || chr(trunc(97+random()*25)::int) || chr(trunc(97+random()*25)::int), trunc(random()*9000000000+1000000000)::bigint, trunc(random()*120+1900)::int from generate_series(1,(%s));", (quant,))
        books = cur.fetchall()
        execute_values(cur, "INSERT INTO public.books(name, isbn, year_of_publication) VALUES %s", books)


    def read_debts_query(self, date, quant):
        cur = self.conn_time.cursor()
        cur.execute("WITH TmpTable AS\n(\nSELECT abonnements.member_id, COUNT(*) AS quantity FROM abonnements WHERE abonnements.is_returned = false GROUP BY abonnements.member_id\n)\nSELECT members.name, surname, email, phone_number, abonnements.id, books.name, date_of_issue, date_of_return, is_returned  FROM TmpTable JOIN members ON TmpTable.member_id = members.id JOIN abonnements ON TmpTable.member_id = abonnements.member_id JOIN books ON abonnements.book_id = books.id WHERE quantity>(%s) AND date_of_issue>=(%s)  AND is_returned=false;", (quant, date))
        debts = cur.fetchall()
        return debts

    def read_member_query(self, name, date1, date2):
        cur = self.conn_time.cursor()
        like_name='{}%'.format(name)
        cur.execute("SELECT members.name, surname, email, books.name, date_of_issue, date_of_return, is_returned  FROM abonnements JOIN members ON abonnements.member_id = members.id JOIN books ON abonnements.book_id = books.id WHERE members.name LIKE (%s) AND is_returned = true AND date_of_issue BETWEEN (%s) AND (%s);", (like_name, date1, date2))
        member = cur.fetchall()
        return member

    def read_popular_query(self, count, date1, date2, year):
        cur = self.conn_time.cursor()
        cur.execute("WITH TmpAbonn AS\n(\nSELECT * FROM abonnements WHERE abonnements.date_of_issue BETWEEN (%s) AND (%s)\n)\nSELECT DISTINCT TmpBooks.name, authors.name, authors.surname, TmpBooks.year_of_publication, TmpBooks.taken_count FROM\n(\nSELECT books.id, books.name, books.year_of_publication, COUNT(TmpAbonn.book_id) AS taken_count FROM books JOIN TmpAbonn ON books.id = TmpAbonn.book_id GROUP BY books.id HAVING COUNT(TmpAbonn.book_id)>(%s)\n) TmpBooks JOIN abonnements ON TmpBooks.id = abonnements.book_id JOIN authors_books ON TmpBooks.id = authors_books.book_id JOIN authors ON authors_books.author_id=authors.id WHERE TmpBooks.year_of_publication>(%s);", (date1, date2, count, year))
        popular = cur.fetchall()
        return popular
