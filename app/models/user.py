from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    celular = Column(String, unique=True, index=True, nullable=False)
    id_login = Column(Integer, ForeignKey("logins.id"), unique=True, nullable=False)

    login = relationship("Login")
