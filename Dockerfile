# Use a minimal Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the script into the container
COPY extractor.py .

# Install required library
RUN pip install pymupdf

# Default command for challenge compliance
CMD ["python", "extractor.py", "--input", "/app/input"]
