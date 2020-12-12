from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Author_Book(Base):
    __tablename__ = 'authors_books'
    author_id = Column(Integer, ForeignKey('authors.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    author = relationship("Author", back_populates="books")
    book = relationship("Book", back_populates="authors")

    def __init__(self, author_id, book_id):
        self.author_id = author_id
        self.book_id = book_id
