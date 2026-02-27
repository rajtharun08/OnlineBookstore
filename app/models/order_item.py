import uuid
from sqlalchemy import Column, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Keys
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    
    # Item Details
    quantity = Column(Integer, nullable=False, default=1)
    price_at_purchase = Column(Float, nullable=False) # Snapshot of price at time of order

    # Relationships
    order = relationship("Order", back_populates="items")
    book = relationship("Book")