# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/")
# def home():
#     return {"message": "Leave Management API Running"}

# from fastapi import FastAPI
#
# app = FastAPI()
#
# leaves = []
#
# @app.post("/apply-leave")
# def apply_leave(data: dict):
#     leaves.append(data)
#     return {"message": "Leave Applied", "data": data}
#
# @app.get("/leaves")
# def get_leaves():
#     return leaves
#
# from fastapi import FastAPI
# import sqlite3
#
# app = FastAPI()
#
# DB = "leave.db"
#
# def init_db():
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
#
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS leaves (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         email TEXT,
#         leave_type TEXT,
#         start_date TEXT,
#         end_date TEXT,
#         reason TEXT,
#         status TEXT DEFAULT 'PENDING'
#     )
#     """)
#
#     conn.commit()
#     conn.close()
#
# init_db()
#
#
# @app.post("/apply-leave")
# def apply_leave(data: dict):
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
#
#     cursor.execute("""
#         INSERT INTO leaves (email, leave_type, start_date, end_date, reason)
#         VALUES (?, ?, ?, ?, ?)
#     """, (
#         data["email"],
#         data["leave_type"],
#         data["start_date"],
#         data["end_date"],
#         data["reason"]
#     ))
#
#     conn.commit()
#     conn.close()
#
#     return {"message": "Leave Applied & Saved in DB"}
#
#
# @app.get("/leaves")
# def get_leaves():
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT * FROM leaves")
#     data = cursor.fetchall()
#
#     conn.close()
#     return data

import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DB = "leave.db"

# ================= EMAIL FUNCTION =================
def send_email(to_email, subject, message):
    sender = "bansodeamol511@gmail.com"
    password = "oknzltczsrakyyng"   # ⚠️ Use Gmail App Password

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())
    except Exception as e:
        print("Email error:", e)


# ================= REQUEST MODEL =================
class LeaveRequest(BaseModel):
    email: str
    leave_type: str
    start_date: str
    end_date: str
    reason: str


# ================= DATABASE INIT =================
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        leave_type TEXT,
        start_date TEXT,
        end_date TEXT,
        reason TEXT,
        status TEXT DEFAULT 'PENDING'
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ================= APPLY LEAVE =================
@app.post("/apply-leave")
def apply_leave(data: LeaveRequest):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leaves (email, leave_type, start_date, end_date, reason)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.email,
        data.leave_type,
        data.start_date,
        data.end_date,
        data.reason
    ))

    conn.commit()

    # ✅ Email to HR
    send_email(
        "hr@gmail.com",   # change this
        "New Leave Request",
        f"""
New Leave Request:

Employee: {data.email}
Type: {data.leave_type}
From: {data.start_date}
To: {data.end_date}
Reason: {data.reason}
"""
    )

    conn.close()

    return {"message": "Leave Applied & Email Sent to HR"}


# ================= GET ALL LEAVES =================
@app.get("/leaves")
def get_leaves():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leaves")
    data = cursor.fetchall()

    conn.close()
    return data


# ================= APPROVE / REJECT =================
@app.post("/update-leave/{leave_id}")
def update_leave(leave_id: int, status: str):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM leaves WHERE id=?", (leave_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return {"error": "Leave not found"}

    status = status.upper()
    if status not in ["APPROVED", "REJECTED"]:
        conn.close()
        return {"error": "Use APPROVED or REJECTED"}

    cursor.execute("UPDATE leaves SET status=? WHERE id=?", (status, leave_id))
    conn.commit()

    # ✅ Email to Employee
    send_email(
        user[0],
        "Leave Status Update",
        f"Your leave request has been {status}"
    )

    conn.close()

    return {"message": f"Leave {status}"}