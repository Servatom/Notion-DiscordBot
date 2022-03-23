from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

url = os.environ.get('DATABASE_URL')
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
#SQLALCHEMY_DATABASE_URI = 'sqlite:///form.sqlite'
SQLALCHEMY_DATABASE_URI = url

engine = create_engine(SQLALCHEMY_DATABASE_URI)
#engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': True},pool_pre_ping=True,pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()