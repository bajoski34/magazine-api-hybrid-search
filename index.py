from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import asyncpg

import logging

logging.basicConfig(filename='app.log',level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

async def get_embedding(text):
    return model.encode(text)

async def store_document(title, content):
    embedding = await get_embedding([content])
    conn = await asyncpg.connect("postgresql+asyncpg://postgres:password@magazine_db:5432/magazine_db")
    await conn.execute(
        "INSERT INTO documents (title, content, embedding) VALUES ($1, $2, $3)",
        title, content, embedding
    )
    await conn.close()

async def hybrid_search(query_text):
    embedding = await get_embedding(query_text)
    logging.info(f" { embedding}")
    conn = await asyncpg.connect("postgresql+asyncpg://postgres:password@magazine_db:5432/magazine_db")
    results = await conn.fetch(
        """SELECT id, title, content
           FROM documents
           WHERE to_tsvector(content) @@ to_tsquery($1)
           ORDER BY embedding <-> $2
           LIMIT 10""",
        query_text, embedding
    )
    await conn.close()
    return results

@app.get("/search/")
async def search(query: str):
    print(query)
    results = await hybrid_search(query)
    return {"results": results}