from app.core.database import Base, engine
from app.db.models import user, system

def create_tables():
    Base.metadata.create_all(bind=engine)