from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import get_session
from .models import Base, Nendoroid

app = FastAPI(title="Nendoroid Viewer API")

@app.on_event("startup")
async def on_startup():
    # create tables if they don't exist
    async with get_session() as session:
        await session.run_sync(Base.metadata.create_all)

@app.get("/nendoroids")
async def list_nendoroids(fandom: str | None = None, season: str | None = None, session: AsyncSession = Depends(get_session)):
    query = select(Nendoroid)
    if fandom:
        query = query.where(Nendoroid.fandom == fandom)
    if season:
        query = query.where(Nendoroid.season == season)
    result = await session.execute(query)
    return [n._asdict() if hasattr(n, '_asdict') else {
        'id': n.id, 'product_id': n.product_id, 'name': n.name,
        'fandom': n.fandom, 'season': n.season, 'release_date': n.release_date
    } for n in result.scalars().all()]
