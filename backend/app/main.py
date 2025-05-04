from fastapi import FastAPI
from app.routers import stocks,users
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import base_models

# Create tables
Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost:5173", #dev frontend
    "https://marketmuse.chinmaymisra.com", #prod frontend
 ]

app = FastAPI(title = 'MarketMuse - Stock Prediction API')

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



@app.get("/")
def root():
    return {"message" : "Welcome to MarketMuse API"}


