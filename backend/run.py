from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "admin123"


def create_admin():
    existing_admin = User.query.filter_by(role="admin").first()
    if not existing_admin:
        admin = User(
            email=ADMIN_EMAIL,
            role="admin",
            is_active=True
        )
        admin.set_password(ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()

    app.run(debug=True)