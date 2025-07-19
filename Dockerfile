# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Accept build arguments for environment variables
ARG GOOGLE_GENAI_USE_VERTEXAI
ARG GOOGLE_API_KEY
ARG LANGSMITH_TRACING
ARG LANGSMITH_API_KEY
ARG LANGCHAIN_ENDPOINT

# Set environment variables
ENV GOOGLE_GENAI_USE_VERTEXAI=${GOOGLE_GENAI_USE_VERTEXAI}
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV LANGSMITH_TRACING=${LANGSMITH_TRACING}
ENV LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
ENV LANGCHAIN_ENDPOINT=${LANGCHAIN_ENDPOINT}

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