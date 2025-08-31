from sqlalchemy import Column, String, Integer, DateTime, PrimaryKeyConstraint, desc, extract
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FileProgress(Base):
    __tablename__ = "file_progress"

    file_path = Column(String, index=True)
    extracted_from = Column(String, index=True)
    last_line_read = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("file_path", "extracted_from"),
    )

    def save(self, session):
        session.add(self)
        session.commit()
    

    @classmethod
    def get_monthly_usage(cls, session, source: str) -> int:
        """
        Calculate how many requests have been processed in the current month
        for a given data source (e.g. "IpQualityScore").
        
        The calculation is based on:
        - Summing the `last_line_read` values
        - Filtering only records from the current year and current month
        - Filtering only records belonging to the given `source`
        
        This is useful to enforce monthly API request limits.
        """
        now = datetime.utcnow()

        total = (
            session.query(func.sum(FileProgress.last_line_read))
            .filter(FileProgress.extracted_from == source)
            .filter(extract("year", FileProgress.time_updated) == now.year)
            .filter(extract("month", FileProgress.time_updated) == now.month)
            .scalar()
        )
        return total or 0