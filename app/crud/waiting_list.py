from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.exceptions.inventory_exceptions import InventoryNotFound
from app.exceptions.offer_exceptions import OfferNotFound
from app.exceptions.representation_exceptions import RepresentationNotFound
from app.exceptions.waiting_list_exceptions import TicketsStillAvailable, AlreadyInWaitingList, WaitingListNotFound, \
    RepresentationEventAndOfferEventDontMatch
from app.models import Inventory, Representation, Offer, Event
from app.models.waiting_list import WaitingListEntry
from app.schemas.waiting_list import WaitingListCreate
from datetime import datetime, timezone


def create_waiting_list_entry(db: Session, data: WaitingListCreate) -> WaitingListEntry:
    """
        Checks whether all the specified entities (offer, representation, inventory) exists, if inventory has no stock
        if user is not already in waitinglist for this, if all these requirements are met; creates waitinglistentry.
    :param db: SQLAlchemy session
    :param data: contains offer_id, representation_id, user_id
    :return: newly created WaitingListEntry with its position in the queue.
    """
    representation = db.query(Representation).filter_by(id=data.representation_id).one_or_none()
    if not representation:
        raise RepresentationNotFound()

    offer = db.query(Offer).filter_by(offer_id=data.offer_id).one_or_none()
    if not offer:
        raise OfferNotFound()

    if offer.event_id != representation.event_id:
        raise RepresentationEventAndOfferEventDontMatch()


    inventory = db.query(Inventory).filter_by(offer_id=data.offer_id, representation_id=data.representation_id).one_or_none()
    if not inventory:
        raise InventoryNotFound()

    if inventory.available_stock > 0:
        raise TicketsStillAvailable()

    existing_waitinglist = db.query(WaitingListEntry).filter(
        WaitingListEntry.user_id == data.user_id,
        WaitingListEntry.representation_id == data.representation_id,
        WaitingListEntry.offer_id == data.offer_id
    ).one_or_none()

    if existing_waitinglist:
        raise AlreadyInWaitingList()

    entry = WaitingListEntry(**data.model_dump(), timestamp=datetime.now(timezone.utc))
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_position_for_waitinglist_entry(db: Session, entry: WaitingListEntry) -> int:
    """
    Returns position for current waitinglist entry
    :param db: SQLALchemy session
    :param entry: waitinglist entry
    :return: position of waiting list entry in the queue
    """
    return (db.query(WaitingListEntry).filter_by(offer_id=entry.offer_id, representation_id=entry.representation_id)
            .filter(WaitingListEntry.timestamp < entry.timestamp).count()) + 1


def get_user_waitinglist_entries(db: Session, user_id: int) -> list[WaitingListEntry]:
    """
    Returns all waitinglist entries for specified user.
    :param db: Session
    :param user_id: id of the user
    :return: waitinglist entries for specified user
    """
    return db.query(WaitingListEntry).filter_by(user_id=user_id).order_by(WaitingListEntry.timestamp.asc()).all()


def get_entry_by_id(db: Session, entry_id: int):
    existing = db.query(WaitingListEntry).filter_by(id=entry_id).one_or_none()
    if not existing:
        raise WaitingListNotFound()
    return existing


def delete_entry(db: Session, entry_id: int):
    """
    Deletes waitinglist entry matching entry_id
    :param db: SQLAlchemy session
    :param entry_id: id of the waiting list entry to be deleted
    :return: Nothing
    """
    entry = get_entry_by_id(db, entry_id)
    db.delete(entry)
    db.commit()


def get_entries_for_event_rep_offer(db: Session, event_id: Optional[str] = None, representation_id: Optional[str] = None, offer_id: Optional[str] = None):
    """
    Returns all waitinglist entries matching intersection of input filters
    :param db: SQLAlchemy session
    :param event_id: filter value for events
    :param representation_id: filter value for representation
    :param offer_id: filter value for offer
    :return: waitinglist entries matching intersection of input filters.
    """
    query = db.query(WaitingListEntry)
    if representation_id:
        query = query.filter(WaitingListEntry.representation_id == representation_id)

    if offer_id:
        query = query.filter(WaitingListEntry.offer_id == offer_id)

    if event_id:
        #we checked at insert for waitingList that representation.event_id = offer.event_id
        query = query.join(Representation).join(Event).filter(Event.id == event_id)

    return query.order_by(WaitingListEntry.timestamp.asc()).all()


def get_entries_with_position(db: Session, event_id: Optional[str] = None, representation_id: Optional[str] = None, offer_id: Optional[str] = None, user_id: Optional[int] = None):
    """
    Returns all waitinglist entries matching intersection of input filters
    :param db: SQLAlchemy session
    :param event_id: filter value for events
    :param representation_id: filter value for representation
    :param offer_id: filter value for offer
    :return: waitinglist entries matching intersection of input filters.
    """
    query = select(
        WaitingListEntry,
        func.row_number().over(
            partition_by=(WaitingListEntry.offer_id, WaitingListEntry.representation_id),
            order_by=WaitingListEntry.timestamp.asc()
        ).label("position")
    )

    if representation_id:
        query = query.filter(WaitingListEntry.representation_id == representation_id)

    if offer_id:
        query = query.filter(WaitingListEntry.offer_id == offer_id)

    if user_id:
        query = query.filter(WaitingListEntry.user_id == user_id)

    if event_id:
        #we checked at insert for waitingList that representation.event_id = offer.event_id
        query = query.join(Representation).join(Event).filter(Event.id == event_id)

    return db.execute(query).all()