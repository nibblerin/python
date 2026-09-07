FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.14-slim AS runtime
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . .
RUN useradd --system --no-create-home --uid 10001 appuser
USER appuser

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]