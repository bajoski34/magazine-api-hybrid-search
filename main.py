from os import getenv
from models import MagazineInfo, MagazineContent, Base
from fastapi import FastAPI, Query, Depends, HTTPException, status
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@db:5432/magazine_db"))
Session = sessionmaker(bind=engine)

def main() -> None:
    Base.metadata.create_all(engine)
    with Session() as session:
        session.add(user)
        session.commit()
        print(session.query(User).all())

if __name__ == "__main__":
    main()