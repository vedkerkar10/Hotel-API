# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import time
import logging

# Move imports for shared state here
REQUEST_COUNT = 0

from routers import rooms_crud, availability, bookings, auth, rbac, images, pagination, background_tasks, websockets, observability

# Create static directory if it doesn't exist for Lab 9
os.makedirs('static/images', exist_ok=True)

app = FastAPI(title="Hotel API", version="0.1")

# Mount the static directory for serving images (Lab 9)
app.mount('/static', StaticFiles(directory='static'), name='static')

# CORS Middleware (Lab 15)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging and Request Count Middleware (Lab 15 and 21)
logger = logging.getLogger("hotel")
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_and_count_requests(request: Request, call_next):
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    logger.info(f"{request.method} {request.url} completed_in={process_time:.3f}s status_code={response.status_code}")
    return response

# Custom Exception Handler (Lab 15)
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

# Include routers from other labs
app.include_router(rooms_crud.router)
app.include_router(availability.router)
app.include_router(bookings.router)
app.include_router(auth.router)
app.include_router(rbac.router)
app.include_router(images.router)
app.include_router(pagination.router)
app.include_router(background_tasks.router)
app.include_router(websockets.router)
app.include_router(observability.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel API!"}