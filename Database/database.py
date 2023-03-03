from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import dotenv_values



DATAVASE_URI = dotenv_values('.env')["DATABASE_URL"]


engine = create_engine(
    DATAVASE_URI,
    echo=True
    )

Base = declarative_base()

session = sessionmaker()