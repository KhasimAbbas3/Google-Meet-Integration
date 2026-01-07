from flask import Flask, request, jsonify, render_template
import jwt
import datetime
from functools import wraps
import uuid
import os
import traceback

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

app = Flask(__name__)

# =====================================================
# JWT CONFIG
# =====================================================
JWT_SECRET = "super-secret-key"
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 60

# =====================================================
# USERS (DEMO)
# =====================================================
users = [
    {"id": 1, "email": "admin@school.com", "password": "admin123", "role": "ADMIN"},
    {"id": 2, "email": "student1@school.com", "password": "student123", "role": "STUDENT"},
]

# =====================================================
# IN-MEMORY MEETINGS (ADMIN → STUDENT)
# =====================================================
meetings = []

# =====================================================
# JWT HELPERS
# =====================================================
def generate_token(user):
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXP_MINUTES)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token.decode() if isinstance(token, bytes) else token


def token_required(required_role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization")

            if not auth or not auth.startswith("Bearer "):
                return jsonify({"message": "Token missing"}), 401

            token = auth.split(" ")[1]

            try:
                decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401

            if required_role and decoded["role"] != required_role:
                return jsonify({"message": "Access denied"}), 403

            request.user = decoded
            return f(*args, **kwargs)
        return wrapper
    return decorator

# =====================================================
# GOOGLE CALENDAR CONFIG
# =====================================================
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

# =====================================================
# UI ROUTE (THIS WAS MISSING)
# =====================================================
@app.route("/")
@app.route("/ui")
def ui():
    return render_template("index.html")

# =====================================================
# AUTH
# =====================================================
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    for user in users:
        if user["email"] == data.get("email") and user["password"] == data.get("password"):
            return jsonify({
                "token": generate_token(user),
                "role": user["role"]
            }), 200

    return jsonify({"message": "Invalid credentials"}), 401

# =====================================================
# ADMIN: CREATE MEETING
# =====================================================
@app.route("/admin/create-meeting", methods=["POST"])
@token_required("ADMIN")
def create_meeting():
    data = request.get_json(silent=True)

    try:
        service = get_calendar_service()

        event = {
            "summary": data.get("title", "Online Class"),
            "start": {
                "dateTime": data["start_time"] + ":00",
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": data["end_time"] + ":00",
                "timeZone": "Asia/Kolkata"
            },
            "conferenceData": {
                "createRequest": {
                    "requestId": str(uuid.uuid4())
                }
            }
        }

        created = service.events().insert(
            calendarId="primary",
            body=event,
            conferenceDataVersion=1
        ).execute()

        meet_link = created["conferenceData"]["entryPoints"][0]["uri"]

        meetings.append({
            "id": str(uuid.uuid4()),
            "title": event["summary"],
            "start_time": data["start_time"],
            "end_time": data["end_time"],
            "meet_link": meet_link
        })

        return jsonify({"meet_link": meet_link}), 201

    except Exception:
        traceback.print_exc()
        return jsonify({"message": "Meeting creation failed"}), 500

# =====================================================
# STUDENT: VIEW LIVE MEETINGS
# =====================================================
@app.route("/student/live-meetings", methods=["GET"])
@token_required("STUDENT")
def student_live_meetings():
    now = datetime.datetime.now()
    live = []

    for m in meetings:
        start = datetime.datetime.fromisoformat(m["start_time"])
        end = datetime.datetime.fromisoformat(m["end_time"])

        if start <= now <= end:
            live.append(m)

    return jsonify({"live_sessions": live}), 200

# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:5000/ui")
    app.run(debug=True)
