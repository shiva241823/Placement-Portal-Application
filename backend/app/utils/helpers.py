from flask_jwt_extended import get_jwt_identity # type: ignore
from flask import jsonify # type: ignore
from app.models import PlacementDrive, StudentProfile
from datetime import datetime


# ==============================
# ROLE CHECK HELPERS
# ==============================
def require_role(role):
    identity = get_jwt_identity()
    if not identity or identity["role"] != role:
        return False
    return True


# ==============================
# STANDARD RESPONSE FORMAT
# ==============================
def success_response(message, data=None):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    })


def error_response(message, status_code=400):
    return jsonify({
        "success": False,
        "message": message
    }), status_code


# ==============================
# ELIGIBILITY CHECK
# ==============================
def check_eligibility(student: StudentProfile, drive: PlacementDrive):

    if drive.min_cgpa and student.cgpa < drive.min_cgpa:
        return False, "CGPA criteria not met"

    if drive.eligible_branch and drive.eligible_branch != student.branch:
        return False, "Branch not eligible"

    if drive.eligible_year and drive.eligible_year != student.graduation_year:
        return False, "Graduation year not eligible"

    if drive.application_deadline and drive.application_deadline < datetime.utcnow():
        return False, "Application deadline passed"

    return True, "Eligible"