from sqlalchemy import inspect
from tabulate import tabulate

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

class View:

    def absent(self):
        print("-----no records------")

    def error(self):
        print("-----something went wrong------")

    def success(self):
        print("-----operation executed successfully------")

    def show_author(self, author):
        print(tabulate([object_as_dict(author)], headers="keys", tablefmt="presto"))

    def show_authors(self, authors):
        print('________________authors_______________')
        printed = []
        for author in authors:
            printed.append(object_as_dict(author))
        print(tabulate(printed, headers="keys", tablefmt="presto"))

    def show_book(self, book):
        print(tabulate([object_as_dict(book)], headers="keys", tablefmt="presto"))

    def show_books(self, books):
        print('________________books_______________')
        printed = []
        for book in books:
            printed.append(object_as_dict(book))
        print(tabulate(printed, headers="keys", tablefmt="presto"))

    def show_authors_books(self, authors_books):
        print('________________authors_books_______________')
        printed = []
        for ab in authors_books:
            printed.append(object_as_dict(ab))
        print(tabulate(printed, headers="keys", tablefmt="presto"))

    def show_member(self, member):
        print(tabulate([object_as_dict(member)], headers="keys", tablefmt="presto"))

    def show_members(self, members):
        print('________________members_______________')
        printed = []
        for member in members:
            printed.append(object_as_dict(member))
        print(tabulate(printed, headers="keys", tablefmt="presto"))

    def show_abonnement(self, abonnement):
        print(tabulate([object_as_dict(abonnement)], headers="keys", tablefmt="presto"))

    def show_abonnements(self, abonnements):
        print('________________abonnements_______________')
        printed = []
        for abonnement in abonnements:
            printed.append(object_as_dict(abonnement))
        print(tabulate(printed, headers="keys", tablefmt="presto"))

