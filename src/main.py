from fastapi import FastAPI, Query, Depends, HttpException, status
from database import async_session
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from typing import Optional

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

class SearchService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def hybrid_search(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10
    ):
        # Generate vector embedding for the query
        query_vector = model.encode(query).tolist()  # Convert NumPy array to list
        
        # SQL Query (Using Hybrid Search: Full-Text + Vector Similarity)
        sql_query = text("""
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
        """)
        
        async with self.session.begin():  # Use Async Session
            results = await self.session.execute(
                sql_query.bindparams(
                    query=query,
                    query_vector=query_vector,  # Correct vector format
                    category=category,
                    limit=limit
                )
            )
            return results.fetchall()

async def get_search_service(session: AsyncSession = Depends(async_session)):
    return SearchService(session)

@app.get("/api/v1/search")
async def search(
    query: str = Query(..., min_length=1),
    category: Optional[str] = None,
    limit: int = Query(default=10, le=100),
    search_service: SearchService = Depends(get_search_service)
):
    try:
        # Attempt to perform the hybrid search
        results = await search_service.hybrid_search(query, category, limit)
        return {"results": [dict(row) for row in results]}
    
    except ValueError as ve:
        # Catch value errors (e.g., invalid input for search)
        logger.error(f"ValueError: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    
    except ConnectionError as ce:
        # Catch database connection errors
        logger.error(f"ConnectionError: {str(ce)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to the database. Please try again later."
        )
    
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )
