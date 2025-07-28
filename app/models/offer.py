from sqlalchemy import Column, String, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Offer(Base):
    __tablename__ = 'offers'

    offer_id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey('events.id'), nullable=False)

    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    max_quantity_per_order = Column(Integer, nullable=False)
    description = Column(Text)

    event = relationship("Event", back_populates="offers")
    inventory = relationship("Inventory", back_populates="offer", cascade="all, delete-orphan")
    waiting_list_entries = relationship('WaitingListEntry', back_populates='offer', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Offer(offer_id={self.offer_id}, name={self.name}, event_id={self.event_id})>"
