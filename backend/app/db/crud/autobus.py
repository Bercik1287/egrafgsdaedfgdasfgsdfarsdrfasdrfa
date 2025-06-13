from sqlalchemy.orm import Session
from ..models.system import Autobusy, Kierowcy, Brygady, Przystanki, Warianty, Trasy, Linie, Linie_Trasy
from ..schema.autobus import (
    LiniaInCreate, AutobusInCreate, KierowcaInCreate, BrygadaInCreate, 
    PrzystanekInCreate, WariantInCreate, TrasaInCreate, LiniaInCreate,
    AutobusInUpdate, KierowcaInUpdate, BrygadaInUpdate, PrzystanekInUpdate,
    WariantInUpdate, TrasaInUpdate, LiniaInUpdate
)
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import text

#autobus
def create_autobus(db: Session, autobus: AutobusInCreate):
    db_autobus = Autobusy(
        rejestracja=autobus.rejestracja,
        marka=autobus.marka,
        model=autobus.model
    )
    db.add(db_autobus)
    db.commit()
    db.refresh(db_autobus)
    return db_autobus

#kierowca
def create_kierowca(db: Session, kierowca: KierowcaInCreate):
    db_kierowca = Kierowcy(
        imie=kierowca.imie,
        nazwisko=kierowca.nazwisko,
        pesel=kierowca.pesel
    )
    db.add(db_kierowca)
    db.commit()
    db.refresh(db_kierowca)
    return db_kierowca

def create_brygada(db: Session, brygada: BrygadaInCreate):
    db_brygada = Brygady(nazwa=brygada.nazwa)
    db.add(db_brygada)
    db.commit()
    db.refresh(db_brygada)
    return db_brygada

def create_przystanek(db: Session, przystanek: PrzystanekInCreate):
    db_przystanek = Przystanki(
        nazwa=przystanek.nazwa,
        longi=przystanek.longi,
        lati=przystanek.lati,
        ulica=przystanek.ulica
    )
    db.add(db_przystanek)
    db.commit()
    db.refresh(db_przystanek)
    return db_przystanek

def create_wariant(db: Session, wariant: WariantInCreate):
    db_wariant = Warianty(
        nazwa=wariant.nazwa,
        kod_wariantu=wariant.kod_wariantu
    )
    db.add(db_wariant)
    db.commit()
    db.refresh(db_wariant)
    return db_wariant

def create_trasa(db: Session, trasa: TrasaInCreate):
    db_trasa = Trasy(nazwa=trasa.nazwa)
    db.add(db_trasa)
    db.commit()
    db.refresh(db_trasa)
    return db_trasa

def create_linie(db: Session, linia: LiniaInCreate):
    try:
        db_linia = Linie(
            numer=linia.numer,
            kierunek=linia.kierunek,
            opis=linia.opis
        )
        db.add(db_linia)
        db.commit()
        db.refresh(db_linia)
        return db_linia
    except IntegrityError:
        db.rollback()
        raise


#GET

def get_linie(db: Session):
    return db.query(Linie).order_by(Linie.numer.asc()).all()

def get_linia_by_id(db: Session, linia_id: int):
    return db.query(Linie).filter(Linie.id == linia_id).first()

def get_przystanki(db: Session):
    return db.query(Przystanki).all()

def get_przystanek_by_id(db: Session, przystanek_id: int):
    return db.query(Przystanki).filter(Przystanki.id == przystanek_id).first()

def get_autobusy(db: Session):
    return db.query(Autobusy).all()

def get_autobus_by_id(db: Session, autobus_id: int):
    return db.query(Autobusy).filter(Autobusy.id == autobus_id).first()

def get_kierowcy(db: Session):
    return db.query(Kierowcy).all()

def get_kierowca_by_id(db: Session, kierowca_id: int):
    return db.query(Kierowcy).filter(Kierowcy.id == kierowca_id).first()

def get_brygady(db: Session):
    return db.query(Brygady).order_by(Brygady.nazwa).all()

def get_brygada_by_id(db: Session, brygada_id: int):
    return db.query(Brygady).filter(Brygady.id == brygada_id).first()

def get_trasy(db: Session):
    return db.query(Trasy).all()

