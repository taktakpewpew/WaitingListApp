from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base


class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(String, primary_key=True)
    offer_id = Column(String, ForeignKey('offers.offer_id'), nullable=False)
    representation_id = Column(String, ForeignKey('representations.id'), nullable=False)
    total_stock = Column(Integer, nullable=False)
    available_stock = Column(Integer, nullable=False)

    offer = relationship("Offer", back_populates="inventory")
    representation = relationship("Representation", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory(id={self.inventory_id}, offer_id={self.offer_id}, rep_id={self.representation_id})>"
