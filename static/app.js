// ================= GLOBAL STATE =================
let token = null;
let role = null;

// ================= DOM ELEMENTS =================
const loginBtn = document.getElementById("loginBtn");
const logoutBtn = document.getElementById("logoutBtn");
const createMeetingBtn = document.getElementById("createMeetingBtn");
const refreshBtn = document.getElementById("refreshBtn");

const adminSection = document.getElementById("admin-section");
const meetingList = document.getElementById("meetingList");

// ================= LOGIN =================
loginBtn.addEventListener("click", login);
logoutBtn.addEventListener("click", logout);
createMeetingBtn.addEventListener("click", createMeeting);
refreshBtn.addEventListener("click", loadLiveMeetings);

function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Please enter email and password");
        return;
    }

    fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.token) {
            alert(data.message || "Login failed");
            return;
        }

        token = data.token;
        role = data.role;

        alert(`Logged in as ${role}`);

        // Role-based UI
        if (role === "ADMIN") {
            adminSection.style.display = "block";
        } else {
            adminSection.style.display = "none";
        }

        loadLiveMeetings();
    })
    .catch(err => {
        console.error(err);
        alert("Login error");
    });
}

// ================= LOGOUT =================
function logout() {
    token = null;
    role = null;
    adminSection.style.display = "none";
    meetingList.innerHTML = "";
    alert("Logged out");
}

// ================= CREATE MEETING (ADMIN) =================
function createMeeting() {
    const title = document.getElementById("title").value;
    const start_time = document.getElementById("start_time").value;
    const end_time = document.getElementById("end_time").value;

    if (!title || !start_time || !end_time) {
        alert("Please fill all meeting fields");
        return;
    }

    fetch("/admin/create-meeting", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            title,
            start_time,
            end_time
        })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.meet_link) {
            alert("Meeting creation failed");
            return;
        }

        alert("Meeting created successfully!");
        window.open(data.meet_link, "_blank");

        loadLiveMeetings();
    })
    .catch(err => {
        console.error(err);
        alert("Error creating meeting");
    });
}

// ================= LOAD LIVE MEETINGS =================
function loadLiveMeetings() {
    if (!token) {
        alert("Please login first");
        return;
    }

    fetch("/student/live-meetings", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        meetingList.innerHTML = "";

        if (!data.live_sessions || data.live_sessions.length === 0) {
            meetingList.innerHTML = "<li>No live sessions</li>";
            return;
        }

        data.live_sessions.forEach(m => {
            const li = document.createElement("li");
            li.innerHTML = `
                <span>${m.title}</span>
                <button onclick="joinMeeting('${m.meet_link}')">Join</button>
            `;
            meetingList.appendChild(li);
        });
    })
    .catch(err => {
        console.error(err);
        alert("Failed to load meetings");
    });
}

// ================= JOIN MEETING =================
function joinMeeting(link) {
    window.open(link, "_blank");
}
