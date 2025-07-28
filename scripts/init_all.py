from app.db.init_db import init_db
from app.db.load_csv_data import load_csv_to_db

if __name__ == "__main__":
    init_db()
    load_csv_to_db()