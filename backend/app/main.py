from fastapi import FastAPI
from app.routers import stocks, users
from fastapi.middleware.cors import CORSMiddleware
from app import database
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    database.Base.metadata.create_all(bind=database.engine)
    yield
    # Optional: cleanup on shutdown

app = FastAPI(title="MarketMuse - Stock Prediction API", lifespan=lifespan)

origins = [
    "http://localhost:5173",  # dev frontend
    "https://marketmuse.chinmaymisra.com",  # prod frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router)
app.include_router(users.router)

@app.middleware("http")
async def log_all_requests(request, call_next):
    print(f"➡️ {request.method} {request.url}")
    response = await call_next(request)
    print(f"⬅️ {response.status_code}")
    return response

@app.api_route("/", methods = ["GET","HEAD"])
def root():
    return JSONResponse(content = {"message": "Welcome to MarketMuse API"})

@app.get("/ping")
def ping():
    return {"message": "pong"}