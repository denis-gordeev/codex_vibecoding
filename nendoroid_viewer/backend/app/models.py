from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Nendoroid(Base):
    __tablename__ = 'nendoroids'

    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    fandom = Column(String)
    season = Column(String)
    release_date = Column(Date)
