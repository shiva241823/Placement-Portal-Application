from flask import Blueprint, request, jsonify # type: ignore
from app.extensions import db
from app.models import User, StudentProfile, CompanyProfile
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity # type: ignore
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

# STUDENT REGISTRATION
@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")
    branch = data.get("branch")
    cgpa = data.get("cgpa")
    graduation_year = data.get("graduation_year")

    if not email or not password or not full_name:
        return jsonify({"error": "Required fields missing"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(email=email, role="student")
    user.set_password(password)

    db.session.add(user)
    db.session.flush()

    student_profile = StudentProfile(
        user_id=user.id,
        full_name=full_name,
        branch=branch,
        cgpa=cgpa,
        graduation_year=graduation_year
    )

    db.session.add(student_profile)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"}), 201


# COMPANY REGISTRATION
@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    company_name = data.get("company_name")
    hr_contact = data.get("hr_contact")
    website = data.get("website")

    if not email or not password or not company_name:
        return jsonify({"error": "Required fields missing"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(email=email, role="company")
    user.set_password(password)

    db.session.add(user)
    db.session.flush()

    company_profile = CompanyProfile(
        user_id=user.id,
        company_name=company_name,
        hr_contact=hr_contact,
        website=website,
        approval_status="Pending"
    )

    db.session.add(company_profile)
    db.session.commit()

    return jsonify({
        "message": "Company registered successfully. Await admin approval."
    }), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Account deactivated"}), 403

    if user.is_blacklisted:
        return jsonify({"error": "Account blacklisted by admin"}), 403

    if user.role == "company":
        if not user.company_profile or user.company_profile.approval_status != "Approved":
            return jsonify({
                "error": "Company not approved by admin yet"
            }), 403

    access_token = create_access_token(
        identity=str(user.id),  
        additional_claims={"role": user.role},
        expires_delta=timedelta(hours=6)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "role": user.role
    }), 200


# GET CURRENT USER
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role
    }), 200