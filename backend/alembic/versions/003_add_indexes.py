"""Add database indexes for better performance

Revision ID: 003_add_indexes
Revises: 002_procedures_triggers
Create Date: 2025-06-13 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '003_add_indexes'
down_revision = '002_procedures_triggers'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('idx_user_rola_user_id', 'User_Rola', ['id_user'])
    op.create_index('idx_user_rola_rola_id', 'User_Rola', ['id_rola'])
    
    op.create_index('idx_przystanki_warianty_przystanek', 'Przystanki_Warianty', ['id_przystanki'])
    op.create_index('idx_przystanki_warianty_wariant', 'Przystanki_Warianty', ['id_warianty'])
    op.create_index('idx_przystanki_warianty_kolejnosc', 'Przystanki_Warianty', ['kolejnosc'])
    
    op.create_index('idx_warianty_trasy_wariant', 'Warianty_Trasy', ['id_warianty'])
    op.create_index('idx_warianty_trasy_trasa', 'Warianty_Trasy', ['id_trasy'])
    
    op.create_index('idx_linie_trasy_linia', 'Linie_Trasy', ['id_linie'])
    op.create_index('idx_linie_trasy_trasa', 'Linie_Trasy', ['id_trasy'])
    
    op.create_index('idx_brygady_linie_brygada', 'Brygady_Linie', ['id_brygady'])
    op.create_index('idx_brygady_linie_linia', 'Brygady_Linie', ['id_linie'])
    
    op.create_index('idx_kierowcy_brygady_kierowca', 'Kierowcy_Brygady', ['id_kierowcy'])
    op.create_index('idx_kierowcy_brygady_brygada', 'Kierowcy_Brygady', ['id_brygady'])
    
    op.create_index('idx_brygady_autobusy_brygada', 'Brygady_Autobusy', ['id_brygady'])
    op.create_index('idx_brygady_autobusy_autobus', 'Brygady_Autobusy', ['id_autobusy'])
    
    op.create_index('idx_odjazdy_wariant', 'Odjazdy', ['id_warianty'])
    op.create_index('idx_odjazdy_przystanek', 'Odjazdy', ['id_przystanku'])
    op.create_index('idx_odjazdy_godzina', 'Odjazdy', ['godzina'])
    
    op.create_index('idx_linie_numer', 'Linie', ['numer'])
    op.create_index('idx_przystanki_nazwa', 'Przystanki', ['nazwa'])
    op.create_index('idx_autobusy_rejestracja', 'Autobusy', ['rejestracja'])
    op.create_index('idx_kierowcy_pesel', 'Kierowcy', ['pesel'])
    op.create_index('idx_kierowcy_nazwisko', 'Kierowcy', ['nazwisko'])
    op.create_index('idx_brygady_nazwa', 'Brygady', ['nazwa'])
    op.create_index('idx_warianty_kod', 'Warianty', ['kod_wariantu'])
    op.create_index('idx_users_username', 'Users', ['username'])
    
    op.create_index('idx_linie_trasy_composite', 'Linie_Trasy', ['id_linie', 'id_trasy'])
    op.create_index('idx_przystanki_warianty_composite', 'Przystanki_Warianty', ['id_warianty', 'kolejnosc'])


def downgrade():
    op.drop_index('idx_przystanki_warianty_composite', 'Przystanki_Warianty')
    op.drop_index('idx_linie_trasy_composite', 'Linie_Trasy')
    
    op.drop_index('idx_users_username', 'Users')
    op.drop_index('idx_warianty_kod', 'Warianty')
    op.drop_index('idx_brygady_nazwa', 'Brygady')
    op.drop_index('idx_kierowcy_nazwisko', 'Kierowcy')
    op.drop_index('idx_kierowcy_pesel', 'Kierowcy')
    op.drop_index('idx_autobusy_rejestracja', 'Autobusy')
    op.drop_index('idx_przystanki_nazwa', 'Przystanki')
    op.drop_index('idx_linie_numer', 'Linie')
    
    op.drop_index('idx_odjazdy_godzina', 'Odjazdy')
    op.drop_index('idx_odjazdy_przystanek', 'Odjazdy')
    op.drop_index('idx_odjazdy_wariant', 'Odjazdy')
    op.drop_index('idx_brygady_autobusy_autobus', 'Brygady_Autobusy')
    op.drop_index('idx_brygady_autobusy_brygada', 'Brygady_Autobusy')
    op.drop_index('idx_kierowcy_brygady_brygada', 'Kierowcy_Brygady')
    op.drop_index('idx_kierowcy_brygady_kierowca', 'Kierowcy_Brygady')
    op.drop_index('idx_brygady_linie_linia', 'Brygady_Linie')
    op.drop_index('idx_brygady_linie_brygada', 'Brygady_Linie')
    op.drop_index('idx_linie_trasy_trasa', 'Linie_Trasy')
    op.drop_index('idx_linie_trasy_linia', 'Linie_Trasy')
    op.drop_index('idx_warianty_trasy_trasa', 'Warianty_Trasy')
    op.drop_index('idx_warianty_trasy_wariant', 'Warianty_Trasy')
    op.drop_index('idx_przystanki_warianty_kolejnosc', 'Przystanki_Warianty')
    op.drop_index('idx_przystanki_warianty_wariant', 'Przystanki_Warianty')
    op.drop_index('idx_przystanki_warianty_przystanek', 'Przystanki_Warianty')
    op.drop_index('idx_user_rola_rola_id', 'User_Rola')
    op.drop_index('idx_user_rola_user_id', 'User_Rola')