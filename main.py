from os import getenv
from models import MagazineInfo, MagazineContent, Base
from fastapi import FastAPI, Query, Depends, HTTPException, status
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db = create_engine(getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@db:5432/magazine_db"))
Session = sessionmaker(bind=db)

def main() -> None:
    print("Hello from magazine-api-hybrid-search!")

if __name__ == "__main__":
    main()
