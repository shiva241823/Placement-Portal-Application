from flask import Blueprint, jsonify, request, Response # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt # type: ignore
from app.models import User, StudentProfile, CompanyProfile, PlacementDrive, Application
from app.extensions import db
from datetime import datetime
import csv
import io


student_bp = Blueprint("student", __name__)


# ROLE CHECK
def get_current_student():
    claims = get_jwt()

    if claims.get("role") != "student":
        return None

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user or not user.student_profile:
        return None

    if not user.is_active or user.is_blacklisted:
        return None

    return user


# BRANCH ELIGIBILITY
def is_branch_eligible(student_branch, drive_branches):

    if not drive_branches:
        return True

    student_branch = student_branch.strip().lower()

    allowed = [b.strip().lower() for b in drive_branches.split(",")]

    return student_branch in allowed


# STUDENT PROFILE INFO
@student_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    student = user.student_profile

    return jsonify({
        "id": student.id,
        "full_name": student.full_name,
        "email": user.email,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "resume_link": student.resume_link
    })


@student_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    search = request.args.get("search", "")
    student = user.student_profile

    query = PlacementDrive.query.join(CompanyProfile).filter(
        PlacementDrive.status == "Approved",
        CompanyProfile.approval_status == "Approved"
    )

    if search:
        query = query.filter(
            db.or_(
                PlacementDrive.job_title.ilike(f"%{search}%"),
                CompanyProfile.company_name.ilike(f"%{search}%")
            )
        )

    drives = query.all()
    response = []

    for d in drives:

        eligible = True

        if d.min_cgpa and student.cgpa < d.min_cgpa:
            eligible = False

        if not is_branch_eligible(student.branch, d.eligible_branch):
            eligible = False

        if d.eligible_year and student.graduation_year != d.eligible_year:
            eligible = False

        already_applied = Application.query.filter_by(
            student_id=student.id,
            drive_id=d.id
        ).first() is not None

        response.append({
            "drive_id": d.id,
            "company": d.company.company_name,
            "job_title": d.job_title,
            "description": d.job_description,
            "deadline": d.application_deadline.isoformat() if d.application_deadline else None,
            "min_cgpa": d.min_cgpa,
            "eligible_branch": d.eligible_branch,
            "eligible_year": d.eligible_year,
            "is_eligible": eligible,
            "already_applied": already_applied
        })

    return jsonify(response)

# VIEW APPROVED COMPANIES
@student_bp.route("/companies", methods=["GET"])
@jwt_required()
def view_companies():

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    companies = CompanyProfile.query.join(User).filter(
        CompanyProfile.approval_status == "Approved",
        User.is_active == True,
        User.is_blacklisted == False
    ).all()

    return jsonify([
        {
            "company_id": c.id,
            "company_name": c.company_name,
            "email": c.user.email,
            "website": c.website,
            "hr_contact": c.hr_contact
        }
        for c in companies
    ])


# VIEW DRIVES OF A COMPANY
@student_bp.route("/company/<int:company_id>/drives", methods=["GET"])
@jwt_required()
def company_drives(company_id):

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    student = user.student_profile

    drives = PlacementDrive.query.filter_by(
        company_id=company_id,
        status="Approved"
    ).all()

    response = []

    for d in drives:

        eligible = True

        if d.min_cgpa and student.cgpa < d.min_cgpa:
            eligible = False

        if not is_branch_eligible(student.branch, d.eligible_branch):
            eligible = False

        if d.eligible_year and student.graduation_year != d.eligible_year:
            eligible = False

        already_applied = Application.query.filter_by(
            student_id=student.id,
            drive_id=d.id
        ).first() is not None

        response.append({
            "drive_id": d.id,
            "job_title": d.job_title,
            "description": d.job_description,
            "deadline": d.application_deadline.isoformat() if d.application_deadline else None,
            "is_eligible": eligible,
            "already_applied": already_applied
        })

    return jsonify(response)


# APPLY TO DRIVE
@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
def apply_to_drive(drive_id):

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    student = user.student_profile
    drive = PlacementDrive.query.get(drive_id)

    if not drive or drive.status != "Approved":
        return jsonify({"error": "Drive not available"}), 404

    if drive.application_deadline and drive.application_deadline < datetime.utcnow():
        return jsonify({"error": "Deadline passed"}), 403

    if drive.min_cgpa and student.cgpa < drive.min_cgpa:
        return jsonify({"error": "CGPA criteria not met"}), 403

    if not is_branch_eligible(student.branch, drive.eligible_branch):
        return jsonify({"error": "Branch not eligible"}), 403

    if drive.eligible_year and student.graduation_year != drive.eligible_year:
        return jsonify({"error": "Graduation year not eligible"}), 403

    if Application.query.filter_by(student_id=student.id, drive_id=drive.id).first():
        return jsonify({"error": "Already applied"}), 400

    application = Application(
        student_id=student.id,
        drive_id=drive.id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Applied successfully"}), 201


# VIEW APPLICATION HISTORY
@student_bp.route("/applications", methods=["GET"])
@jwt_required()
def view_applications():

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    apps = Application.query.join(PlacementDrive).join(CompanyProfile).filter(
        Application.student_id == user.student_profile.id
    ).all()

    return jsonify([
        {
            "company": a.drive.company.company_name,
            "job_title": a.drive.job_title,
            "status": a.status,
            "applied_on": a.application_date.isoformat() if a.application_date else None,
            "interview_date": a.interview_date.isoformat() if a.interview_date else None
        }
        for a in apps
    ])


# UPDATE PROFILE
@student_bp.route("/update-profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    data = request.get_json() or {}
    student = user.student_profile

    student.full_name = data.get("full_name", student.full_name)
    student.branch = data.get("branch", student.branch)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.graduation_year = data.get("graduation_year", student.graduation_year)
    student.resume_link = data.get("resume_link", student.resume_link)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})


# EXPORT CSV
@student_bp.route("/export-history", methods=["GET"])
@jwt_required()
def export_history():

    user = get_current_student()
    if not user:
        return jsonify({"error": "Student access required"}), 403

    from celery_worker import export_student_history
    export_student_history.delay(user.student_profile.id)

    return jsonify({
        "message": "Your export request has been submitted. CSV will be sent to your email shortly."
    }), 200