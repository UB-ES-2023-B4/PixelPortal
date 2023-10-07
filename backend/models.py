from sqlalchemy import Boolean, MetaData, Column, ForeignKey, Integer, String, Date, Float, Enum, UniqueConstraint, Table,LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from database import Base
class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)
    username = Column(String(30), ForeignKey('accounts.username'), nullable=False)

    account = relationship('Account', back_populates='images')
    def __init__(self, name, data, account):
        self.name = name
        self.data = data
        self.account = account
class Account(Base):
    __tablename__ = 'accounts'
    username = Column(String(30), primary_key=True, unique=True, nullable=False)
    password = Column(String(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = Column(Integer, nullable=False)
    orders = relationship('Order', backref='orders', lazy=True)

    images = relationship('Image', back_populates='account')
    def __init__(self, username,password, is_admin=0):
        self.username = username
        self.password = password
        self.is_admin = is_admin

