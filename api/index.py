from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers import (
    liquefaction_api,
    tsunami_api,
    soft_story_api,
    health_api,
)
from backend.api.config import settings
import sentry_sdk
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Sentry
sentry_sdk.init(
    dsn=settings.sentry_dsn,
    # Add request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=False,
)

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/docs", openapi_url="/openapi.json", redirect_slashes=False)

# Log startup information
logger.info(f"Starting FastAPI application")
logger.info(f"Environment: {settings.environment}")
logger.info(f"PORT environment variable: {os.getenv('PORT', 'not set')}")

app.include_router(liquefaction_api.router)
app.include_router(tsunami_api.router)
app.include_router(soft_story_api.router)
app.include_router(health_api.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code} for {request.method} {request.url.path}")
        return response
    except Exception as e:
        logger.error(f"Error handling request {request.method} {request.url.path}: {str(e)}", exc_info=True)
        raise

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint for basic connectivity check
@app.get("/")
def root():
    """Root endpoint to verify server is running"""
    logger.info("Root endpoint called")
    return {"message": "API is running", "status": "ok"}


# Global exception handler (ensures flush before serverless exit)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    sentry_sdk.flush(timeout=2.0)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
