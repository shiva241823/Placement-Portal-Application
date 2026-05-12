from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from flask_caching import Cache # type: ignore
from celery import Celery # type: ignore

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()

celery = Celery(__name__)

def init_celery(app):
    """
    Bind Celery with Flask app context
    """
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="UTC",
        enable_utc=True
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask