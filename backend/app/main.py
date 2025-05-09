from fastapi import FastAPI
from app.routers import stocks, users, watchlist
from fastapi.middleware.cors import CORSMiddleware
from app import database
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

# Lifecycle context for app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup: ensures DB tables are created from SQLAlchemy models
    database.Base.metadata.create_all(bind=database.engine)
    yield
    # Runs once on shutdown (can be used to clean up resources if needed)

# Instantiate FastAPI app with lifespan hook
app = FastAPI(title="MarketMuse - Stock Prediction API", lifespan=lifespan)

# CORS configuration: allow requests from frontend and API origins
origins = [
    "http://localhost:5173",                   # local development
    "https://marketmuse.chinmaymisra.com",     # production frontend
]

# Register CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route handlers from modular routers
app.include_router(stocks.router)
app.include_router(users.router)
app.include_router(watchlist.router)

# Middleware to log every HTTP request and its response status
@app.middleware("http")
async def log_all_requests(request, call_next):
    print(f"➡️ {request.method} {request.url}")
    response = await call_next(request)
    print(f"⬅️ {response.status_code}")
    return response

# Root route for API base URL
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return JSONResponse(content={"message": "Welcome to MarketMuse API"})

# Health check route (useful for uptime checks)
@app.get("/ping")
def ping():
    return {"message": "pong"}
