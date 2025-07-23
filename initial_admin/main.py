from fastapi import FastAPI
from .routes import ml_routes
from .database import connect_to_mongo, close_mongo_connection
from .config import settings

print(settings.APP_NAME)
print(settings.APP_DESCRIPTION)
# 
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
)

# Include machine learning related routes
app.include_router(ml_routes.router, prefix="/ml", tags=["ML Operations"])


# Connect to MongoDB when app starts
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    print("Connected to MongoDB")


# Close MongoDB connection when app shuts down
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    print("MongoDB connection closed")
