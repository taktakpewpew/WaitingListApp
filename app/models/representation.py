from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base


class Representation(Base):
    __tablename__ = 'representations'

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey('events.id'), nullable=False)

    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=False)

    # Relation avec Event
    event = relationship("Event", back_populates="representations")
    inventory = relationship("Inventory", back_populates="representation", cascade="all, delete-orphan")
    waiting_list_entries = relationship('WaitingListEntry', back_populates='representation',
                                        cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Representation(id={self.id}, event_id={self.event_id}, start={self.start_datetime})>"
