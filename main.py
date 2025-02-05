from fastapi import FastAPI, Query
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Optional

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

class SearchService:
    def __init__(self):
        self.engine = create_engine('postgresql://user:password@localhost/magazine_db')
        
    async def hybrid_search(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10
    ):
        # Generate vector embedding for the query
        query_vector = model.encode(query)
        
        # Combine keyword and vector search
        sql_query = """
        WITH keyword_matches AS (
            SELECT 
                mi.id,
                mi.title,
                mi.author,
                mc.content,
                ts_rank(
                    to_tsvector('english', mi.title || ' ' || mi.author || ' ' || mc.content),
                    plainto_tsquery('english', :query)
                ) as keyword_score,
                1 - (mc.vector_representation <-> :query_vector) as vector_score
            FROM magazine_info mi
            JOIN magazine_content mc ON mi.id = mc.magazine_id
            WHERE 
                to_tsvector('english', mi.title || ' ' || mi.author || ' ' || mc.content) @@ 
                plainto_tsquery('english', :query)
                AND (:category IS NULL OR mi.category = :category)
        )
        SELECT 
            id, 
            title, 
            author, 
            content,
            (keyword_score * 0.3 + vector_score * 0.7) as final_score
        FROM keyword_matches
        ORDER BY final_score DESC
        LIMIT :limit
        """
        
        results = await self.engine.execute(
            sql_query,
            query=query,
            query_vector=query_vector,
            category=category,
            limit=limit
        )
        
        return results.fetchall()

search_service = SearchService()

@app.get("/api/v1/search")
async def search(
    query: str = Query(..., min_length=1),
    category: Optional[str] = None,
    limit: int = Query(default=10, le=100)
):
    results = await search_service.hybrid_search(query, category, limit)
    return {"results": results}