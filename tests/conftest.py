from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import Base, get_db
from app.main import app
from app.models import User, Offer, Event, Representation, Inventory

from app.config import Settings

class TestSettings(Settings):
    class Config:
        env_file = ".env.test"

test_settings = TestSettings()
test_engine = create_engine(test_settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def test_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=test_engine)
    test_session = TestingSessionLocal()
    try:
        yield test_session
    finally:
        test_session.rollback()
        test_session.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client(test_session):
    def override_get_db():
        yield test_session

    #dependency_override (see FASTAPI docs)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_session):
    user = User(first_name="Jean-michel", last_name="Apeupré", email="jeanmich@gmail.com")
    test_session.add(user)
    test_session.commit()
    return user

@pytest.fixture()
def test_setup_without_inventory(test_session):
    event = Event(id="evt_001", title="Concert Test")
    test_session.add(event)

    representation = Representation(id="rep_001", event_id=event.id, start_datetime="2025-08-01 20:00:00", end_datetime="2025-08-01 23:00:00")
    test_session.add(representation)

    offer = Offer(offer_id="off_001", name="test_offer", event_id=event.id, type="ticket", max_quantity_per_order=500)
    test_session.add(offer)

    test_session.commit()

    return {
        "event": event,
        "representation": representation,
        "offer": offer,
    }

@pytest.fixture(params=[(0, "stock_empty"), (500, "stock_available")], ids=["stock_empty", "stock_available"])
def test_inventory(test_session, test_setup_without_inventory, request):
    inv = Inventory(
        inventory_id=f"inv_{request.param[0]}",
        offer_id=test_setup_without_inventory['offer'].offer_id,
        representation_id=test_setup_without_inventory['representation'].id,
        total_stock=1000,
        available_stock=request.param[0]
    )
    test_session.add(inv)
    test_session.commit()
    return inv