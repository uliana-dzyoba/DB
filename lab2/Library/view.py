from tabulate import tabulate

class View:

    def absent(self):
        print("-----no records------")

    def error(self):
        print("-----something went wrong------")

    def success(self):
        print("-----operation executed successfully------")

    def show_member(self, member):
        print(tabulate(member, headers=["id", "name", "surname", "phone", "email"]))

    def show_members(self, members):
        print('________________members_______________')
        print(tabulate(members, headers=["id", "name", "surname", "phone", "email"]))

    def show_author(self, author):
        print(tabulate(author, headers=["id", "name", "surname"]))

    def show_authors(self, authors):
        print('________________authors_______________')
        print(tabulate(authors, headers=["id", "name", "surname"]))

    def show_book(self, book):
        print(tabulate(book, headers=["id", "name", "ISBN", "published in"]))

    def show_books(self, books):
        print('________________books_______________')
        print(tabulate(books, headers=["id", "name", "ISBN", "published in"]))

    def show_abonnement(self, abonnement):
        print(tabulate(abonnement, headers=["id", "member id", "book id", "date of issue", "date of return", "is returned"]))

    def show_abonnements(self, abonnements):
        print('________________abonnements_______________')
        print(tabulate(abonnements, headers=["id", "member id", "book id", "date of issue", "date of return", "is returned"]))

    def show_authors_books(self, authors_books):
        print('________________authors_books_______________')
        print(tabulate(authors_books, headers=["id", "author id", "book id"]))

    def show_debts_query(self, debts, date, quant):
        print(f'___Abonnements of members who took books after {date} and didn\'t return more than {quant} books__')
        print(tabulate(debts, headers=["name", "surname", "email", "phone number", "abonnement id", "name of the book", "date of issue", "date of return", "is returned"]))

    def show_member_query(self, member, name, date1, date2):
        print(f'___Books returned between {date1} and {date2} by members whose name starts with {name}__')
        print(tabulate(member, headers=["name", "surname", "email", "name of the book", "date of issue", "date of return", "is returned"]))

    def show_popular_query(self, popular, count, date1, date2, year):
        print(f'___Books that were taken between {date1} and {date2} more than {count} times and were published after {year}__')
        print(tabulate(popular, headers=["name of the book", "name of the author", "surname of the author", "year of publication", "amount of times taken"]))