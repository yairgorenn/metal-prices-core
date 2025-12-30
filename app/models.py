from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func

from app.db import Base

class MetalPrice(Base):
    __tablename__ = "metal_prices"

    id = Column(Integer, primary_key=True)
    metal_code = Column(String, nullable=False)  # CU / AL
    price_eur_per_ton = Column(Numeric(10,4), nullable=False)
    eur_to_ils = Column(Numeric(10,6), nullable=False)
    price_ils_per_kg = Column(Numeric(10,6), nullable=False)
    price_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

