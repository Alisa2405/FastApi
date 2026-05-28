from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Advertisement
from schemas import (
AdvertisementCreate,
AdvertisementUpdate,
AdvertisementResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/advertisement", response_model=AdvertisementResponse)
def create_advertisement(
ad: AdvertisementCreate,
db: Session = Depends(get_db),
):
advertisement = Advertisement(**ad.model_dump())

db.add(advertisement)
db.commit()
db.refresh(advertisement)

return advertisement

@app.get(
"/advertisement/{advertisement_id}",
response_model=AdvertisementResponse,
)
def get_advertisement(
advertisement_id: int,
db: Session = Depends(get_db),
):
advertisement = db.get(Advertisement, advertisement_id)

if advertisement is None:
    raise HTTPException(status_code=404, detail="Not found")

return advertisement

@app.patch(
"/advertisement/{advertisement_id}",
response_model=AdvertisementResponse,
)
def update_advertisement(
advertisement_id: int,
ad_data: AdvertisementUpdate,
db: Session = Depends(get_db),
):
advertisement = db.get(Advertisement, advertisement_id)

if advertisement is None:
    raise HTTPException(status_code=404, detail="Not found")

for field, value in ad_data.model_dump(exclude_unset=True).items():
    setattr(advertisement, field, value)

db.commit()
db.refresh(advertisement)

return advertisement

@app.delete("/advertisement/{advertisement_id}")
def delete_advertisement(
advertisement_id: int,
db: Session = Depends(get_db),
):
advertisement = db.get(Advertisement, advertisement_id)


if advertisement is None:
    raise HTTPException(status_code=404, detail="Not found")

db.delete(advertisement)
db.commit()

return {"status": "deleted"}

@app.get("/advertisement", response_model=list[AdvertisementResponse])
def search_advertisements(
title: Optional[str] = None,
author: Optional[str] = None,
min_price: Optional[int] = None,
max_price: Optional[int] = None,
db: Session = Depends(get_db),
):
query = db.query(Advertisement)

if title:
    query = query.filter(Advertisement.title.ilike(f"%{title}%"))

if author:
    query = query.filter(Advertisement.author.ilike(f"%{author}%"))

if min_price is not None:
    query = query.filter(Advertisement.price >= min_price)

if max_price is not None:
    query = query.filter(Advertisement.price <= max_price)

return query.all()