def get_trasa_by_id(db: Session, trasa_id: int):
    return db.query(Trasy).filter(Trasy.id == trasa_id).first()

def get_warianty(db: Session):
    return db.query(Warianty).all()

def get_wariant_by_id(db: Session, wariant_id: int):
    return db.query(Warianty).filter(Warianty.id == wariant_id).first()

#ALTER
#procedure ---------------------------
def update_autobus(db: Session, autobus_update: AutobusInUpdate):
    try:
        db.execute(
            text("""
                CALL update_autobus(:id, :rejestracja, :marka, :model)
            """),
            {
                "id": autobus_update.id,
                "rejestracja": autobus_update.rejestracja,
                "marka": autobus_update.marka,
                "model": autobus_update.model
            }
        )
        db.commit()
        result = db.execute(
            text('SELECT * FROM "Autobusy" WHERE id = :id'),
            {"id": autobus_update.id}
        ).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Autobus nie zostal znaleziony")
        return dict(result._mapping)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Numer rejestracyjny już istnieje w systemie!")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# CREATE OR REPLACE PROCEDURE update_autobus(
#     p_id INT,
#     p_rejestracja TEXT,
#     p_marka TEXT,
#     p_model TEXT
# )
# LANGUAGE plpgsql
# AS $$
# BEGIN
#     UPDATE "Autobusy"
#     SET
#         rejestracja = COALESCE(p_rejestracja, rejestracja),
#         marka = COALESCE(p_marka, marka),
#         model = COALESCE(p_model, model)
#     WHERE id = p_id;

#     IF NOT FOUND THEN
#         RAISE EXCEPTION 'Autobus nie zostal znaleziony';
#     END IF;
# END;
# $$;


def update_kierowca(db: Session, kierowca_update: KierowcaInUpdate):
    db_kierowca = db.query(Kierowcy).filter(Kierowcy.id == kierowca_update.id).first()
    if not db_kierowca:
        raise HTTPException(status_code=404, detail="Kierowca nie zostal znaleziony")
    
    update_data = kierowca_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_kierowca, key, value)
    
    try:
        db.commit()
        db.refresh(db_kierowca)
        return db_kierowca
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="PESEL już istnieje w systemie!")
#END procedure ---------------------------

#Trigger ------------------
def update_brygada(db: Session, brygada_update: BrygadaInUpdate):
    try:
        result = db.execute(
            text("""
                UPDATE "Brygady"
                SET nazwa = COALESCE(:nazwa, nazwa)
                WHERE id = :id
                RETURNING *;
            """),
            {
                "id": brygada_update.id,
                "nazwa": brygada_update.nazwa
            }
        ).fetchone()
        db.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Brygada nie zostala znaleziona")
        return dict(result._mapping)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Brygada o tej nazwie już istnieje!")

# CREATE OR REPLACE FUNCTION aktualizuj_date_brygady()
# RETURNS TRIGGER AS $$
# BEGIN
#     NEW.zmieniono_dnia := now();
#     RETURN NEW;
# END;
# $$ LANGUAGE plpgsql;

# -- Trigger na UPDATE
# CREATE TRIGGER trg_update_brygady_data
# BEFORE UPDATE ON "Brygady"
# FOR EACH ROW
# EXECUTE FUNCTION aktualizuj_date_brygady();

#END Trigger ------------------
def update_przystanek(db: Session, przystanek_update: PrzystanekInUpdate):
    db_przystanek = db.query(Przystanki).filter(Przystanki.id == przystanek_update.id).first()
    if not db_przystanek:
        raise HTTPException(status_code=404, detail="Przystanek nie zostal znaleziony")
    
    update_data = przystanek_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_przystanek, key, value)
    
    try:
        db.commit()
        db.refresh(db_przystanek)
        return db_przystanek
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Przystanek o tej nazwie już istnieje!")

def update_linia(db: Session, linia_update: LiniaInUpdate):
    db_linia = db.query(Linie).filter(Linie.id == linia_update.id).first()
    if not db_linia:
        raise HTTPException(status_code=404, detail="Linia nie zostala znaleziona")
    
    update_data = linia_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_linia, key, value)
    
    try:
        db.commit()
        db.refresh(db_linia)
        return db_linia
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Linia o tym numerze już istnieje!")

