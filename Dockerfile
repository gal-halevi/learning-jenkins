FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 10001 appuser
USER appuser

COPY calculator/ calculator/

ENTRYPOINT ["python", "-m", "calculator"]