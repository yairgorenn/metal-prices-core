from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from .db import SessionLocal, engine
from .models import Base, MetalPrice
from .auth import require_ingest_token, require_client_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ingest/metal-price")
def ingest_price(
    metal: str,
    price_eur_per_ton: float,
    eur_to_ils: float,
    price_date: date,
    db: Session = Depends(get_db),
    _: None = Depends(require_ingest_token)
):
    price_ils_per_kg = round((price_eur_per_ton * eur_to_ils) / 1000, 6)

    row = (
        db.query(MetalPrice)
        .filter(MetalPrice.metal_code == metal)
        .one_or_none()
    )

    if row:
        # UPDATE
        row.price_eur_per_ton = price_eur_per_ton
        row.eur_to_ils = eur_to_ils
        row.price_ils_per_kg = price_ils_per_kg
        row.price_date = price_date
    else:
        # INSERT
        row = MetalPrice(
            metal_code=metal,
            price_eur_per_ton=price_eur_per_ton,
            eur_to_ils=eur_to_ils,
            price_ils_per_kg=price_ils_per_kg,
            price_date=price_date
        )
        db.add(row)

    db.commit()
    return {"status": "ok", "metal": metal}


@app.get("/prices/latest")
def get_latest_prices(
    db: Session = Depends(get_db),
    _: None = Depends(require_client_token)
):
    result = {}
    for metal in ["CU", "AL"]:
        row = (
            db.query(MetalPrice)
            .filter(MetalPrice.metal_code == metal)
            .order_by(MetalPrice.price_date.desc())
            .first()
        )
        if row:
            result[metal] = {
                "price_ils_per_kg": float(row.price_ils_per_kg),
                "price_date": row.price_date.isoformat()
            }

    return result