def update_trasa(db: Session, trasa_update: TrasaInUpdate):
    db_trasa = db.query(Trasy).filter(Trasy.id == trasa_update.id).first()
    if not db_trasa:
        raise HTTPException(status_code=404, detail="Trasa nie zostala znaleziona")
    
    update_data = trasa_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_trasa, key, value)
    
    try:
        db.commit()
        db.refresh(db_trasa)
        return db_trasa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Trasa o tej nazwie już istnieje!")

def update_wariant(db: Session, wariant_update: WariantInUpdate):
    db_wariant = db.query(Warianty).filter(Warianty.id == wariant_update.id).first()
    if not db_wariant:
        raise HTTPException(status_code=404, detail="Wariant nie zostal znaleziony")
    
    update_data = wariant_update.dict(exclude_unset=True, exclude={'id'})
    if 'kod' in update_data:
        update_data['kod_wariantu'] = update_data.pop('kod')
    
    for key, value in update_data.items():
        if value is not None:
            setattr(db_wariant, key, value)
    
    try:
        db.commit()
        db.refresh(db_wariant)
        return db_wariant
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Kod wariantu już istnieje w systemie!")


#DELETE
def delete_autobus(db: Session, autobus_id: int):
    result = db.execute(
        text("SELECT rejestracja FROM \"Autobusy\" WHERE id = :id"),
        {"id": autobus_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Autobus nie zostal znaleziony")
    rejestracja = result[0]

    try:
        db.execute(
            text("DELETE FROM \"Autobusy\" WHERE id = :id"),
            {"id": autobus_id}
        )
        db.commit()
        return {"message": f"Autobus {rejestracja} zostal usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunac autobusu - jest używany w systemie")



def delete_kierowca(db: Session, kierowca_id: int):
    # Pobierz dane kierowcy do komunikatu
    result = db.execute(
        text("SELECT imie, nazwisko FROM \"Kierowcy\" WHERE id = :id"),
        {"id": kierowca_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Kierowca nie zostal znaleziony")
    imie, nazwisko = result

    try:
        db.execute(
            text("DELETE FROM \"Kierowcy\" WHERE id = :id"),
            {"id": kierowca_id}
        )
        db.commit()
        return {"message": f"Kierowca {imie} {nazwisko} zostal usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunac kierowcy - jest przypisany do brygady")

def delete_brygada(db: Session, brygada_id: int):
    # Pobierz nazwę brygady do komunikatu
    result = db.execute(
        text("SELECT nazwa FROM \"Brygady\" WHERE id = :id"),
        {"id": brygada_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Brygada nie zostala znaleziona")
    nazwa = result[0]

    try:
        db.execute(
            text("DELETE FROM \"Brygady\" WHERE id = :id"),
            {"id": brygada_id}
        )
        db.commit()
        return {"message": f"Brygada {nazwa} zostala usunięta"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunac brygady - ma przypisanych kierowców lub autobusy")

def delete_przystanek(db: Session, przystanek_id: int):
    # Pobierz nazwę przystanku do komunikatu
    result = db.execute(
        text("SELECT nazwa FROM \"Przystanki\" WHERE id = :id"),
        {"id": przystanek_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Przystanek nie zostal znaleziony")
    nazwa = result[0]

    try:
        db.execute(
            text("DELETE FROM \"Przystanki\" WHERE id = :id"),
            {"id": przystanek_id}
        )
        db.commit()
        return {"message": f"Przystanek {nazwa} zostal usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunac przystanku - jest używany w trasach")

def delete_linia(db: Session, linia_id: int):
    # Pobierz numer linii do komunikatu
    result = db.execute(
        text("SELECT numer FROM \"Linie\" WHERE id = :id"),
        {"id": linia_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Linia nie zostala znaleziona")
    numer = result[0]

    try:
        db.execute(
            text("DELETE FROM \"Linie\" WHERE id = :id"),
            {"id": linia_id}
        )
        db.commit()
        return {"message": f"Linia {numer} zostala usunięta"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunac linii - ma przypisane trasy lub brygady")

def delete_trasa(db: Session, trasa_id: int):
    # Pobierz nazwę trasy do komunikatu
    result = db.execute(
        text("SELECT nazwa FROM \"Trasy\" WHERE id = :id"),
        {"id": trasa_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Trasa nie zostala znaleziona")
    nazwa = result[0]

    try:
        db.execute(
            text("DELETE FROM \"Trasy\" WHERE id = :id"),
            {"id": trasa_id}
        )
        db.commit()
        return {"message": f"Trasa {nazwa} zostala usunięta"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunac trasy - jest używana przez linie")

def delete_wariant(db: Session, wariant_id: int):
    # Pobierz nazwę wariantu do komunikatu
    result = db.execute(
        text("SELECT nazwa FROM \"Warianty\" WHERE id = :id"),
        {"id": wariant_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Wariant nie zostal znaleziony")
    nazwa = result[0]

    try:
        db.execute(
            text("DELETE FROM \"Warianty\" WHERE id = :id"),
            {"id": wariant_id}
        )
        db.commit()
        return {"message": f"Wariant {nazwa} zostal usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunac wariantu - jest używany w trasach")

#generator
def assign_route_to_line(db: Session, line_id: int, route_id: int, line_number: str = None):
    """
    Przypisz trase do linii
    """
    try:
        line = db.query(Linie).filter(Linie.id == line_id).first()
        if not line:
            raise ValueError(f"Linia z ID {line_id} nie istnieje")
        
        route = db.query(Trasy).filter(Trasy.id == route_id).first()
        if not route:
            raise ValueError(f"Trasa z ID {route_id} nie istnieje")
        
        existing = db.query(Linie_Trasy).filter(
            Linie_Trasy.id_linie == line_id,
            Linie_Trasy.id_trasy == route_id
        ).first()
        
        if existing:
            raise ValueError("Trasa jest już przypisana do tej linii")
        
        line_route = Linie_Trasy(
            id_linie=line_id,
            id_trasy=route_id,
            numer_linii=line_number or line.numer
        )
        
        db.add(line_route)
        db.commit()
        db.refresh(line_route)
        
        return line_route
        
    except IntegrityError:
        db.rollback()
        raise ValueError("Database integrity error - check if the relationship already exists")

def remove_route_from_line(db: Session, line_id: int, route_id: int):
    """
    Remove a route from a line
    """
    line_route = db.query(Linie_Trasy).filter(
        Linie_Trasy.id_linie == line_id,
        Linie_Trasy.id_trasy == route_id
    ).first()
    
    if not line_route:
        raise ValueError("Route is not assigned to this line")
    
    db.delete(line_route)
    db.commit()
    
    return {"message": "Route removed from line successfully"}

def get_routes_for_line(db: Session, line_id: int):
    """
    Get all routes assigned to a specific line
    """
    line_routes = db.query(Linie_Trasy, Trasy).join(
        Trasy, Linie_Trasy.id_trasy == Trasy.id
    ).filter(Linie_Trasy.id_linie == line_id).all()
    
    routes = []
    for line_route, route in line_routes:
        routes.append({
            "route_id": route.id,
            "route_name": route.nazwa,
            "line_number": line_route.numer_linii,
            "assignment_id": line_route.id
        })
    
    return routes

def get_lines_for_route(db: Session, route_id: int):
    """
    Get all lines that use a specific route
    """
    route_lines = db.query(Linie_Trasy, Linie).join(
        Linie, Linie_Trasy.id_linie == Linie.id
    ).filter(Linie_Trasy.id_trasy == route_id).all()
    
    lines = []
    for route_line, line in route_lines:
        lines.append({
            "line_id": line.id,
            "line_number": line.numer,
            "line_direction": line.kierunek,
            "line_description": line.opis,
            "assignment_id": route_line.id
        })
    
    return lines

def get_lines_for_route_2(db: Session, route_id: int):
    result = db.execute(
        text("""
            SELECT line_id, line_number, line_direction, line_description, assignment_id
            FROM lines_for_routes_2
            WHERE route_id = :route_id
        """),
        {"route_id": route_id}
    ).fetchall()
    return [dict(row._mapping) for row in result]