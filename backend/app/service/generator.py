from fpdf import FPDF
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.system import (
    Linie, Przystanki, Warianty, Trasy,
    Przystanki_Warianty, Warianty_Trasy, Linie_Trasy,
    Brygady, Brygady_Linie, Kierowcy, Kierowcy_Brygady,
    Autobusy, Brygady_Autobusy
)

class PDFSchedule(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Rozkład Jazdy Autobusów', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Strona {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, body)
        self.ln()

def generate_schedule_pdf(db: Session = Depends(get_db), line_number=None, output_file='rozklad_jazdy.pdf'):
    pdf = PDFSchedule()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    if line_number:
        line = db.query(Linie).filter_by(numer=line_number).first()
        if not line:
            print(f"Linia {line_number} nie istnieje!")
            return
        
        pdf.chapter_title(f"Rozkład jazdy dla linii {line.numer} - {line.kierunek}")
        
        pdf.set_font('Arial', 'I', 10)
        for brigade_link in line.brygada_ref:
            brigade = brigade_link.brygada_ref
            pdf.cell(0, 6, f"Brygada: {brigade.nazwa}", 0, 1)
            
            for driver_link in brigade.kierowca_ref:
                driver = driver_link.kierowca_ref
                pdf.cell(0, 6, f"Kierowca: {driver.imie} {driver.nazwisko}", 0, 1)
            
            for bus_link in brigade.autobus_ref:
                bus = bus_link.autobus_ref
                pdf.cell(0, 6, f"Autobus: {bus.marka} {bus.model} ({bus.rejestracja})", 0, 1)
        
        pdf.ln(5)
        
        for line_route in line.trasa_ref:
            route = line_route.trasa_ref
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, f"Trasa: {route.nazwa}", 0, 1)
            pdf.set_font('Arial', '', 10)
            
            for route_variant in route.wariant_ref:
                variant = route_variant.wariant_ref
                pdf.cell(0, 6, f"Wariant {variant.kod_wariantu}: {variant.nazwa}", 0, 1)
                
                for variant_stop in variant.przystanek_ref:
                    stop = variant_stop.przystanek_ref
                    pdf.cell(0, 6, f"- {stop.nazwa} ({stop.ulica})", 0, 1)
                
                pdf.ln(3)
    else:
        lines = db.query(Linie).order_by(Linie.numer).all()
        
        for line in lines:
            pdf.chapter_title(f"Linia {line.numer} - {line.kierunek}")
            
            pdf.set_font('Arial', 'I', 10)
            for brigade_link in line.brygada_ref:
                brigade = brigade_link.brygada_ref
                pdf.cell(0, 6, f"Brygada: {brigade.nazwa}", 0, 1)
                
                for driver_link in brigade.kierowca_ref:
                    driver = driver_link.kierowca_ref
                    pdf.cell(0, 6, f"Kierowca: {driver.imie} {driver.nazwisko}", 0, 1)
                
                for bus_link in brigade.autobus_ref:
                    bus = bus_link.autobus_ref
                    pdf.cell(0, 6, f"Autobus: {bus.marka} {bus.model} ({bus.rejestracja})", 0, 1)
            
            pdf.ln(5)
            
            for line_route in line.trasa_ref:
                route = line_route.trasa_ref
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, f"Trasa: {route.nazwa}", 0, 1)
                pdf.set_font('Arial', '', 10)
                
                for route_variant in route.wariant_ref:
                    variant = route_variant.wariant_ref
                    pdf.cell(0, 6, f"Wariant {variant.kod_wariantu}: {variant.nazwa}", 0, 1)
                    
                    for variant_stop in variant.przystanek_ref:
                        stop = variant_stop.przystanek_ref
                        pdf.cell(0, 6, f"- {stop.nazwa} ({stop.ulica})", 0, 1)
                    
                    pdf.ln(3)
            
            pdf.add_page()
    
    pdf.set_y(-30)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 0, 'C')
    
    pdf.output(output_file)
    print(f"Wygenerowano rozkład jazdy: {output_file}")
