# Magazine Search API.

## Requirements

1. UV - Package manager

## Database Design

```sql
-- Magazine Information Table
CREATE TABLE magazine_info (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publication_date DATE NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Magazine Content Table
CREATE TABLE magazine_content (
    id SERIAL PRIMARY KEY,
    magazine_id INTEGER REFERENCES magazine_info(id),
    content TEXT NOT NULL,
    vector_representation vector(384), -- Assuming using BERT embeddings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_magazine_title ON magazine_info(title);
CREATE INDEX idx_magazine_author ON magazine_info(author);
CREATE INDEX idx_magazine_category ON magazine_info(category);
CREATE INDEX idx_content_magazine_id ON magazine_content(magazine_id);
```

## Setup Instructions

1. Install Dependencies.

```shell
uv venv & uv sync
```
2. Environment Setup
```.env
export DATABASE_URL="postgresql://user:password@localhost/magazine_db"
export MODEL_NAME="all-MiniLM-L6-v2"
```
3. 
