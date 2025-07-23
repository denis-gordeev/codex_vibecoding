from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Nendoroid(Base):
    __tablename__ = 'nendoroids'

    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    announcement_date = Column(Date)
    release_date = Column(Date)
    fandom = Column(String)
    season = Column(String)
    images = Column(JSONB)
    product_url = Column(String)
