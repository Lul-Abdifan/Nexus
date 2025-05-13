# FROM python:3.10

# ENV PYTHONUNBUFFERED=1

# WORKDIR /app/



# # Install uv
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# # Place executables in the environment at the front of the path
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
# ENV PATH="/app/.venv/bin:$PATH"

# # Compile bytecode
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
# ENV UV_COMPILE_BYTECODE=1

# # uv Cache
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
# ENV UV_LINK_MODE=copy

# # Install dependencies
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --frozen --no-install-project

# ENV PYTHONPATH=/app

# COPY ./scripts /app/scripts

# COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

# COPY ./app /app/app

# # Sync the project
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync

# CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
# Stage 1: Builder - install dependencies and create virtual environment
# Stage 1: Build - install dependencies and set up the environment
FROM python:3.10 as builder

WORKDIR /app

# Install UV (Astral's fast Python installer)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Copy only the necessary files for dependency installation
COPY pyproject.toml uv.lock ./ 

# Install dependencies using UV
RUN uv pip compile pyproject.toml && \
    pip install -r dist/requirements.txt && \
    uv venv


# Stage 2: Runtime - create the final lightweight image
FROM python:3.10-slim

WORKDIR /app

# Copy only what's needed from the builder stage
COPY --from=builder /app/.venv /app/.venv
COPY . . 

# Environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED="1"
ENV UV_COMPILE_BYTECODE="1"
ENV UV_LINK_MODE="copy"

# Ensure scripts are executable
RUN chmod +x /app/scripts/*

# Runtime command (adjust for your FastAPI app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
