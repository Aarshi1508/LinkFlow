"""
LinkFlow API entrypoint.

Router registration happens here and only here - main.py doesn't contain
any business or DB logic itself. This keeps the "wiring" of the app in one
place that's easy to scan.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import auth, dashboard, redirect, urls

app = FastAPI(
    title=settings.APP_NAME,
    description="A clean, production-style URL shortener API built with FastAPI.",
    version="1.0.0",
)

# Allow the configured frontend origin(s) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """Simple liveness check used by Docker/monitoring."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}


app.include_router(auth.router)
app.include_router(urls.router)
app.include_router(dashboard.router)
app.include_router(redirect.router)
