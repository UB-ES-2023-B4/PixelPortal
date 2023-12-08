import os
#from utils import  production
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Development backend path -> en main.py hay que comentar 4 lineas mas y abajo del todo tienes dos lienas mas para comentar
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

#Production backend path
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Ej4Lu2pWrA8U3W0D@db.taomhirwekysblnfqxea.supabase.co:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
if (SQLALCHEMY_DATABASE_URL == "sqlite:///./test.db"):
    Base.metadata.drop_all(bind=engine)