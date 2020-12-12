from author import Author
from author_book import Author_Book
from book import Book
from member import Member
from abonnement import Abonnement



class Model:
    def __init__(self, session):
        self.session = session

    def read_author(self, name, surname):
        author = self.session.query(Author).filter(Author.name == name, Author.surname == surname).first()
        return author

    def read_authors(self):
        authors = self.session.query(Author).all()
        return authors

    def create_author(self, name, surname):
        author = Author(name, surname)
        self.session.add(author)

    def update_author(self, id, name, surname):
        author = self.session.query(Author).get(id)
        author.name = name
        author.surname = surname

    def delete_author(self, id):
        is_used = self.session.query(self.session.query(Author_Book).filter(Author_Book.author_id == id).exists()).scalar()
        if is_used:
            return False
        else:
            self.session.query(Author).filter(Author.id == id).delete()
            return True

    def read_book(self, id):
        book = self.session.query(Book).get(id)
        return book

    def read_books(self):
        books = self.session.query(Book).all()
        return books

    def create_book(self, name, isbn, year):
        book = Book(name, isbn, year)
        self.session.add(book)

    def update_book(self, id, name, isbn, year):
        book = self.session.query(Book).get(id)
        book.name = name
        book.isbn = isbn
        book.year_of_publication = year

    def delete_book(self, id):
        is_used1 = self.session.query(self.session.query(Author_Book).filter(Author_Book.book_id == id).exists()).scalar()
        is_used2 = self.session.query(self.session.query(Abonnement).filter(Abonnement.book_id == id).exists()).scalar()
        if is_used1 or is_used2:
            return False
        else:
            self.session.query(Book).filter(Book.id == id).delete()
            return True

    def read_authors_books(self):
        authors_books = self.session.query(Author_Book).all()
        return authors_books

    def create_author_book(self, author_id, book_id):
        author = self.session.query(Author).get(author_id)
        book = self.session.query(Book).get(book_id)
        if not author or not book:
            return 1
        else:
            author_book_ex = self.session.query(Author_Book).get((author_id, book_id))
            if(author_book_ex):
                return 2
            else:
                author_book = Author_Book(author_id, book_id)
                author_book.author = author
                author_book.book = book
                author.books.append(author_book)
                book.authors.append(author_book)
                self.session.add(author_book)
                return 0

    def update_author_book(self, author_id, book_id, new_author_id, new_book_id):
        author = self.session.query(Author).get(new_author_id)
        book = self.session.query(Book).get(new_book_id)
        if not author or not book:
            return 1
        else:
            author_book_ex = self.session.query(Author_Book).get((new_author_id, new_book_id))
            if (author_book_ex):
                return 2
            else:
                author_book = self.session.query(Author_Book).get((author_id, book_id))
                author_book.author = author
                author_book.book = book
                author.books.append(author_book)
                book.authors.append(author_book)
                return 0

    def delete_author_book(self, author_id, book_id):
        author_book = self.session.query(Author_Book).get((author_id, book_id))
        self.session.delete(author_book)

    def read_member(self, name, surname):
        member = self.session.query(Member).filter(Member.name == name, Member.surname == surname).first()
        return member

    def read_members(self):
        members = self.session.query(Member).all()
        return members

    def create_member(self, name, surname, phone, email):
        member = Member(name, surname, phone, email)
        self.session.add(member)

    def update_member(self, id, name, surname, phone, email):
        member = self.session.query(Member).get(id)
        member.name = name
        member.surname = surname
        member.phone_number = phone
        member.email = email

    def delete_member(self, id):
        is_used = self.session.query(self.session.query(Abonnement).filter(Abonnement.member_id == id).exists()).scalar()
        if is_used:
            return False
        else:
            self.session.query(Member).filter(Member.id == id).delete()
            return True

    def read_abonnement(self, id):
        abonnement = self.session.query(Abonnement).get(id)
        return abonnement

    def read_abonnements(self):
        abonnements = self.session.query(Abonnement).all()
        return abonnements

    def create_abonnement(self, member_id, book_id, date_of_issue, date_of_return, is_returned):
        member = self.session.query(Member).get(member_id)
        book = self.session.query(Book).get(book_id)
        if not member or not book:
            return False
        else:
            abonnement = Abonnement(member_id, book_id, date_of_issue, date_of_return, is_returned)
            abonnement.member = member
            abonnement.book = book
            self.session.add(abonnement)
            return True


    def update_abonnement(self, id, member_id, book_id, date_of_issue, date_of_return, is_returned):
        member = self.session.query(Member).get(member_id)
        book = self.session.query(Book).get(book_id)
        if not member or not book:
            return False
        else:
            abonnement = self.session.query(Abonnement).get(id)
            abonnement.member = member
            abonnement.book = book
            abonnement.date_of_issue = date_of_issue
            abonnement.date_of_return = date_of_return
            abonnement.is_returned = is_returned
            return True

    def delete_abonnement(self, id):
        abonnement = self.session.query(Abonnement).get(id)
        self.session.delete(abonnement)
