from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from base import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    isbn = Column(BigInteger)
    year_of_publication = Column(Integer)
    authors = relationship("Author_Book", back_populates="book")

    def __init__(self, name, isbn, year):
        self.name = name
        self.isbn = isbn
        self.year_of_publication = year
