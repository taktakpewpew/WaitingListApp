import app.models
from app.db.session import engine, Base

def init_db():
    """Creates tables for model."""
    Base.metadata.create_all(bind=engine)