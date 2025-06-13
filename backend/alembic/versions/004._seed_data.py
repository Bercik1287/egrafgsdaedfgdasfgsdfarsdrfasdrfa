"""Seed initial data

Revision ID: 004_seed_data
Revises: 003_add_indexes
Create Date: 2025-06-13 10:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer
import bcrypt

revision = '004_seed_data'
down_revision = '003_add_indexes'
branch_labels = None
depends_on = None


def upgrade():
    rola_table = table('Rola',
        column('id', Integer),
        column('nazwa', String)
    )
    
    users_table = table('Users',
        column('id', Integer),
        column('username', String),
        column('password', String)
    )
    
    user_rola_table = table('User_Rola',
        column('id', Integer),
        column('id_user', Integer),
        column('id_rola', Integer)
    )
    
    op.bulk_insert(rola_table, [
        {'id': 1, 'nazwa': 'Administrator'},
        {'id': 2, 'nazwa': 'Operator'},
        {'id': 3, 'nazwa': 'Kierowca'},
        {'id': 4, 'nazwa': 'Dyspozytor'}
    ])
    
    hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    op.bulk_insert(users_table, [
        {'id': 1, 'username': 'admin', 'password': hashed_password}
    ])
    
    op.bulk_insert(user_rola_table, [
        {'id': 1, 'id_user': 1, 'id_rola': 1}
    ])
    
    przystanki_table = table('Przystanki',
        column('id', Integer),
        column('nazwa', String),
        column('longi', sa.Float),
        column('lati', sa.Float),
        column('ulica', String)
    )
    
    op.bulk_insert(przystanki_table, [
        {'id': 1, 'nazwa': 'Dworzec Główny', 'longi': 21.012229, 'lati': 52.229676, 'ulica': 'Lubelska'},
        {'id': 2, 'nazwa': 'Plac Zamkowy', 'longi': 21.013863, 'lati': 52.247876, 'ulica': 'Krakowskie Przedmieście'},
        {'id': 3, 'nazwa': 'Politechnika', 'longi': 21.006693, 'lati': 52.219947, 'ulica': 'Nadbystrzycka'},
        {'id': 4, 'nazwa': 'Centrum Handlowe', 'longi': 21.025000, 'lati': 52.235000, 'ulica': 'Aleje Racławickie'},
        {'id': 5, 'nazwa': 'Szpital', 'longi': 21.015000, 'lati': 52.240000, 'ulica': 'Staszica'}
    ])
    
    linie_table = table('Linie',
        column('id', Integer),
        column('numer', String),
        column('kierunek', String),
        column('opis', String)
    )
    
    op.bulk_insert(linie_table, [
        {'id': 1, 'numer': '1', 'kierunek': 'Dworzec - Politechnika', 'opis': 'Linia łącząca dworzec z uczelnią'},
        {'id': 2, 'numer': '2', 'kierunek': 'Centrum - Szpital', 'opis': 'Linia komunikacji miejskiej'},
        {'id': 3, 'numer': '10', 'kierunek': 'Okrężna', 'opis': 'Linia okrężna przez centrum miasta'}
    ])
    
    brygady_table = table('Brygady',
        column('id', Integer),
        column('nazwa', String)
    )
    
    op.bulk_insert(brygady_table, [
        {'id': 1, 'nazwa': 'Brygada A'},
        {'id': 2, 'nazwa': 'Brygada B'},
        {'id': 3, 'nazwa': 'Brygada C'}
    ])
    
    op.execute("SELECT setval('\"Rola_id_seq\"', (SELECT MAX(id) FROM \"Rola\"));")
    op.execute("SELECT setval('\"Users_id_seq\"', (SELECT MAX(id) FROM \"Users\"));")
    op.execute("SELECT setval('\"User_Rola_id_seq\"', (SELECT MAX(id) FROM \"User_Rola\"));")
    op.execute("SELECT setval('\"Przystanki_id_seq\"', (SELECT MAX(id) FROM \"Przystanki\"));")
    op.execute("SELECT setval('\"Linie_id_seq\"', (SELECT MAX(id) FROM \"Linie\"));")
    op.execute("SELECT setval('\"Brygady_id_seq\"', (SELECT MAX(id) FROM \"Brygady\"));")


def downgrade():
    op.execute('DELETE FROM "User_Rola" WHERE id <= 1;')
    op.execute('DELETE FROM "Users" WHERE id <= 1;')
    op.execute('DELETE FROM "Rola" WHERE id <= 4;')
    op.execute('DELETE FROM "Przystanki" WHERE id <= 5;')
    op.execute('DELETE FROM "Linie" WHERE id <= 3;')
    op.execute('DELETE FROM "Brygady" WHERE id <= 3;')
    
    op.execute("SELECT setval('\"Rola_id_seq\"', 1, false);")
    op.execute("SELECT setval('\"Users_id_seq\"', 1, false);")
    op.execute("SELECT setval('\"User_Rola_id_seq\"', 1, false);")
    op.execute("SELECT setval('\"Przystanki_id_seq\"', 1, false);")
    op.execute("SELECT setval('\"Linie_id_seq\"', 1, false);")
    op.execute("SELECT setval('\"Brygady_id_seq\"', 1, false);")