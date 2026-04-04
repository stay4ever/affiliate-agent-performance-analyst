# ──────────────────────────────────────────────────────────────────────────────
# Production Dockerfile — affiliate-agent-performance-analyst
# ──────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

# Install build essentials needed by some transitive deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for security
RUN addgroup --system agent && adduser --system --ingroup agent agent

WORKDIR /app

# Upgrade pip only — let pip handle hatchling via PEP 517 build isolation
# (do NOT pre-install hatchling separately; it causes resolver conflicts)
RUN pip install --no-cache-dir --upgrade pip

# Copy package definition + source
COPY pyproject.toml .
COPY src/ src/

# Install the package — pip invokes hatchling automatically via build isolation
RUN pip install --no-cache-dir .

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
