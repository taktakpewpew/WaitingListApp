from sqlalchemy.orm import Session

from app.exceptions.user_exceptions import UserAlreadyExists
from app.models import User
from app.schemas import UserCreate


def create_user_if_not_exist(db: Session, data: UserCreate) -> User:
    """
    Creates specified user if email not already in use.
    :param db: SQLALchemy session
    :param data: first_name, last_name and email
    :return: newly created user.
    """
    email_check = db.query(User).filter_by(email=data.email).one_or_none()
    if email_check:
        raise UserAlreadyExists()
    new_user = User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user