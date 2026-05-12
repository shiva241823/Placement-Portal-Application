from app.extensions import cache
from flask import Blueprint, request, jsonify # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity # type: ignore
from sqlalchemy import or_ # type: ignore
from app.extensions import db
from app.models import (
    User,
    StudentProfile,
    CompanyProfile,
    PlacementDrive,
    Application
)

admin_bp = Blueprint("admin", __name__)

# ADMIN ACCESS CHECK

def admin_required():
    if request.method == "OPTIONS":
        return None, None, None

    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user or user.role != "admin":
        return None, jsonify({"error": "Admin access required"}), 403

    return user, None, None



# ADMIN DASHBOARD

@admin_bp.route("/dashboard", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def admin_dashboard():
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    return jsonify({
        "total_companies": CompanyProfile.query.count(),
        "total_drives": PlacementDrive.query.filter_by(status="Approved").count(),
        "total_students": db.session.query(StudentProfile)
            .join(User)
            .filter(
                User.role == "student",
                User.is_active == True,
                User.is_blacklisted == False
            ).count(),
    })



# COMPANY MANAGEMENT

@admin_bp.route("/companies", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all_companies():
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    search = request.args.get("search", "")
    query = CompanyProfile.query.join(User)

    if search:
        query = query.filter(
            or_(
                CompanyProfile.company_name.ilike(f"%{search}%"),
                CompanyProfile.hr_contact.ilike(f"%{search}%"),
                CompanyProfile.website.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    companies = query.order_by(
        CompanyProfile.approval_status.desc(),
        CompanyProfile.company_name.asc()
    ).all()

    return jsonify([{
        "id": c.id,
        "user_id": c.user.id,
        "company_name": c.company_name,
        "hr_contact": c.hr_contact,
        "website": c.website,
        "approval_status": c.approval_status,
        "is_active": c.user.is_active,
        "is_blacklisted": c.user.is_blacklisted
    } for c in companies])


@admin_bp.route("/company/<int:company_id>/approve", methods=["PUT"])
@jwt_required()
def approve_company(company_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = "Approved"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Company approved"})


@admin_bp.route("/company/<int:company_id>/reject", methods=["PUT"])
@jwt_required()
def reject_company(company_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = "Rejected"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Company rejected"})


@admin_bp.route("/company/<int:user_id>/toggle-active", methods=["PUT"])
@jwt_required()
def toggle_company_active(user_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    company_user = User.query.get_or_404(user_id)

    if company_user.role != "company":
        return jsonify({"error": "Invalid company user"}), 400

    company_user.is_active = not company_user.is_active
    db.session.commit()
    cache.clear()
    return jsonify({"is_active": company_user.is_active})


@admin_bp.route("/company/<int:user_id>/toggle-blacklist", methods=["PUT"])
@jwt_required()
def toggle_company_blacklist(user_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    company_user = User.query.get_or_404(user_id)

    if company_user.role != "company":
        return jsonify({"error": "Invalid company user"}), 400

    company_user.is_blacklisted = not company_user.is_blacklisted
    db.session.commit()
    cache.clear()
    return jsonify({"is_blacklisted": company_user.is_blacklisted})


# STUDENT MANAGEMENT

@admin_bp.route("/students", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all_students():
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    search = request.args.get("search", "")
    query = StudentProfile.query.join(User)

    if search:
        query = query.filter(
            or_(
                StudentProfile.full_name.ilike(f"%{search}%"),
                StudentProfile.branch.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    students = query.order_by(StudentProfile.full_name.asc()).all()

    return jsonify([{
        "student_profile_id": s.id,
        "user_id": s.user.id,
        "full_name": s.full_name,
        "branch": s.branch,
        "cgpa": s.cgpa,
        "graduation_year": s.graduation_year,
        "email": s.user.email,
        "is_active": s.user.is_active,
        "is_blacklisted": s.user.is_blacklisted
    } for s in students])


@admin_bp.route("/student/<int:user_id>/toggle-active", methods=["PUT"])
@jwt_required()
def toggle_student_active(user_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    student_user = User.query.get_or_404(user_id)

    if student_user.role != "student":
        return jsonify({"error": "Invalid student user"}), 400

    student_user.is_active = not student_user.is_active
    db.session.commit()
    cache.clear()
    return jsonify({"is_active": student_user.is_active})


@admin_bp.route("/student/<int:user_id>/toggle-blacklist", methods=["PUT"])
@jwt_required()
def toggle_student_blacklist(user_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    student_user = User.query.get_or_404(user_id)

    if student_user.role != "student":
        return jsonify({"error": "Invalid student user"}), 400

    student_user.is_blacklisted = not student_user.is_blacklisted
    db.session.commit()
    cache.clear()
    return jsonify({"is_blacklisted": student_user.is_blacklisted})


# PLACEMENT DRIVES

@admin_bp.route("/drives", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all_drives():
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    search = request.args.get("search", "")
    query = PlacementDrive.query.join(CompanyProfile)

    if search:
        query = query.filter(
            or_(
                PlacementDrive.job_title.ilike(f"%{search}%"),
                PlacementDrive.job_description.ilike(f"%{search}%"),
                CompanyProfile.company_name.ilike(f"%{search}%")
            )
        )

    drives = query.order_by(
        PlacementDrive.status.desc(),
        PlacementDrive.created_at.desc()
    ).all()

    return jsonify([{
        "id": d.id,
        "company": d.company.company_name,
        "job_title": d.job_title,
        "job_description": d.job_description,
        "min_cgpa": d.min_cgpa,
        "eligible_branch": d.eligible_branch,
        "eligible_year": d.eligible_year,
        "deadline": d.application_deadline,
        "status": d.status
    } for d in drives])


@admin_bp.route("/drive/<int:drive_id>/approve", methods=["PUT"])
@jwt_required()
def approve_drive(drive_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Approved"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Drive approved"})


@admin_bp.route("/drive/<int:drive_id>/reject", methods=["PUT"])
@jwt_required()
def reject_drive(drive_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Rejected"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Drive rejected"})


# APPLICATIONS VIEW

@admin_bp.route("/applications", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def view_all_applications():
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    search = request.args.get("search", "").strip()

    query = Application.query.join(StudentProfile)\
        .join(PlacementDrive)\
        .join(CompanyProfile)

    if search:
        query = query.filter(
            or_(
                StudentProfile.full_name.ilike(f"%{search}%"),
                PlacementDrive.job_title.ilike(f"%{search}%"),
                CompanyProfile.company_name.ilike(f"%{search}%"),
                Application.status.ilike(f"%{search}%")
            )
        )

    applications = query.all()

    return jsonify([{
        "student_name": a.student.full_name,
        "drive_title": a.drive.job_title,
        "company": a.drive.company.company_name,
        "status": a.status,
        "application_date": a.application_date,
        "interview_date": a.interview_date,
        "remarks": a.remarks
    } for a in applications])


# REPORTS

@admin_bp.route("/reports/overview", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def overall_report():
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    return jsonify({
        "total_drives": PlacementDrive.query.filter_by(status="Approved").count(),
        "total_students": db.session.query(StudentProfile)
            .join(User)
            .filter(
                User.role == "student",
                User.is_active == True,
                User.is_blacklisted == False
            ).count(),
        "total_selected_students": db.session.query(Application)
            .join(PlacementDrive)
            .filter(
                Application.status == "Selected",
                PlacementDrive.status == "Approved"
            ).count()
    })


@admin_bp.route("/reports/drives", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def drive_list_for_reports():
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    drives = PlacementDrive.query.filter_by(status="Approved").all()

    return jsonify([
        {"id": d.id, "job_title": d.job_title}
        for d in drives
    ])


@admin_bp.route("/reports/drive/<int:drive_id>", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def drive_report(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive or drive.status != "Approved":
        return jsonify({"error": "Drive not found"}), 404

    students = StudentProfile.query.all()
    eligible_count = 0

    for s in students:
        eligible = True

        if drive.min_cgpa and s.cgpa < drive.min_cgpa:
            eligible = False

        if drive.eligible_branch:
            allowed_branches = [
                b.strip().lower()
                for b in drive.eligible_branch.split(",")
            ]
            if s.branch.strip().lower() not in allowed_branches:
                eligible = False

        if drive.eligible_year and s.graduation_year != drive.eligible_year:
            eligible = False

        if eligible:
            eligible_count += 1

    applications = Application.query.filter_by(drive_id=drive.id).all()

    applied_count = len(applications)
    selected_count = len([a for a in applications if a.status == "Selected"])
    rejected_count = len([a for a in applications if a.status == "Rejected"])

    if eligible_count < applied_count:
        eligible_count = applied_count

    return jsonify({
        "drive_name": drive.job_title,
        "eligible_students": eligible_count,
        "applied": applied_count,
        "selected": selected_count,
        "rejected": rejected_count
    })


# VIEW APPLICATIONS FOR A DRIVE 

@admin_bp.route("/drive/<int:drive_id>/applications", methods=["GET", "OPTIONS"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def admin_view_drive_applications(drive_id):
    user, error_response, status = admin_required()
    if error_response:
        return error_response, status

    drive = PlacementDrive.query.get_or_404(drive_id)
    applications = Application.query.filter_by(drive_id=drive_id).all()

    return jsonify({
        "drive_title": drive.job_title,
        "applications": [{
            "application_id": app.id,
            "student_name": app.student.full_name,
            "email": app.student.user.email,
            "branch": app.student.branch,
            "cgpa": app.student.cgpa,
            "status": app.status,
            "application_date": app.application_date
        } for app in applications]
    })