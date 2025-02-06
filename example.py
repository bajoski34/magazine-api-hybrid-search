from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example documents
documents = [
    "This is a test sentence.",
    "Another example document.",
    "More text to search through."
]

# Generate embeddings for the documents
document_embeddings = model.encode(documents)

print(document_embeddings)

# Example query
query = "Test search query"

# Generate embedding for the query
query_embedding = model.encode([query])

print(query_embedding)

# Compute the cosine similarity between the query and each document
similarities = cosine_similarity(query_embedding, document_embeddings)

# Get the index of the most similar document
most_similar_document_index = similarities.argmax()

# Print the most similar document
print(f"Most similar document: {documents[most_similar_document_index]}")