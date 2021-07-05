from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    # 다른 table column 값 연동
    #owner = relationship("User", back_populates="items")


class License(Base):
    __tablename__ = 'license'

    id = Column(Integer, primary_key=True, index=True)
    companyname = Column(String, index=True)
    hostname = Column(String, index=True)
