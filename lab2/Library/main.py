import psycopg2
import time
import psycopg2.extensions
from psycopg2.extras import LoggingConnection, LoggingCursor
import logging

from controller import Controller
from model import Model
from view import View

conn = psycopg2.connect(dbname="library", host="localhost", port=5432, user="postgres", password="28012001")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MyLoggingCursor simply sets self.timestamp at start of each query
class MyLoggingCursor(LoggingCursor):
    def execute(self, query, vars=None):
        self.timestamp = time.time()
        return super(MyLoggingCursor, self).execute(query, vars)

    def callproc(self, procname, vars=None):
        self.timestamp = time.time()
        return super(MyLoggingCursor, self).callproc(procname, vars)

# MyLogging Connection:
#   a) calls MyLoggingCursor rather than the default
#   b) adds resulting execution (+ transport) time via filter()
class MyLoggingConnection(LoggingConnection):
    def filter(self, msg, curs):
        return "   %d ms" % int((time.time() - curs.timestamp) * 1000)

    def cursor(self, *args, **kwargs):
        kwargs.setdefault('cursor_factory', MyLoggingCursor)
        return LoggingConnection.cursor(self, *args, **kwargs)

#db_settings = {dbname="library", host="localhost", port=5432, user="postgres", password="28012001"}

conn_time = psycopg2.connect(connection_factory=MyLoggingConnection, dbname="library", host="localhost", port=5432, user="postgres", password="28012001")
conn_time.initialize(logger)


c = Controller(Model(conn, conn_time), View())
#c.show_member()
# c.show_author()
# c.show_debts_query()
# c.show_member_query()
# c.show_popular_query()
# c.create_book()
# c.create_abonnement()
# c.delete_book()
# c.generate_authors()
# c.show_authors()

# print("________Create new abonnement_________")
# c.create_abonnement()
# print("________Delete a book_________")
# c.delete_book()
# print("________Delete a member_________")
# c.delete_member()
# print("________Create author-book connection_________")
# c.create_author_book()
# print("________Generate random books_________")
# c.generate_books()
# print("________Generate random members_________")
# c.generate_members()
# print("________Member query_________")
# c.show_member_query()
# print("________Debts query_________")
# c.show_debts_query()
# print("________Popular books query_________")
# c.show_popular_query()
# conn.commit()

