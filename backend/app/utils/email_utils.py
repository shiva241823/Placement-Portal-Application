import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "example@gmail.com"       # change this
SENDER_PASSWORD = "nfar ewer ipjd fvxp bnwa"       # change this


def send_email(to_email, subject, html_content):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email}")

    except Exception as e:
        print("Email sending failed:", str(e))


# ==============================
# MONTHLY REPORT MAIL
# ==============================
def send_monthly_report(admin_email, total_drives, total_applications, total_selected):

    html = f"""
    <h2>Monthly Placement Report</h2>
    <p>Total Drives Conducted: {total_drives}</p>
    <p>Total Applications: {total_applications}</p>
    <p>Total Selected Students: {total_selected}</p>
    """

    send_email(admin_email, "Monthly Placement Report", html)


# ==============================
# DEADLINE REMINDER MAIL
# ==============================
def send_deadline_reminder(student_email, drive_title, deadline):

    html = f"""
    <h3>Placement Drive Reminder</h3>
    <p>The drive <b>{drive_title}</b> is closing on {deadline}.</p>
    <p>Please apply before deadline.</p>
    """

    send_email(student_email, "Drive Deadline Reminder", html)