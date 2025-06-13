"""Initial migration - create all tables

Revision ID: 001_initial_tables
Revises: 
Create Date: 2025-06-13 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=250), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Rola',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nazwa', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('User_Rola',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_user', sa.Integer(), nullable=True),
        sa.Column('id_rola', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_rola'], ['Rola.id'], ),
        sa.ForeignKeyConstraint(['id_user'], ['Users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Przystanki',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nazwa', sa.String(length=50), nullable=True),
        sa.Column('longi', sa.Double(), nullable=True),
        sa.Column('lati', sa.Double(), nullable=True),
        sa.Column('ulica', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nazwa')
    )
    
    op.create_table('Warianty',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nazwa', sa.String(length=50), nullable=True),
        sa.Column('kod_wariantu', sa.String(length=5), nullable=True),
        sa.Column('godziny_odjazdu', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Przystanki_Warianty',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_przystanki', sa.Integer(), nullable=True),
        sa.Column('id_warianty', sa.Integer(), nullable=True),
        sa.Column('kolejnosc', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_przystanki'], ['Przystanki.id'], ),
        sa.ForeignKeyConstraint(['id_warianty'], ['Warianty.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Trasy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nazwa', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Warianty_Trasy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_warianty', sa.Integer(), nullable=True),
        sa.Column('id_trasy', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_trasy'], ['Trasy.id'], ),
        sa.ForeignKeyConstraint(['id_warianty'], ['Warianty.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Linie',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numer', sa.String(length=25), nullable=True),
        sa.Column('kierunek', sa.String(length=50), nullable=True),
        sa.Column('opis', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numer')
    )
    
    op.create_table('Linie_Trasy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_linie', sa.Integer(), nullable=True),
        sa.Column('id_trasy', sa.Integer(), nullable=True),
        sa.Column('numer_linii', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id_linie'], ['Linie.id'], ),
        sa.ForeignKeyConstraint(['id_trasy'], ['Trasy.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Brygady',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nazwa', sa.String(length=25), nullable=True),
        sa.Column('zmieniono_dnia', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nazwa')
    )
    
    op.create_table('Brygady_Linie',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_brygady', sa.Integer(), nullable=True),
        sa.Column('id_linie', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_brygady'], ['Brygady.id'], ),
        sa.ForeignKeyConstraint(['id_linie'], ['Linie.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Kierowcy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('imie', sa.String(length=30), nullable=True),
        sa.Column('nazwisko', sa.String(length=30), nullable=True),
        sa.Column('pesel', sa.String(length=11), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pesel')
    )
    
    op.create_table('Kierowcy_Brygady',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_kierowcy', sa.Integer(), nullable=True),
        sa.Column('id_brygady', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_brygady'], ['Brygady.id'], ),
        sa.ForeignKeyConstraint(['id_kierowcy'], ['Kierowcy.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Autobusy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rejestracja', sa.String(length=7), nullable=True),
        sa.Column('marka', sa.String(length=25), nullable=True),
        sa.Column('model', sa.String(length=25), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('rejestracja')
    )
    
    op.create_table('Brygady_Autobusy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_brygady', sa.Integer(), nullable=True),
        sa.Column('id_autobusy', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_autobusy'], ['Autobusy.id'], ),
        sa.ForeignKeyConstraint(['id_brygady'], ['Brygady.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('Odjazdy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_warianty', sa.Integer(), nullable=True),
        sa.Column('id_przystanku', sa.Integer(), nullable=True),
        sa.Column('godzina', sa.Time(), nullable=True),
        sa.ForeignKeyConstraint(['id_przystanku'], ['Przystanki.id'], ),
        sa.ForeignKeyConstraint(['id_warianty'], ['Warianty.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Odjazdy')
    op.drop_table('Brygady_Autobusy')
    op.drop_table('Autobusy')
    op.drop_table('Kierowcy_Brygady')
    op.drop_table('Kierowcy')
    op.drop_table('Brygady_Linie')
    op.drop_table('Brygady')
    op.drop_table('Linie_Trasy')
    op.drop_table('Linie')
    op.drop_table('Warianty_Trasy')
    op.drop_table('Trasy')
    op.drop_table('Przystanki_Warianty')
    op.drop_table('Warianty')
    op.drop_table('Przystanki')
    op.drop_table('User_Rola')
    op.drop_table('Rola')
    op.drop_table('Users')