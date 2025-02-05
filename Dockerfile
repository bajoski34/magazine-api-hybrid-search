# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock (if available)
COPY pyproject.toml .

# Install `uv`
RUN pip install uv

# Install dependencies using `uv`
RUN uv sync

# Copy the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application using Uvicorn with 4 workers
CMD ["uvicorn", "app:main", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]