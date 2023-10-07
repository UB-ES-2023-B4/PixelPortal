from sqlalchemy import Boolean, MetaData, Column, ForeignKey, Integer, String, Date, Float, Enum, UniqueConstraint, Table,LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from database import Base
from sqlalchemy.sql import func  # Importa func
class Publication(Base):
    __tablename__ = 'publication'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)
    username = Column(String(30), ForeignKey('accounts.username'), nullable=False)
    description = Column(String(500), nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    account = relationship('Account', back_populates='images')
    def __init__(self, name, data, account,description):
        self.name = name
        self.data = data
        self.account = account
        self.description = description
class Account(Base):
    __tablename__ = 'accounts'
    username = Column(String(30), primary_key=True, unique=True, nullable=False)
    password = Column(String(), nullable=False)
    email = Column(String(100), nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = Column(Integer, nullable=False)

    publications = relationship('Publication', back_populates='account')
    def __init__(self, username,password, is_admin=0):
        self.username = username
        self.password = password
        self.is_admin = is_admin

