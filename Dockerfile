FROM python:3.14-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv via pip (reliable on slim)
RUN pip install --no-cache-dir uv

# Sanity check
RUN uv --version

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .


CMD [ "uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "9090"]