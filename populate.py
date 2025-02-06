import pandas as pd
from faker import Faker
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import numpy as np
from os import getenv
import asyncio

fake = Faker()
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create an async engine and sessionmaker
engine = create_async_engine(getenv('DATABASE_URL', "postgresql+asyncpg://postgres:password@db:5432/magazine_db"))
AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def generate_magazine_data(n_records: int):
    magazines = []
    contents = []
    
    categories = ['Technology', 'Science', 'Arts', 'Business', 'Sports']
    
    for i in range(n_records):
        # Generate magazine info
        magazine = {
            'id': i + 1,
            'title': fake.catch_phrase(),
            'author': fake.name(),
            'publication_date': fake.date_between(start_date='-5y'),
            'category': np.random.choice(categories)
        }
        magazines.append(magazine)
        
        # Generate content and vector representation
        content = fake.text(max_nb_chars=1000)
        vector = model.encode(content).tolist()  # Convert numpy array to list for storage
        
        content_record = {
            'id': i + 1,
            'magazine_id': i + 1,
            'content': content,
            'vector_representation': vector
        }
        contents.append(content_record)
    
    return pd.DataFrame(magazines), pd.DataFrame(contents)

async def store_data(magazines_df, contents_df):
    async with AsyncSessionMaker() as session:
        async with session.begin():
            # Insert magazines data
            for _, row in magazines_df.iterrows():
                await session.execute(
                    text("INSERT INTO magazine_info (id, title, author, publication_date, category) "
                         "VALUES (:id, :title, :author, :publication_date, :category)"),
                    {"id": row['id'], "title": row['title'], "author": row['author'], 
                     "publication_date": row['publication_date'], "category": row['category']}
                )
            
            # Insert contents data
            for _, row in contents_df.iterrows():
                await session.execute(
                    text("INSERT INTO magazine_content (id, magazine_id, content, vector_representation) "
                         "VALUES (:id, :magazine_id, :content, :vector_representation)"),
                    {"id": row['id'], "magazine_id": row['magazine_id'], "content": row['content'], 
                     "vector_representation": row['vector_representation']}
                )
        await session.commit()

async def main():
    # Generate 100 records (change to 1000000 or your preferred size in production)
    magazines_df, contents_df = await generate_magazine_data(100)
    
    # Store data asynchronously
    await store_data(magazines_df, contents_df)

    print("Data inserted into database successfully.")

# Run the async main function
if __name__ == '__main__':
    asyncio.run(main())
