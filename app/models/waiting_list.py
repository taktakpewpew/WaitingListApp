from datetime import datetime

from sqlalchemy import UniqueConstraint, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base


class WaitingListEntry(Base):
    __tablename__ = 'waiting_list_entries'
    __table_args__ = (
        #A user can only be on the waiting list once per representation/offer combination
        UniqueConstraint('user_id', 'representation_id', 'offer_id', name='uq_user_rep_offer'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    representation_id = Column(String, ForeignKey('representations.id'), nullable=False)
    offer_id = Column(String, ForeignKey('offers.offer_id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='waiting_list_entries')
    representation = relationship('Representation', back_populates='waiting_list_entries')
    offer = relationship('Offer', back_populates='waiting_list_entries')

    def __repr__(self):
        return f"<WaitingListEntry user_id={self.user_id} rep_id={self.representation_id} offer_id={self.offer_id} qty={self.quantity}>"
