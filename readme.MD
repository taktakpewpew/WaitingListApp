## Architecture:
This project was written in python3.12, using POSTGRESQL, FASTAPI and SQLAlchemy.

Clone the repository:
```bash
    git clone <url_repository>
    cd WaitingListProject
```

Install python 3.12 (use Homebrew for macos):
```bash
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt install python3.12 python3.12-venv python3.12-dev -y
```

Create a venv for python 3.12 and activate it
```bash
  python3.12 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
```

To test, you will need to install postgres locally:

```bash
    sudo apt install postgresql postgresql-contrib
```

And run this list of shell command to create database/user/password, once for production env, once for test env

```code
  sudo -u postgres psql -c "CREATE DATABASE <db_name>;"
  sudo -u postgres psql -c "CREATE USER <user_name> WITH PASSWORD '<user_password>';"
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <user_name>;"
  sudo -u postgres psql -d <db_name> -c "GRANT CREATE ON SCHEMA public TO <user_name>;"
  sudo -u postgres psql -d <db_name> -c "GRANT USAGE ON SCHEMA public TO <user_name>;"
  sudo -u postgres psql -d <db_name> -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO <user_name>;"
```

Then update your .env and .env.test as follow

```code
  DATABASE_URL=postgresql://<user_name>:<user_password>@localhost/<db_name>
```

Run setup script to load CSV data in Postgresql database
```bash
  python -m scripts.init_all
```


Run the server locally using
```bash
  uvicorn app.main:app --reload
```

You can test manually the server using postman or CURL:

- creating USER
```bash
    curl -X POST http://localhost:8000/users/ \
     -H "Content-Type: application/json" \
     -d '{"first_name":"Maelle", "last_name":"Dessendre", "email": "maelle.dessendre@gmail.com"}'
```

- adding USER to waitingList
```bash
    curl -X POST http://localhost:8000/waiting-list/join \
     -H "Content-Type: application/json" \
     -d '{"user_id":"1", "representation_id":"rep_002", "offer_id": "off_001", "quantity": 5}'
```


Run the tests using 
```bash
  pytest
```


## Notes & Asumptions on Business Rules

- **The waiting list is activated for a given representation/offer combination only when the offer is sold out for the given representation** - Simple check before waitingListEntry creation on related Inventory's available stock
- **Users are added to the waiting list in chronological order** - As Notification is not part of this, a simple insertion timestamp on waiting list should be enough to keep track of order.
- **Users can specify the quantity of tickets they want to join the waiting list for** - quantity field on WaitingListEntry
- **A user can only be on the waiting list once per representation/offer combination** - unique constraint in model + check before insert; should maybe materialize the constraint in DB


## Documentation

Visit swagger at:
```bash
    http://127.0.0.1:8000/docs
```


## Possible improvements

- **include Alembic** for migrations management
- **include linter**
- **include proper CICD pipeline** : lint/ tests/ sonarcloud/ deploy
- **more tests**
- **more typing**
- **more docs**
- **add traduction for error messages** : use translation dicts