from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime as dt
from sqlalchemy.sql import func




class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False)
    predictions = relationship("Predictions", back_populates='user')
    data_created = Column(DateTime(timezone=True), server_default=func.now())


    def __repr__(self) -> str:
        return f"<User {self.username}"
    


class Predictions(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    predictions = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='predictions')


    def __repr__(self):
        return f"<Predictions {self.id}"