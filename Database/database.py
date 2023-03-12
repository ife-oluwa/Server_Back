from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import dotenv_values



DATABASE_URI = dotenv_values('.env')["DATABASE_URL"]


engine = create_engine(
    DATABASE_URI,
    echo=True
    )

Base = declarative_base()

session = sessionmaker()