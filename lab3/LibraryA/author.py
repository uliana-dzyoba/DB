from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    books = relationship("Author_Book", back_populates="author")

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname