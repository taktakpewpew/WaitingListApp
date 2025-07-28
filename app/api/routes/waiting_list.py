from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import WaitingListCreate, WaitingListOut
from app.crud import waiting_list
from app.services.waiting_list import compute_position_for_waitinglist_entries, compute_position_for_waitinglist_entry

router = APIRouter()


@router.post("/join", response_model=WaitingListOut, status_code=status.HTTP_201_CREATED)
def join_waiting_list(data: WaitingListCreate, db: Session = Depends(get_db)):
    """
    Creates waiting list entry for combination of user/offer/representation

    :param data: contains user_id, offer_id, representation_id and quantity
    :param db: SQLAlchemy session
    :return: WaitingListOut, the created waiting list entry with computed position in queue.
    """
    return compute_position_for_waitinglist_entry(db, waiting_list.create_waiting_list_entry(db, data))

@router.get("/{entry_id}/", response_model=WaitingListOut)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Get WaitingListEntry for input entry_id if exists.
    :param entry_id: id of the WaitingListEntry
    :param db: SQLAlchemy session
    :return: WaitingListOut, the requested waiting list entry with computed position in queue.
    """
    return compute_position_for_waitinglist_entry(db, waiting_list.get_entry_by_id(db, entry_id))

@router.delete("/{entry_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Deletes specified WaitingListEntry if exists.
    :param entry_id: id of the WaitingListEntry
    :param db: SQLAlchemy session
    :return: No Content
    """
    waiting_list.delete_entry(db, entry_id)

@router.get("/organizer/view/", response_model=list[WaitingListOut])
def organizer_view(event_id: Optional[str] = Query(None), representation_id: Optional[str] = Query(None), offer_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """
    Gets all WaitingListEntry matching input query filters.
    :param event_id: optional filter for event
    :param representation_id: optional filter for representation
    :param offer_id: optional filter for offer
    :param db: SQLAlchemy session
    :return: list of WaitingListOut including positions in the queue.
    """
    return compute_position_for_waitinglist_entries(db, waiting_list.get_entries_for_event_rep_offer(db=db, event_id=event_id, representation_id=representation_id, offer_id=offer_id))