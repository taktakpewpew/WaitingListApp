from sqlalchemy.orm import Session

from app.crud.waiting_list import get_position_for_waitinglist_entry
from app.models import WaitingListEntry
from app.schemas import WaitingListOut

def compute_position_for_waitinglist_entry(db: Session, entry: WaitingListEntry):
    """
    Computes its position and update WaitingListEntry ouput model with it.
    :param db: SQLAlchemy session
    :param entry: WaitingListEntry model to be patched with position
    :return: updated model.
    """
    return WaitingListOut.model_validate(entry, from_attributes=True).model_copy(update={"position": get_position_for_waitinglist_entry(db, entry)})

def compute_position_for_waitinglist_entries(db: Session, entries: list[WaitingListEntry]) -> list[WaitingListOut]:
    """Computes position for list of Waitinglist entries."""
    return [compute_position_for_waitinglist_entry(db, e) for e in entries]