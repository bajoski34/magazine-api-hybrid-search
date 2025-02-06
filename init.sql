-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a new Database
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'magazine_db') THEN
      PERFORM pg_create_database('magazine_db');
   END IF;
END
$$;

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
    magazine_id INTEGER REFERENCES magazine_info(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    vector_representation VECTOR(384), -- Storing BERT or other embeddings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_magazine_title ON magazine_info(title);
CREATE INDEX idx_magazine_author ON magazine_info(author);
CREATE INDEX idx_magazine_category ON magazine_info(category);
CREATE INDEX idx_content_magazine_id ON magazine_content(magazine_id);