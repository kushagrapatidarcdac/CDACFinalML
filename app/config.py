import os
from dotenv import load_dotenv

class Settings():
    # Database Configurations
    MONGO_URI: str
    MONGO_DB: str
    
    # Application Configurations
    APP_NAME: str 
    APP_DESCRIPTION: str
    
    def __init__(self):
        load_dotenv()
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.MONGO_DB = os.getenv("MONGO_DB", "mydatabase")
        self.APP_NAME = os.getenv("APP_NAME")
        self.APP_DESCRIPTION = os.getenv("APP_DESCRIPTION")

settings = Settings()


if __name__ == "__main__":
    print("Configuration settings:")
    print(f"MongoDB URI: {settings.MONGO_URI}")
    print(f"MongoDB Database: {settings.MONGO_DB}")
    print(f"App Name: {settings.APP_NAME}")
    print(f"App Description: {settings.APP_DESCRIPTION}")