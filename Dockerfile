FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src/ src/

# Install dependencies
RUN uv sync --no-dev

# Create adloop config directory
RUN mkdir -p /root/.adloop

# Default environment variables
ENV ADLOOP_HOST=0.0.0.0
ENV ADLOOP_PORT=3000

EXPOSE 3000

# Start the MCP server with streamable-http transport
CMD ["/app/.venv/bin/python", "-m", "adloop", "--transport", "streamable-http"]
