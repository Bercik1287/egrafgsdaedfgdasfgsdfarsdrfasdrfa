"""Add stored procedures and triggers

Revision ID: 002_procedures_triggers
Revises: 001_initial_tables
Create Date: 2025-06-13 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '002_procedures_triggers'
down_revision = '001_initial_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION update_autobus(
            p_id INT,
            p_rejestracja TEXT,
            p_marka TEXT,
            p_model TEXT
        )
        RETURNS VOID
        LANGUAGE plpgsql
        AS $$
        BEGIN
            UPDATE "Autobusy"
            SET
                rejestracja = COALESCE(p_rejestracja, rejestracja),
                marka = COALESCE(p_marka, marka),
                model = COALESCE(p_model, model)
            WHERE id = p_id;

            IF NOT FOUND THEN
                RAISE EXCEPTION 'Autobus nie zostal znaleziony';
            END IF;
        END;
        $$;
    """)
    
    op.execute("""
        CREATE OR REPLACE FUNCTION aktualizuj_date_brygady()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.zmieniono_dnia := now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
        CREATE TRIGGER trg_update_brygady_data
        BEFORE UPDATE ON "Brygady"
        FOR EACH ROW
        EXECUTE FUNCTION aktualizuj_date_brygady();
    """)
    
    op.execute("""
        CREATE OR REPLACE VIEW lines_for_routes_2 AS
        SELECT 
            lt.id_trasy as route_id,
            l.id as line_id,
            l.numer as line_number,
            l.kierunek as line_direction,
            l.opis as line_description,
            lt.id as assignment_id
        FROM "Linie_Trasy" lt
        JOIN "Linie" l ON lt.id_linie = l.id;
    """)


def downgrade():
    op.execute('DROP VIEW IF EXISTS lines_for_routes_2;')
    
    op.execute('DROP TRIGGER IF EXISTS trg_update_brygady_data ON "Brygady";')
    
    op.execute('DROP FUNCTION IF EXISTS aktualizuj_date_brygady();')
    op.execute('DROP FUNCTION IF EXISTS update_autobus(INT, TEXT, TEXT, TEXT);')