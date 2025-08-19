from sqlalchemy import Column, String, Integer, DateTime, PrimaryKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileProgress(Base):
    __tablename__ = "file_progress"

    file_path = Column(String, index=True)
    extracted_from = Column(String, index=True)
    last_line_read = Column(Integer, default=0)
    last_batch_number_extracted = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("file_path", "extracted_from"),
    )

    def save(self, session):
        session.add(self)
        session.commit()
