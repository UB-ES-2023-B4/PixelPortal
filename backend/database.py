import os
#from utils import  production
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Ej4Lu2pWrA8U3W0D@db.taomhirwekysblnfqxea.supabase.co:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
# check_same_thread...is needed only for SQLite. It's not needed for other databases.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()