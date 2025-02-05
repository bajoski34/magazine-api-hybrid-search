# Use an official Python image as a base
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Install `uv` package manager
RUN pip install uv

# Copy the project files
COPY . .

# Install dependencies using `uv`
RUN uv pip install --system -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the app with 4 Uvicorn workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
