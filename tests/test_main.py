import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database import async_session
from main import get_search_service, app
from unittest.mock import AsyncMock

SearchService = get_search_service()

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/magazine_db"

# Create a separate test database engine
test_engine = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="function")
async def test_db():
    """Fixture to create a new test database session"""
    async with TestSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
def test_client():
    """Fixture to provide a test client for FastAPI"""
    return TestClient(app)

@pytest.fixture(scope="function")
def mock_search_service():
    """Mock SearchService for testing"""
    mock_service = AsyncMock()
    mock_service.hybrid_search.return_value = [
        {
            "id": 1,
            "title": "AI and the Future",
            "author": "John Doe",
            "content": "Exploring AI advancements",
            "final_score": 0.95,
        }
    ]
    return mock_service

def test_health_check(test_client):
    """Test if the API is running"""
    response = test_client.get("/docs")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_search_endpoint(test_client, mock_search_service):
    """Test the search API"""
    app.dependency_overrides[SearchService] = lambda: mock_search_service  # Override dependency
    
    response = test_client.get("/api/v1/search?query=AI&limit=1")
    
    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "id": 1,
                "title": "AI and the Future",
                "author": "John Doe",
                "content": "Exploring AI advancements",
                "final_score": 0.95,
            }
        ]
    }

    app.dependency_overrides = {}  # Reset dependency overrides
