FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

COPY calculator/ calculator/

ENTRYPOINT ["python", "-m", "calculator"]