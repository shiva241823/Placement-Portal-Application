from app import create_app
from app.extensions import celery, db
from app.models import (
    PlacementDrive,
    Application,
    User,
    StudentProfile,
    MonthlyReport
)
from app.utils.email_utils import (
    send_monthly_report,
    send_deadline_reminder
)
from datetime import datetime, timedelta
from celery.schedules import crontab # type: ignore
import csv
import os
import smtplib
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# CREATE FLASK APP CONTEXT
app = create_app()
app.app_context().push()


# MONTHLY REPORT TASK
@celery.task
def generate_monthly_report():

    now = datetime.utcnow()

    first_day_this_month = now.replace(day=1)
    last_day_previous_month = first_day_this_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)

    start = first_day_previous_month
    end = last_day_previous_month.replace(hour=23, minute=59, second=59)

    total_drives = PlacementDrive.query.filter(
        PlacementDrive.created_at.between(start, end)
    ).count()

    total_applications = Application.query.filter(
        Application.application_date.between(start, end)
    ).count()

    total_selected = Application.query.filter(
        Application.status == "Selected",
        Application.application_date.between(start, end)
    ).count()

    report = MonthlyReport(
        month=first_day_previous_month.strftime("%B %Y"),
        total_drives=total_drives,
        total_applications=total_applications,
        total_selected=total_selected
    )

    db.session.add(report)
    db.session.commit()

    admin_email = "22f3001174@ds.study.iitm.ac.in"

    send_monthly_report(
        admin_email,
        total_drives,
        total_applications,
        total_selected
    )

    print("Monthly report generated and sent.")
    return "Monthly report sent"


# DAILY DEADLINE REMINDER TASK
@celery.task
def send_daily_reminders():

    now = datetime.utcnow()

    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.application_deadline >= now
    ).all()

    if not drives:
        return "No active drives"

    students = StudentProfile.query.join(User).filter(
        User.role == "student",
        User.is_active == True,
        User.is_blacklisted == False
    ).all()

    for drive in drives:
        for student in students:

            if drive.min_cgpa and (student.cgpa is None or student.cgpa < drive.min_cgpa):
                continue

            if drive.eligible_branch and student.branch != drive.eligible_branch:
                continue

            if drive.eligible_year and student.graduation_year != drive.eligible_year:
                continue

            send_deadline_reminder(
                student.user.email,
                drive.job_title,
                drive.application_deadline
            )

    print("Daily reminders sent.")
    return "Reminders completed"



# ASYNC CSV EXPORT TASK (User Triggered)
@celery.task
def export_student_history(student_id):

    student = StudentProfile.query.get(student_id)

    if not student:
        return "Student not found"

    applications = Application.query.filter_by(
        student_id=student_id
    ).all()

    if not applications:
        return "No applications found"
    
    export_folder = "exports"
    os.makedirs(export_folder, exist_ok=True)

    filename = f"application_history_{student_id}_{int(datetime.utcnow().timestamp())}.csv"
    filepath = os.path.join(export_folder, filename)

    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Company Name",
            "Drive Title",
            "Application Status",
            "Interview Date"
        ])

        for app in applications:
            writer.writerow([
                student_id,
                app.drive.company.company_name,
                app.drive.job_title,
                app.status,
                app.interview_date.strftime("%Y-%m-%d") if app.interview_date else ""
            ])

    msg = MIMEMultipart()
    msg["From"] = "mycomplainto2025@gmail.com"
    msg["To"] = student.user.email
    msg["Subject"] = "Your Placement Application History CSV"

    msg.attach(MIMEText("Please find attached your application history CSV.", "plain"))

    with open(filepath, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("mycomplainto2025@gmail.com", "nfar ipjd fvxp bnwa")
    server.send_message(msg)
    server.quit()

    os.remove(filepath)

    print("CSV exported and emailed.")
    return "CSV generated and emailed"


# CELERY CONFIG (Indian Time Zone)
celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False
)

celery.conf.beat_schedule = {
    "monthly-report-task": {
        "task": "celery_worker.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=9, minute=0),
    },
    "daily-reminder-task": {
        "task": "celery_worker.send_daily_reminders",
        "schedule": crontab(hour=9, minute=0),
    },
}