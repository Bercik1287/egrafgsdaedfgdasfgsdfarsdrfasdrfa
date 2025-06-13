from pydantic import BaseModel, Field, validator
from typing import Union, List, Optional
from datetime import time
import json

class AutobusInCreate(BaseModel):
    rejestracja: str
    marka: str
    model: str

class AutobusOutput(BaseModel):
    id: int
    rejestracja: str
    marka: str
    model: str


class KierowcaInCreate(BaseModel):
    imie: str
    nazwisko: str
    pesel: str

class KierowcaOutput(BaseModel):
    id: int
    imie: str
    nazwisko: str


class BrygadaInCreate(BaseModel):
    nazwa: str

class BrygadaOutput(BaseModel):
    id: int
    nazwa: str


class PrzystanekInCreate(BaseModel):
    nazwa: str
    longi: float
    lati: float
    ulica: str

class PrzystanekOutput(BaseModel):
    id: int
    nazwa: str
    longi: float
    lati: float
    ulica: str

class WariantInCreate(BaseModel):
    nazwa: str
    kod: str

class WariantOutput(BaseModel):
    id: int
    nazwa: str
    kod: str

class LiniaInCreate(BaseModel):
    numer: str
    kierunek: str
    opis: str

class LiniaOutput(BaseModel):
    id: int
    numer: str
    kierunek: str
    opis: str

class TrasaInCreate(BaseModel):
    nazwa: str

class TrasaOutput(BaseModel):
    id: int
    nazwa: str

#-------------------------------

class PrzystanekBase(BaseModel):
    id: int
    nazwa: str
    ulica: Optional[str] = None
    longi: Optional[float] = None
    lati: Optional[float] = None
    
    class Config:
        orm_mode = True

class WariantBase(BaseModel):
    id: int
    nazwa: str
    kod_wariantu: str
    godziny_odjazdu: List[str] = []
    
    class Config:
        orm_mode = True

class TrasaCreate(BaseModel):
    przystanki_ids: List[int] = Field(..., min_items=2, description="Lista ID przystanków w kolejności")
    godziny_odjazdu: List[str] = Field(..., description="Godziny odjazdu w formacie HH:MM")
    nazwa_trasy: str = "Nowa trasa"
    kod_wariantu: str = "T1"
    numer_linii: Optional[str] = None

    @validator('godziny_odjazdu', each_item=True)
    def validate_hour(cls, v):
        try:
            time.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Nieprawidłowy format godziny. Użyj HH:MM")

class TrasaResponse(BaseModel):
    id: int
    nazwa: str
    wariant: WariantBase
    przystanki: List[PrzystanekBase]
    numer_linii: Optional[str] = None
    
    class Config:
        orm_mode = True

#---------------------------------

class AutobusInUpdate(BaseModel):
    id: int
    rejestracja: Union[str, None] = None
    marka: Union[str, None] = None
    model: Union[str, None] = None

class KierowcaInUpdate(BaseModel):
    id: int
    imie: Union[str, None] = None
    nazwisko: Union[str, None] = None
    pesel: Union[str, None] = None

class BrygadaInUpdate(BaseModel):
    id: int
    nazwa: Union[str, None] = None





class LiniaInUpdate(BaseModel):
    id: int
    numer: Union[str, None] = None
    kierunek: Union[str, None] = None
    opis: Union[str, None] = None



class PrzystanekInUpdate(BaseModel):
    id: int
    nazwa: Union[str, None] = None
    longi: Union[float, None] = None
    lati: Union[float, None] = None
    ulica: Union[str, None] = None



class TrasaInUpdate(BaseModel):
    id: int
    nazwa: Union[str, None] = None


class WariantInUpdate(BaseModel):
    id: int
    nazwa: Union[str, None] = None
    kod: Union[str, None] = None

# class UserOutput(BaseModel):
#     id: int
#     username: str
    
# class UserInUpdate(BaseModel):
#     id: int
#     username: Union[str, None] = None
#     password: Union[str, None] = None

# class UserInLogin(BaseModel):
#     username: str
#     password: str

# class UserWithToken(BaseModel):
#     token: str

class LinieTrasy(BaseModel):
    """Schema for assigning routes to lines"""
    line_id: int
    route_id: int
    line_number: Optional[str] = None

class LinieTrasy_Response(BaseModel):
    """Response schema for line-route assignment"""
    id: int
    line_id: int
    route_id: int
    line_number: str
    
    class Config:
        orm_mode = True

class RouteForLine(BaseModel):
    """Schema for routes assigned to a line"""
    route_id: int
    route_name: str
    line_number: Optional[str]
    assignment_id: int

class LineForRoute(BaseModel):
    """Schema for lines using a route"""
    line_id: int
    line_number: str
    line_direction: str
    line_description: Optional[str]
    assignment_id: int

class LineWithRoutes(BaseModel):
    """Schema for line with all its routes"""
    id: int
    numer: str
    kierunek: str
    opis: Optional[str]
    routes: List[RouteForLine]
    
    class Config:
        orm_mode = True

class RouteWithLines(BaseModel):
    """Schema for route with all lines using it"""
    id: int
    nazwa: str
    lines: List[LineForRoute]
    
    class Config:
        orm_mode = True