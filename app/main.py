from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import recommender, predictor, increment_prediction
from .database import close_mongo_connection
from .config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Shutdown logic
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_home():
    return {"Routes Available": [predictor.router.prefix, recommender.router.prefix],
            "Under Development": [increment_prediction.router.prefix]}

# Machine Learning related routes
app.include_router(predictor.router)
app.include_router(recommender.router)
# app.include_router(increment_prediction.router)