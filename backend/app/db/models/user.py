from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(250))

    rola_ref = relationship("User_Rola", back_populates="user_ref")
                                                       
class User_Rola(Base):
    __tablename__ = "User_Rola"
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("Users.id"))
    id_rola = Column(Integer, ForeignKey("Rola.id"))

    user_ref = relationship("User", back_populates="rola_ref")
    rola_ref = relationship("Rola", back_populates="user_ref")


class Rola(Base):
    __tablename__ = "Rola"
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(50))

    user_ref = relationship("User_Rola", back_populates="rola_ref")