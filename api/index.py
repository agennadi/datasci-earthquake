from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers import (
    liquefaction_api,
    tsunami_api,
    soft_story_api
)

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json", redirect_slashes=False)


app.include_router(liquefaction_api.router)
app.include_router(tsunami_api.router)
app.include_router(soft_story_api.router)

@app.get("/api/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}