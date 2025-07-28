from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    waiting_list_entries = relationship('WaitingListEntry', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(user_id={self.id}, name={self.first_name} {self.last_name}, email={self.email})>"
