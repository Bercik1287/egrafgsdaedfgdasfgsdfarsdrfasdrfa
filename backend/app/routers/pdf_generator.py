from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from fpdf import FPDF
from app.db.models.system import (
    Linie, Trasy, Warianty, Przystanki, 
    Przystanki_Warianty, Warianty_Trasy, 
    Linie_Trasy
)
from datetime import datetime
import json
import os
import tempfile
from typing import List, Dict

class BusSchedulePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Rozklad Jazdy Autobusow', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f'Wygenerowano: {datetime.now().strftime("%d.%m.%Y %H:%M")}', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Strona {self.page_no()}', 0, 0, 'C')

class ScheduleGenerator:
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def get_line_schedules(self) -> List[Dict]:
        schedules = []
        lines = self.db.query(Linie).order_by(Linie.numer).all()
        
        for line in lines:
            line_data = {
                'numer': line.numer,
                'kierunek': line.kierunek,
                'opis': line.opis,
                'trasy': []
            }
            line_routes = (self.db.query(Linie_Trasy, Trasy)
                          .join(Trasy, Linie_Trasy.id_trasy == Trasy.id)
                          .filter(Linie_Trasy.id_linie == line.id)
                          .all())
            
            for line_route, route in line_routes:
                route_data = {
                    'nazwa': route.nazwa,
                    'warianty': []
                }
                
                route_variants = (self.db.query(Warianty_Trasy, Warianty)
                                .join(Warianty, Warianty_Trasy.id_warianty == Warianty.id)
                                .filter(Warianty_Trasy.id_trasy == route.id)
                                .all())
                
                for route_variant, variant in route_variants:
                    variant_data = {
                        'nazwa': variant.nazwa,
                        'kod': variant.kod_wariantu,
                        'godziny': [],
                        'przystanki': []
                    }
                    
                    if variant.godziny_odjazdu:
                        try:
                            variant_data['godziny'] = json.loads(variant.godziny_odjazdu)
                        except:
                            variant_data['godziny'] = []
                    
                    variant_stops = (self.db.query(Przystanki_Warianty, Przystanki)
                                   .join(Przystanki, Przystanki_Warianty.id_przystanki == Przystanki.id)
                                   .filter(Przystanki_Warianty.id_warianty == variant.id)
                                   .order_by(Przystanki_Warianty.kolejnosc)
                                   .all())
                    
                    for variant_stop, stop in variant_stops:
                        stop_data = {
                            'nazwa': stop.nazwa,
                            'ulica': stop.ulica,
                            'kolejnosc': variant_stop.kolejnosc
                        }
                        variant_data['przystanki'].append(stop_data)
                    
                    route_data['warianty'].append(variant_data)
                
                line_data['trasy'].append(route_data)
            
            schedules.append(line_data)
        
        return schedules
    
    def generate_pdf(self, output_path: str) -> str:
        pdf = BusSchedulePDF()
        schedules = self.get_line_schedules()
        
        if not schedules:
            pdf.add_page()
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, 'Brak danych o rozkladach jazdy w systemie.', 0, 1, 'C')
            pdf.ln(10)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 8, 'Aby wygenerowac rozklad jazdy, dodaj:', 0, 1, 'L')
            pdf.cell(0, 6, '* Linie autobusowe', 0, 1, 'L')
            pdf.cell(0, 6, '* Trasy z przystankami', 0, 1, 'L')
            pdf.cell(0, 6, '* Warianty tras z godzinami odjazdu', 0, 1, 'L')
            pdf.output(output_path)
            return output_path
        
        for line in schedules:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(0, 10, f'Linia {line["numer"]} - {line["kierunek"]}', 1, 1, 'C', True)
            
            if line['opis']:
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(0, 8, line['opis'], 0, 1, 'C')
            
            pdf.ln(5)
            
            if not line['trasy']:
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 8, 'Brak przypisanych tras dla tej linii.', 0, 1, 'L')
                continue
            
            for route in line['trasy']:
                pdf.set_font('Arial', 'B', 12)
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(0, 8, f'Trasa: {route["nazwa"]}', 1, 1, 'L', True)
                
                if not route['warianty']:
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(0, 6, '  Brak wariantow dla tej trasy.', 0, 1, 'L')
                    pdf.ln(3)
                    continue
                
                for variant in route['warianty']:
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(0, 6, f'Wariant {variant["kod"]}: {variant["nazwa"]}', 0, 1, 'L')
                    
                    if variant['przystanki']:
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(40, 5, 'Przystanki:', 0, 0, 'L')
                        
                        stops_text = " > ".join([
                            f"{stop['nazwa']}" + (f" ({stop['ulica']})" if stop['ulica'] else "")
                            for stop in variant['przystanki']
                        ])
                        
                        self._print_wrapped_text(pdf, stops_text, 40, 150)
                    else:
                        pdf.set_font('Arial', 'I', 9)
                        pdf.cell(40, 5, 'Przystanki:', 0, 0, 'L')
                        pdf.cell(0, 5, 'Brak przypisanych przystankow', 0, 1, 'L')
                    
                    if variant['godziny']:
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(40, 5, 'Godziny odjazdu:', 0, 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        hours_text = " | ".join(variant['godziny'])
                        self._print_wrapped_text(pdf, hours_text, 40, 150)
                    else:
                        pdf.set_font('Arial', 'I', 9)
                        pdf.cell(40, 5, 'Godziny odjazdu:', 0, 0, 'L')
                        pdf.cell(0, 5, 'Brak godzin odjazdu', 0, 1, 'L')
                    
                    pdf.ln(3)
                
                pdf.ln(2)
        
        pdf.output(output_path)
        return output_path
    
    def _print_wrapped_text(self, pdf, text: str, indent: float, max_width: float):
        if pdf.get_string_width(text) <= max_width:
            pdf.cell(0, 5, text, 0, 1, 'L')
        else:
            words = text.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if pdf.get_string_width(test_line) <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            for i, line_text in enumerate(lines):
                if i == 0:
                    pdf.cell(0, 5, line_text, 0, 1, 'L')
                else:
                    pdf.cell(indent, 5, '', 0, 0, 'L')
                    pdf.cell(0, 5, line_text, 0, 1, 'L')

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.get("/rozklad")
async def download_schedule_pdf(db: Session = Depends(get_db)):
    try:
        generator = ScheduleGenerator(db)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            temp_path = tmp_file.name
        
        generator.generate_pdf(temp_path)
        
        if os.path.exists(temp_path):
            return FileResponse(
                path=temp_path,
                filename=f"rozklad_jazdy_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=rozklad_jazdy.pdf"}
            )
        else:
            raise HTTPException(status_code=500, detail="Blad podczas generowania PDF")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blad podczas generowania PDF: {str(e)}")

@router.get("/rozklad/preview")
async def preview_schedule_data(db: Session = Depends(get_db)):
    try:
        generator = ScheduleGenerator(db)
        schedules = generator.get_line_schedules()
        
        return {
            "status": "success",
            "count": len(schedules),
            "schedules": schedules
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blad podczas pobierania danych: {str(e)}")
