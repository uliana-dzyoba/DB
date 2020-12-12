from sqlalchemy import Column, Integer, String
from base import Base


class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone_number = Column(String)
    email = Column(String)

    def __init__(self, name, surname, phone, email):
        self.name = name
        self.surname = surname
        self.phone_number = phone
        self.email = email
