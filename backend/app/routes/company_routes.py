from flask import Blueprint, jsonify, request # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt # type: ignore
from app.models import User, CompanyProfile, PlacementDrive, Application, StudentProfile
from app.extensions import db
from datetime import datetime, timedelta

company_bp = Blueprint("company", __name__)


# COMPANY ROLE CHECK
def company_required():
    claims = get_jwt()
    if claims.get("role") != "company":
        return None

    return int(get_jwt_identity())


# COMPANY DASHBOARD

@company_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def company_dashboard():

    user_id = company_required()
    if not user_id:
        return jsonify({"error": "Company access required"}), 403

    user = User.query.get(user_id)
    if not user or not user.company_profile:
        return jsonify({"error": "Company profile not found"}), 404

    company = user.company_profile

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    drive_data = []
    for drive in drives:
        applicants = Application.query.filter_by(drive_id=drive.id).count()

        drive_data.append({
            "drive_id": drive.id,
            "job_title": drive.job_title,
            "status": drive.status,
            "application_deadline": drive.application_deadline,
            "applicants_count": applicants
        })

    return jsonify({
        "company_name": company.company_name,
        "email": user.email,
        "hr_contact": company.hr_contact,   
        "website": company.website,         
        "approval_status": company.approval_status,
        "drives": drive_data
    })


# CREATE PLACEMENT DRIVE

@company_bp.route("/create-drive", methods=["POST"])
@jwt_required()
def create_drive():

    user_id = company_required()
    if not user_id:
        return jsonify({"error": "Company access required"}), 403

    user = User.query.get(user_id)
    company = user.company_profile

    if company.approval_status != "Approved":
        return jsonify({"error": "Company not approved by admin"}), 403

    data = request.get_json() or {}

    job_title = data.get("job_title")
    job_description = data.get("job_description")
    eligible_branches = data.get("eligible_branches") 
    min_cgpa = data.get("min_cgpa")
    eligible_year = data.get("eligible_year")
    deadline = data.get("application_deadline")

    if not job_title or not job_description or not deadline:
        return jsonify({"error": "Required fields missing"}), 400

    try:
        parsed_deadline = datetime.strptime(deadline, "%Y-%m-%d")
    except:
        return jsonify({"error": "Invalid deadline format"}), 400

    drive = PlacementDrive(
        company_id=company.id,
        job_title=job_title,
        job_description=job_description,
        eligible_branch=",".join(eligible_branches),
        min_cgpa=min_cgpa,
        eligible_year=eligible_year,
        application_deadline=parsed_deadline,
        status="Pending"
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Drive created. Awaiting admin approval"}), 201


# VIEW DRIVE APPLICATIONS
@company_bp.route("/drive/<int:drive_id>/applications", methods=["GET"])
@jwt_required()
def view_drive_applications(drive_id):

    user_id = company_required()
    if not user_id:
        return jsonify({"error": "Company access required"}), 403

    user = User.query.get(user_id)
    company = user.company_profile

    drive = PlacementDrive.query.get(drive_id)

    if not drive or drive.company_id != company.id:
        return jsonify({"error": "Unauthorized"}), 403

    applications = Application.query.filter_by(drive_id=drive_id).all()

    data = []
    for app in applications:
        data.append({
            "application_id": app.id,
            "student_name": app.student.full_name,
            "branch": app.student.branch,
            "cgpa": app.student.cgpa,
            "resume_link": app.student.resume_link,
            "status": app.status,
            "interview_date": app.interview_date
        })

    return jsonify(data)


# UPDATE APPLICATION
@company_bp.route("/application/<int:application_id>/update", methods=["PUT"])
@jwt_required()
def update_application(application_id):

    user_id = company_required()
    if not user_id:
        return jsonify({"error": "Company access required"}), 403

    user = User.query.get(user_id)
    company = user.company_profile

    application = Application.query.get(application_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404

    if application.drive.company_id != company.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    new_status = data.get("status")
    interview_date = data.get("interview_date")

    allowed_status = ["Shortlisted", "Interview Scheduled", "Selected", "Rejected"]

    if new_status:
        if new_status not in allowed_status:
            return jsonify({"error": "Invalid status"}), 400

        application.status = new_status

    if interview_date:
        try:
            parsed_date = datetime.strptime(interview_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

        if application.status not in ["Shortlisted", "Interview Scheduled"]:
            return jsonify({
                "error": "Interview can only be scheduled after shortlisting"
            }), 400

        application.status = "Interview Scheduled"
        application.interview_date = parsed_date

    db.session.commit()

    return jsonify({"message": "Application updated successfully"})