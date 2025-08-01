from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud import waiting_list
from app.crud.user import create_user_if_not_exist
from app.db.session import get_db
from app.schemas import UserCreate, UserOut
from app.schemas.waiting_list import WaitingListOut
from app.services.waiting_list import compute_position_for_waitinglist_entries, format_position_for_waitinglist_entries

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates user for specified first_name, last_name and email.
    :param user: contains first_name, last_name and email
    :param db: SQLAlchemy session
    :return: UserOut, the created user.
    """
    return create_user_if_not_exist(db, user)

@router.get("/{user_id}/waiting-list", response_model=list[WaitingListOut])
def get_user_entries(user_id: int, db: Session = Depends(get_db)):
    """
    Gets all waitingList entries for specified user_id
    :param user_id:
    :param db:
    :return: list of WaitingListEntries associated to user_id
    """
    return format_position_for_waitinglist_entries(waiting_list.get_entries_with_position(db, user_id=user_id))