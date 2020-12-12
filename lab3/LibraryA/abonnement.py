from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Abonnement(Base):
    __tablename__ = 'abonnements'
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    date_of_issue = Column(Date)
    date_of_return = Column(Date)
    is_returned = Column(Boolean)
    member = relationship("Member", backref="abonnements")
    book = relationship("Book", backref="abonnements")

    def __init__(self, member_id, book_id, date_of_issue, date_of_return, is_returned):
        self.member_id = member_id
        self.book_id = book_id
        self.date_of_issue = date_of_issue
        self.date_of_return = date_of_return
        self.is_returned = is_returned
