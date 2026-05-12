from flask import Flask # type: ignore
from config import Config
from flask_cors import CORS # type: ignore
from .extensions import db, jwt, cache, celery, init_celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    
    init_celery(app)

    from .routes.auth_routes import auth_bp
    from .routes.admin_routes import admin_bp
    from .routes.company_routes import company_bp
    from .routes.student_routes import student_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(company_bp, url_prefix="/api/company")
    app.register_blueprint(student_bp, url_prefix="/api/student")

    return app