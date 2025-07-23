import os
from dotenv import load_dotenv

class Settings():
    MONGO_URI: str
    MONGO_DB: str = "mydatabase"
    
    APP_NAME: str 
    APP_DESCRIPTION: str

# Load variables from the .env file (must be called at the start)
load_dotenv()

settings = Settings()


# Access environment variables
settings.MONGO_URI = os.getenv("MONGO_URI")
settings.MONGO_DB = os.getenv("MONGO_DB", "mydatabase")

settings.APP_NAME = os.getenv("APP_NAME")
settings.APP_DESCRIPTION = os.getenv("APP_DESCRIPTION")

if __name__ == "__main__":
    print("Configuration settings:")
    print(f"MongoDB URI: {settings.MONGO_URI}")
    print(f"MongoDB Database: {settings.MONGO_DB}")
    print(f"App Name: {settings.APP_NAME}")
    print(f"App Description: {settings.APP_DESCRIPTION}")