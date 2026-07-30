# Single-stage build: FastAPI apps don't need a compiled build step, so a
# multi-stage build wouldn't buy us anything here (unlike the frontend).
FROM python:3.12-slim

WORKDIR /app

# System deps for building psycopg2 from source if a prebuilt wheel isn't
# available for the target platform. bcrypt ships its own prebuilt
# manylinux wheels for this image's platform, so no extra system packages
# are needed for it specifically.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first so Docker can cache this layer - it only
# reinstalls dependencies when requirements.txt actually changes, not on
# every code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
