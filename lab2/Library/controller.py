from datetime import datetime

def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_member(self):
        name=input('Enter member\'s name: ')
        surname = input('Enter member\'s surname: ')
        member=self.model.read_member(name, surname)
        if not member:
            self.view.absent()
        else:
            self.view.show_member(member)

    def show_members(self):
        members=self.model.read_members()
        self.view.show_members(members)

    def create_member(self):
        name=input('Enter member\'s name: ')
        surname = input('Enter member\'s surname: ')
        phone = input('Enter member\'s phone number: ')
        email = input('Enter member\'s email: ')
        try:
            self.model.create_member(name, surname, phone, email)
        except:
            self.view.error()
        else:
            self.view.success()

    def update_member(self):
        id = input('Enter member\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            name=input('Enter member\'s name: ')
            surname = input('Enter member\'s surname: ')
            phone = input('Enter member\'s phone number: ')
            email = input('Enter member\'s email: ')
            try:
                self.model.create_member(id, name, surname, phone, email)
            except:
                self.view.error()
            else:
                self.view.success()

    def delete_member(self):
        id = input('Enter member\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            try:
                is_valid = self.model.delete_member(id)
            except:
                self.view.error()
            else:
                if is_valid:
                    self.view.success()
                else:
                    print("this member's id is used in other table")

    def show_author(self):
        name=input('Enter author\'s name: ')
        surname = input('Enter author\'s surname: ')
        author=self.model.read_author(name, surname)
        if not author:
            self.view.absent()
        else:
            self.view.show_author(author)

    def show_authors(self):
        authors=self.model.read_authors()
        self.view.show_authors(authors)

    def create_author(self):
        name=input('Enter author\'s name: ')
        surname = input('Enter author\'s surname: ')
        try:
            self.model.create_author(name, surname)
        except:
            self.view.error()
        else:
            self.view.success()

    def update_author(self):
        id = input('Enter author\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            name=input('Enter author\'s name: ')
            surname = input('Enter author\'s surname: ')
            try:
                self.model.update_author(id, name, surname)
            except:
                self.view.error()
            else:
                self.view.success()

    def delete_author(self):
        id = input('Enter author\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            try:
                is_valid = self.model.delete_author(id)
            except:
                self.view.error()
            else:
                if is_valid:
                    self.view.success()
                else:
                    print("this author's id is used in other table")

    def show_book(self):
        name=input('Enter book\'s name: ')
        book=self.model.read_book(name)
        if not book:
            self.view.absent()
        else:
            self.view.show_book(book)

    def show_books(self):
        books=self.model.read_books()
        self.view.show_books(books)

    def create_book(self):
        name=input('Enter book\'s name: ')
        isbn = input('Enter books\'s isbn: ')
        if not isbn.isnumeric():
            print("number is invalid")
        else:
            year = input('Enter books\'s year of publication: ')
            if not year.isnumeric():
                print("number is invalid")
            else:
                try:
                    self.model.create_book(name, isbn, year)
                except:
                    self.view.error()
                else:
                    self.view.success()

    def update_book(self):
        name=input('Enter book\'s name: ')
        id = input('Enter book\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            isbn = input('Enter books\'s isbn: ')
            if not isbn.isnumeric():
                print("number is invalid")
            else:
                year = input('Enter books\'s year of publication: ')
                if not year.isnumeric():
                    print("number is invalid")
                else:
                    try:
                        self.model.update_book(id, name, isbn, year)
                    except:
                        self.view.error()
                    else:
                        self.view.success()

    def delete_book(self):
        id = input('Enter book\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            try:
                is_valid = self.model.delete_book(id)
            except:
                self.view.error()
            else:
                if is_valid:
                    self.view.success()
                else:
                    print("this book's id is used in other table")


    def show_abonnement(self):
        id = input('Enter abonnement\'s id: ')
        abonnement=self.model.read_abonnement(id)
        if not abonnement:
            self.view.absent()
        else:
            self.view.show_abonnement(abonnement)

    def show_abonnements(self):
        abonnements = self.model.read_abonnements()
        self.view.show_abonnements(abonnements)

    def create_abonnement(self):
        member_id = input('Enter member\'s id: ')
        if not member_id.isnumeric():
            print("id must be a number")
        else:
            book_id = input('Enter books\'s id: ')
            if not book_id.isnumeric():
                print("id must be a number")
            else:
                date_of_issue = input('Enter date of issue: ')
                if not validate(date_of_issue):
                    print("date must be valid")
                else:
                    date_of_return = input('Enter date of return: ')
                    if not validate(date_of_return):
                        print("date must be valid")
                    else:
                        is_returned = input('Enter is book returned: ')
                        if is_returned == 'True' or is_returned == 'False':
                            try:
                                is_valid = self.model.create_abonnement(member_id, book_id, date_of_issue, date_of_return, is_returned)
                            except:
                                self.view.error()
                            else:
                                if is_valid:
                                    self.view.success()
                                else:
                                    print("not found corresponding member or book id")
                        else:
                            print("value must be 'True' or 'False'")

    def update_abonnement(self):
        id = input('Enter abonnement\'s id: ')
        member_id = input('Enter member\'s id: ')
        book_id = input('Enter books\'s id: ')
        if not member_id.isnumeric() or not book_id.isnumeric() or not id.isnumeric():
            print("id's must be numbers")
        else:
            date_of_issue = input('Enter date of issue: ')
            date_of_return = input('Enter date of return: ')
            if not validate(date_of_issue) or not validate(date_of_return):
                print("dates must be valid")
            else:
                is_returned = input('Enter is book returned: ')
                if is_returned == 'True' or is_returned == 'False':
                    try:
                        is_valid = self.model.update_abonnement(id, member_id, book_id, date_of_issue, date_of_return, is_returned)
                    except:
                        self.view.error()
                    else:
                        if is_valid:
                            self.view.success()
                        else:
                            print("not found corresponding member or book id")
                else:
                    print("value is invalid")

    def delete_abonnement(self):
        id = input('Enter abonnement\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            try:
                self.model.delete_abonnement(id)
            except:
                self.view.error()
            else:
                self.view.success()

    def show_authors_books(self):
        authors_books = self.model.read_authors_books()
        self.view.show_authors_books(authors_books)

    def create_author_book(self):
        author_id = input('Enter author\'s id: ')
        if not author_id.isnumeric():
            print("id must be a number")
        else:
            book_id = input('Enter books\'s id: ')
            if not book_id.isnumeric():
                print("id must be a number")
            else:
                try:
                    is_valid = self.model.create_author_book(author_id, book_id)
                except:
                    self.view.error()
                else:
                    if is_valid:
                        self.view.success()
                    else:
                        print("not found corresponding author or book id")

    def update_author_book(self):
        id = input('Enter author_book\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            author_id = input('Enter author\'s id: ')
            if not author_id.isnumeric():
                print("id must be a number")
            else:
                book_id = input('Enter books\'s id: ')
                if not book_id.isnumeric():
                    print("id must be a number")
                else:
                    try:
                        is_valid = self.model.update_author_book(id, author_id, book_id)
                    except:
                        self.view.error()
                    else:
                        if is_valid:
                            self.view.success()
                        else:
                            print("not found corresponding author or book id")

    def delete_author_book(self):
        id = input('Enter author_book\'s id: ')
        if not id.isnumeric():
            print("id must be a number")
        else:
            try:
                self.model.delete_author_book(id)
            except:
                self.view.error()
            else:
                self.view.success()


    def generate_members(self):
        quant = input('Enter number of members: ')
        if not quant.isnumeric():
            print("number is invalid")
        else:
            try:
                self.model.generate_members(quant)
            except:
                self.view.error()
            else:
                self.view.success()

    def generate_authors(self):
        quant = input('Enter number of authors: ')
        if not quant.isnumeric():
            print("number is invalid")
        else:
            try:
                self.model.generate_authors(quant)
            except:
                self.view.error()
            else:
                self.view.success()

    def generate_books(self):
        quant = input('Enter number of books: ')
        if not quant.isnumeric():
            print("number is invalid")
        else:
            try:
                self.model.generate_books(quant)
            except:
                self.view.error()
            else:
                self.view.success()



    def show_debts_query(self):
        date = input('After date: ')
        if not validate(date):
            print("date is invalid")
        else:
            quant = input('Books not returned more than: ')
            if not quant.isnumeric():
                print("number is invalid")
            else:
                debts = self.model.read_debts_query(date, quant)
                if not debts:
                    self.view.absent()
                else:
                    self.view.show_debts_query(debts, date, quant)

    def show_member_query(self):
        name = input('Name starts with: ')
        date1 = input('After date: ')
        if not validate(date1):
            print("date is invalid")
        else:
            date2 = input('Before date: ')
            if not validate(date2):
                print("date is invalid")
            else:
                member = self.model.read_member_query(name, date1, date2)
                if not member:
                    self.view.absent()
                else:
                    self.view.show_member_query(member, name, date1, date2)

    def show_popular_query(self):
        count = input('Amount of times book was taken more than: ')
        if not count.isnumeric():
            print("number is invalid")
        else:
            date1 = input('After date: ')
            if not validate(date1):
                print("date is invalid")
            else:
                date2 = input('Before date: ')
                if not validate(date2):
                    print("date is invalid")
                else:
                    year = input('Published after year: ')
                    if not year.isnumeric():
                        print("number is invalid")
                    else:
                        popular = self.model.read_popular_query(count, date1, date2, year)
                        if not popular:
                            self.view.absent()
                        else:
                            self.view.show_popular_query(popular, count, date1, date2, year)
