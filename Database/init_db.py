from database import engine, Base

from models import User, Predictions

Base.metadata.create_all(bind=engine)

