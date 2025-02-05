import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from main import app, search_service

@pytest.fixture
def mock_search_service():
    """Mock the hybrid_search method of SearchService."""
    search_service.hybrid_search = AsyncMock(return_value=[
        (1, "AI in Healthcare", "John Doe", "AI is revolutionizing healthcare...", 0.95),
        (2, "Machine Learning Trends", "Jane Smith", "Latest trends in ML for 2025...", 0.89),
    ])
    return search_service

@pytest.mark.asyncio
async def test_search_success(mock_search_service):
    """Test search endpoint with a valid query."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/search", params={"query": "AI", "limit": 2})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "results" in data
    assert len(data["results"]) == 2
    assert data["results"][0][1] == "AI in Healthcare"
    assert data["results"][1][1] == "Machine Learning Trends"

@pytest.mark.asyncio
async def test_search_no_results(mock_search_service):
    """Test search endpoint when no results are found."""
    search_service.hybrid_search.return_value = []  # Simulate empty result

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/search", params={"query": "Quantum Computing"})

    assert response.status_code == 200
    data = response.json()
    assert data["results"] == []

@pytest.mark.asyncio
async def test_search_invalid_query():
    """Test search with an invalid query (empty string)."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/search", params={"query": ""})
    
    assert response.status_code == 422  # FastAPI validates min_length=1

@pytest.mark.asyncio
async def test_search_limit_exceeds():
    """Test search with limit exceeding the maximum allowed."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/search", params={"query": "AI", "limit": 150})
    
    assert response.status_code == 422  # FastAPI enforces limit <= 100
