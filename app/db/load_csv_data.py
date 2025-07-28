import pandas as pd
from sqlalchemy import text

from app.db.session import engine
from app.config import settings

def load_csv_to_db():
    """Loads input CSV from data folder."""
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE inventory, representations, offers, events CASCADE"))
        for entity in ['events', 'offers', 'representations', 'inventory']:
            df = pd.read_csv(settings.DATA_PATH / f"{entity}.csv")
            df.to_sql(entity, con=conn, if_exists='append', index=False)