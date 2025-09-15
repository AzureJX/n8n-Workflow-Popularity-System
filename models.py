from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    workflow = Column(String, nullable=False, index=True)
    platform = Column(String, nullable=False, index=True)  # YouTube / Forum / Google
    country = Column(String, nullable=False, index=True)   # US / India
    # store raw metrics in a JSON-like structure (sqlite: TEXT)
    popularity_metrics = Column(JSON, nullable=True)