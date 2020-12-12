from controller import Controller
from model import Model
from view import View


from base import Session

# 2 - extract a session
session = Session()

c = Controller(Model(session), View())
# c.create_author()
# c.show_authors()
# c.show_author()
# c.update_author()
# c.delete_author()

# c.create_author_book()
# c.show_authors_books()
# c.update_author_book()
# c.delete_author_book()



session.commit()


