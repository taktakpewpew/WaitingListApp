from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    thumbnail_url = Column(String)
    organization_id = Column(String)
    venue_name = Column(String)
    venue_address = Column(String)
    timezone = Column(String)

    offers = relationship('Offer', back_populates='event')
    representations = relationship("Representation", back_populates="event", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title})>"
