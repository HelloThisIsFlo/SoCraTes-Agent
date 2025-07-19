# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Set non-sensitive environment variables
ENV GOOGLE_GENAI_USE_VERTEXAI=False
ENV LANGSMITH_TRACING=true
ENV LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com/

# Note: Sensitive API keys (GOOGLE_API_KEY, LANGSMITH_API_KEY) should be passed at runtime
# using docker run -e or docker-compose environment settings for security

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/

# Expose port 7860 (Gradio default)
EXPOSE 7860

# Set environment variable for Gradio to bind to all interfaces
ENV GRADIO_SERVER_NAME=0.0.0.0

# Run the UI application
CMD ["uv", "run", "python", "-m", "src.ui"] 