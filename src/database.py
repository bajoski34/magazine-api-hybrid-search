from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@db:5432/magazine_db")

async_engine = create_async_engine(DATABASE_URL, echo=True)  # Enable logs for debugging
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)