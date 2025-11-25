import os
from dotenv import load_dotenv
from redis import Redis
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "redis"
    SESSION_REDIS = Redis(host='localhost', port=6379)
