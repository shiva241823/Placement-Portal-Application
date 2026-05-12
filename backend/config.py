import os


class Config:
    # BASIC CONFIG
    SECRET_KEY = "super-secret-key-of-application"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "ppa.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT CONFIG
    JWT_SECRET_KEY = "this-is-a-very-strong-32-character-secret-key-123456"
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 6  # 6 hours
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # REDIS CONFIG
    REDIS_URL = "redis://localhost:6379/0"

    # CACHE CONFIG
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300

    # CELERY CONFIG
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TIMEZONE = "UTC"