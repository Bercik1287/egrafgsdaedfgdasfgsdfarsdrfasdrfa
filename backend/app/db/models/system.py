from app.core.database import Base
from sqlalchemy import Text, Column, Integer, String, Double, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

class Przystanki(Base):
    __tablename__ = "Przystanki"
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(50), unique=True)
    longi = Column(Double)
    lati = Column(Double)
    ulica = Column(String(50))

    wariant_ref = relationship("Przystanki_Warianty", back_populates="przystanek_ref")


class Przystanki_Warianty(Base):
    __tablename__ = "Przystanki_Warianty"
    id = Column(Integer, primary_key=True)
    id_przystanki = Column(Integer, ForeignKey("Przystanki.id"))
    id_warianty = Column(Integer, ForeignKey("Warianty.id"))
    kolejnosc = Column(Integer)

    przystanek_ref = relationship("Przystanki", back_populates="wariant_ref")
    wariant_ref = relationship("Warianty", back_populates="przystanek_ref")


class Warianty(Base):
    __tablename__ = "Warianty"
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(50))
    kod_wariantu = Column(String(5))
    godziny_odjazdu = Column(String)

    przystanek_ref = relationship("Przystanki_Warianty", back_populates="wariant_ref")
    trasa_ref = relationship("Warianty_Trasy", back_populates="wariant_ref")


class Warianty_Trasy(Base):
    __tablename__ = "Warianty_Trasy"
    id = Column(Integer, primary_key=True)
    id_warianty = Column(Integer, ForeignKey("Warianty.id"))
    id_trasy = Column(Integer, ForeignKey("Trasy.id"))

    wariant_ref = relationship("Warianty", back_populates="trasa_ref")
    trasa_ref = relationship("Trasy", back_populates="wariant_ref")


class Trasy(Base):
    __tablename__ = "Trasy"
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(50))

    wariant_ref = relationship("Warianty_Trasy", back_populates="trasa_ref")
    linia_ref = relationship("Linie_Trasy", back_populates="trasa_ref")


class Linie_Trasy(Base):
    __tablename__ = "Linie_Trasy"
    id = Column(Integer, primary_key=True)
    id_linie = Column(Integer, ForeignKey("Linie.id"))
    id_trasy = Column(Integer, ForeignKey("Trasy.id"))
    numer_linii = Column(String)

    linia_ref = relationship("Linie", back_populates="trasa_ref")
    trasa_ref = relationship("Trasy", back_populates="linia_ref")


class Linie(Base):
    __tablename__ = "Linie"
    id = Column(Integer, primary_key=True)
    numer = Column(String(25), unique=True)
    kierunek = Column(String(50))
    opis = Column(String(100))

    trasa_ref = relationship("Linie_Trasy", back_populates="linia_ref")
    brygada_ref = relationship("Brygady_Linie", back_populates="linia_ref")


class Brygady_Linie(Base):
    __tablename__ = "Brygady_Linie"
    id = Column(Integer, primary_key=True)
    id_brygady = Column(Integer, ForeignKey("Brygady.id"))
    id_linie = Column(Integer, ForeignKey("Linie.id"))

    brygada_ref = relationship("Brygady", back_populates="linia_ref")
    linia_ref = relationship("Linie", back_populates="brygada_ref")


class Brygady(Base):
    __tablename__ = "Brygady"
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(25), unique=True)
    zmieniono_dnia = Column(DateTime)

    linia_ref = relationship("Brygady_Linie", back_populates="brygada_ref")
    kierowca_ref = relationship("Kierowcy_Brygady", back_populates="brygada_ref")
    autobus_ref = relationship("Brygady_Autobusy", back_populates="brygada_ref")




class Kierowcy(Base):
    __tablename__ = "Kierowcy"
    id = Column(Integer, primary_key=True)
    imie = Column(String(30))
    nazwisko = Column(String(30))
    pesel = Column(String(11), unique=True)

    brygada_ref = relationship("Kierowcy_Brygady", back_populates="kierowca_ref")


class Kierowcy_Brygady(Base):
    __tablename__ = "Kierowcy_Brygady"
    id = Column(Integer, primary_key=True)
    id_kierowcy = Column(Integer, ForeignKey("Kierowcy.id"))
    id_brygady = Column(Integer, ForeignKey("Brygady.id"))

    kierowca_ref = relationship("Kierowcy", back_populates="brygada_ref")
    brygada_ref = relationship("Brygady", back_populates="kierowca_ref")




class Autobusy(Base):
    __tablename__ = "Autobusy"
    id = Column(Integer, primary_key=True)
    rejestracja = Column(String(7), unique=True)
    marka = Column(String(25))
    model = Column(String(25))

    brygada_ref = relationship("Brygady_Autobusy", back_populates="autobus_ref")


class Brygady_Autobusy(Base):
    __tablename__ = "Brygady_Autobusy"
    id = Column(Integer, primary_key=True)
    id_brygady = Column(Integer, ForeignKey("Brygady.id"))
    id_autobusy = Column(Integer, ForeignKey("Autobusy.id"))

    autobus_ref = relationship("Autobusy", back_populates="brygada_ref")
    brygada_ref = relationship("Brygady", back_populates="autobus_ref")

class Odjazdy(Base):
    __tablename__ = "Odjazdy"
    id = Column(Integer, primary_key=True)
    id_warianty = Column(Integer, ForeignKey("Warianty.id"))
    id_przystanku = Column(Integer, ForeignKey("Przystanki.id"))
    godzina = Column(Time)