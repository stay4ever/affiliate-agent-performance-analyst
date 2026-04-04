# ──────────────────────────────────────────────────────────────────────────────
# Production Dockerfile — affiliate-agent-performance-analyst
# Multi-stage build: builder installs deps, final image is minimal.
# ──────────────────────────────────────────────────────────────────────────────

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build tooling
RUN pip install --no-cache-dir hatchling>=1.24.0

# Copy only the files needed to resolve & install dependencies first
# (layer-caches pip install unless pyproject.toml changes)
COPY pyproject.toml .
COPY src/ src/

# Install the package and all runtime dependencies into a prefix directory
RUN pip install --no-cache-dir --prefix=/install .

# ── Stage 2: final runtime image ──────────────────────────────────────────────
FROM python:3.12-slim

# Non-root user for security
RUN addgroup --system agent && adduser --system --ingroup agent agent

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy source so the package is importable in editable-equivalent fashion
COPY --from=builder /build/src /app/src

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
