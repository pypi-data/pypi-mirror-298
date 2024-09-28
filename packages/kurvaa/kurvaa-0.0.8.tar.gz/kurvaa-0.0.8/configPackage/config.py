from fastapi import FastAPI
from routes import health
from prometheus_fastapi_instrumentator import Instrumentator

def setup_health_checks(app: FastAPI):

    # Setup routes
    app.include_router(
        health.router, prefix="/prosperity-svc/internals/health", tags=["health"]
    )
    # Setup Prometheus metrics
    instrumentor = Instrumentator()
    instrumentor.instrument(app).expose(app, endpoint="/prosperity-svc/metrics")

