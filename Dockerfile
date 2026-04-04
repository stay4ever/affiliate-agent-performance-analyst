# ──────────────────────────────────────────────────────────────────────────────
# Production Dockerfile — affiliate-agent-performance-analyst
# Single-stage build: clean, reliable, proven to match the CI install path.
# ──────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

# Non-root user for security
RUN addgroup --system agent && adduser --system --ingroup agent agent

WORKDIR /app

# Copy package definition first (layer-caches pip install unless pyproject.toml changes)
COPY pyproject.toml .
COPY src/ src/

# Install the package + all runtime dependencies
RUN pip install --no-cache-dir "hatchling>=1.24.0" \
 && pip install --no-cache-dir . \
 && pip cache purge

# Default output directory (mountable volume in production)
RUN mkdir -p /app/output && chown -R agent:agent /app

USER agent

# ── Environment defaults (override at runtime) ────────────────────────────────
ENV LOG_LEVEL=INFO \
    OUTPUT_DIR=/app/output \
    OPENAI_MODEL=gpt-4o \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# The CLI entrypoint registered by pyproject.toml
ENTRYPOINT ["performance-analyst"]
CMD ["--help"]
