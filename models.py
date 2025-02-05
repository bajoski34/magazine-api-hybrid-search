from sqlalchemy.orm import (
    declarative_base, Mapped, mapped_column, relationship
)
from sqlalchemy import Integer, String, ForeignKey, Date, TIMESTAMP, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
import numpy as np

Base = declarative_base()

class MagazineInfo(Base):
    __tablename__ = "magazine_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_date: Mapped[Date] = mapped_column(Date, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())

    contents = relationship("MagazineContent", back_populates="magazine", cascade="all, delete-orphan")

class MagazineContent(Base):
    __tablename__ = "magazine_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    magazine_id: Mapped[int] = mapped_column(Integer, ForeignKey("magazine_info.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    vector_representation: Mapped[list[float]] = mapped_column(ARRAY(FLOAT), nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())

    magazine = relationship("MagazineInfo", back_populates="contents")

    def __init__(self, magazine_id: int, content: str, vector_representation: np.ndarray = None):
        self.magazine_id = magazine_id
        self.content = content
        self.set_vector(vector_representation)

    def set_vector(self, vector_array: np.ndarray):
        """Converts a numpy array to a list of floats for direct PostgreSQL storage."""
        self.vector_representation = vector_array.tolist() if vector_array is not None else None

    def get_vector(self) -> np.ndarray:
        """Converts the stored list back to a NumPy array."""
        return np.array(self.vector_representation, dtype=np.float32) if self.vector_representation else None
