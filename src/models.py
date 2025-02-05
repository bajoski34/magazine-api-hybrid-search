from sqlalchemy import Column, Integer, String, ForeignKey, Date, TIMESTAMP, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class MagazineInfo(Base):
    __tablename__ = "magazine_info"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    publication_date = Column(Date, nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    contents = relationship("MagazineContent", back_populates="magazine")

class MagazineContent(Base):
    __tablename__ = "magazine_content"

    id = Column(Integer, primary_key=True, index=True)
    magazine_id = Column(Integer, ForeignKey("magazine_info.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    vector_representation = Column(String, nullable=True)  # Store vector as string/array
    created_at = Column(TIMESTAMP, server_default=func.now())

    magazine = relationship("MagazineInfo", back_populates="contents")
