# 🎓 School Online Classes – Google Meet Integration

A web application that allows schools to conduct online classes using **Google Meet**, where:

- 👨‍🏫 **Admins / Teachers** can create live Google Meet sessions
- 👩‍🎓 **Students** can log in and join ongoing live classes from the same interface
- 🔐 Authentication is handled using **JWT**
- 📅 Meetings are created using **Google Calendar API (Google Meet)**

---


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a54ad534-6922-4daf-bf8e-02b504d40f1e" />


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/704a77cf-7a58-424d-a27c-3397d32aea49" />




## 🚀 Features

### 🔐 Authentication
- Role-based login using JWT
- Two roles:
  - `ADMIN` – Teacher / School Admin
  - `STUDENT` – Student

### 👨‍🏫 Admin Capabilities
- Login securely
- Create Google Meet sessions
- Automatically generate Meet links
- Sessions are stored temporarily (in-memory for demo)

### 👩‍🎓 Student Capabilities
- Login securely
- View **live sessions** created by admin
- Join Google Meet with one click

### 🌐 Unified Interface
- Same UI for Admin & Student
- Features are shown based on role after login

---

## 🧱 Tech Stack

### Backend
- Python
- Flask
- JWT (Authentication)
- Google Calendar API
- OAuth 2.0 (Google)

### Frontend
- HTML
- CSS
- Vanilla JavaScript (Fetch API)

---

## 📁 Project Structure

school-gmeet-integration/
│
├── app.py
├── requirements.txt
├── templates/
│ └── index.html
├── static/
│ ├── css/
│ │ └── style.css
│ └── js/
│ └── app.js
├── .gitignore
└── README.md

yaml
Copy code

---

## 🔑 Demo Credentials (For Testing)

### Admin
Email: admin@school.com
Password: admin123

shell
Copy code

### Student
Email: student1@school.com
Password: student123

yaml
Copy code

---

## 🧪 How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/school-gmeet-integration.git
cd school-gmeet-integration
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv .venv
.venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Google OAuth Setup
Create a Google Cloud project

Enable Google Calendar API

Create OAuth Client (Desktop App)

Download credentials.json

Place it in the project root

⚠️ credentials.json and token.json are ignored via .gitignore

5️⃣ Run the App
bash
Copy code
python app.py
Open browser:

arduino
Copy code
http://127.0.0.1:5000/ui
🔄 Application Flow
Admin Flow
Login as Admin

Create a meeting (subject + time)

Google OAuth popup appears (first time only)

Meet link is generated and session goes live

Student Flow
Login as Student

Click Refresh Live Sessions

See ongoing meetings

Click Join → redirected to Google Meet

⚠️ Important Notes
Meetings are stored in-memory (demo purpose)

On server restart, meetings will be cleared

For production, replace with:

Database (PostgreSQL / MongoDB)

Secure secret storage

Service Account based OAuth

🔐 Security Practices Used
JWT for stateless authentication

Role-based API access

Sensitive files excluded using .gitignore

📈 Future Enhancements
Class / Section based filtering

Database persistence

Attendance tracking

Notifications

Recording management

Deployment on cloud (AWS / GCP / Render)

🧑‍💻 Author
Khasim Abbas
Backend & Product Engineer
📍 India

📄 License
This project is for learning and demonstration purposes.

yaml
Copy code

---

If you want, next I can:
- 🧠 Rewrite this README for **resume/interview**
- 🎥 Help you explain this as a **project walkthrough**
- ☁️ Help you **deploy** it online

Just say **NEXT** 🚀
