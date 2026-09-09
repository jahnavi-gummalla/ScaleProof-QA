import time

import psutil
from fastapi import Request
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from starlette.responses import Response


HTTP_REQUESTS_TOTAL = Counter(
    "scaleproof_http_requests_total",
    "Total number of HTTP requests processed.",
    ["method", "endpoint", "status_code"],
)

HTTP_REQUEST_DURATION = Histogram(
    "scaleproof_http_request_duration_seconds",
    "Time spent processing HTTP requests.",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
)

CPU_USAGE_PERCENT = Gauge(
    "scaleproof_cpu_usage_percent",
    "Current system CPU usage percentage.",
)

MEMORY_USAGE_PERCENT = Gauge(
    "scaleproof_memory_usage_percent",
    "Current system memory usage percentage.",
)


async def collect_request_metrics(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    HTTP_REQUESTS_TOTAL.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()

    HTTP_REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    return response


def prometheus_metrics_response():
    CPU_USAGE_PERCENT.set(psutil.cpu_percent())
    MEMORY_USAGE_PERCENT.set(psutil.virtual_memory().percent)

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )