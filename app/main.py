from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
import time
import os
import logging
import random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Structured logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s","logger":"%(name)s"}'
)
logger = logging.getLogger("sample-app")

app = FastAPI(title="Sample App for Observability", version="1.0.0")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

START_TIME = time.time()


@app.middleware("http")
async def metrics_and_logging(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    endpoint = request.url.path
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)

    logger.info(
        f"{request.method} {endpoint} -> {response.status_code} ({duration:.3f}s)"
    )
    return response


@app.get("/")
async def root():
    return {
        "message": "Observability Demo App",
        "version": "1.0.0",
        "env": os.getenv("APP_ENV", "local")
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "uptime": round(time.time() - START_TIME, 2)}


@app.get("/ready")
async def ready():
    return {"status": "ready"}


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/api/data")
async def get_data():
    # Имитация работы + иногда ошибки
    delay = random.uniform(0.01, 0.3)
    time.sleep(delay)

    if random.random() < 0.05:  # 5% ошибок
        logger.error("Simulated internal error while fetching data")
        return JSONResponse(
            status_code=500,
            content={"error": "internal server error"}
        )

    logger.info("Successfully returned data")
    return {
        "items": [
            {"id": 1, "name": "item-1"},
            {"id": 2, "name": "item-2"},
            {"id": 3, "name": "item-3"},
        ],
        "delay_ms": round(delay * 1000, 1)
    }


@app.get("/api/slow")
async def slow_endpoint():
    """Эндпоинт для демонстрации высокой latency"""
    delay = random.uniform(0.8, 2.0)
    time.sleep(delay)
    logger.warning(f"Slow endpoint took {delay:.2f}s")
    return {"message": "This was intentionally slow", "delay": delay}
