from sqlalchemy import Column, String, Integer, DateTime, PrimaryKeyConstraint, desc, extract
from sqlalchemy.sql import func
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from database.database import Base
from datetime import datetime

class LastBatchNumber(Base):
    __tablename__ = "last_batch_number"

    model_name = Column(String, index=True, primary_key=True)
    last_batch_number_extracted = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    def save(self, session):
        session.add(self)
        session.commit()

    @classmethod
    def find_or_create(cls, session, model_name: str):
        instance = session.query(cls).filter_by(model_name=model_name).one_or_none()
        if instance is None:
            instance = cls(model_name=model_name, last_batch_number_extracted=0)
            session.add(instance)
        return instance

    @classmethod
    def get_last_number_batch(cls, session, model_name: str) -> int:
        """
        """
        actual_batch_number = session.execute (
            select(cls.last_batch_number_extracted).where(cls.model_name == model_name)
        ).scalar_one_or_none()

        return actual_batch_number if actual_batch_number is not None else 0
    

        