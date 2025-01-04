import os

class Config:
    API_KEY = os.getenv("API_KEY")
    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")