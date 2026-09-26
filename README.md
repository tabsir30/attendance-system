# 📍 ATTENZO

### Smart Attendance System

> A modern Flutter-based attendance platform for educational institutions, combining **QR authentication, GPS verification, face recognition, and real-time attendance tracking**.

---

## 🚀 Features

- 👨‍🏫 Teacher & Student Login
- 📱 Flutter-based Android application
- 🔐 JWT-based authentication
- 📸 Teacher face verification
- 📍 GPS-based location verification
- 🎯 Teacher-controlled class sessions
- 🔄 Dynamic QR codes for attendance
- 👨‍🎓 Student QR scanning
- 📊 Subject-wise attendance percentage
- ⚠️ Low-attendance detection
- 📝 Attendance history
- ⚡ FastAPI backend
- 🗄️ SQLite database

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| 📱 Frontend | Flutter, Dart |
| ⚙️ Backend | Python, FastAPI |
| 🗄️ Database | SQLite, SQLAlchemy |
| 🔐 Authentication | JWT |
| 📍 Location | Geolocator |
| 📷 Face Verification | Face Recognition |
| 🔳 QR System | QR Flutter, Mobile Scanner |
| 🌐 API Communication | Dio |
| 💻 Development | Android Studio, VS Code |

---

## 📂 Project Structure

```text
Attendx/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── database/
│   └── requirements.txt
│
├── frontend/
│   ├── android/
│   ├── assets/
│   ├── lib/
│   └── pubspec.yaml
│
├── .gitignore
└── README.md
```

---

# ⚙️ Setup & Installation

## 1️⃣ Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Attendx
```

---

## 2️⃣ Backend Setup

The backend is developed using **FastAPI** and was run locally through **VS Code**.

Open the `backend` folder in VS Code.

### Create Virtual Environment

```powershell
cd backend
python -m venv venv
```

### Activate Virtual Environment

```powershell
venv\Scripts\activate
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Start FastAPI Server

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will run on:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 📱 3️⃣ Flutter Frontend Setup

The frontend is built using **Flutter** and can be developed/run through **Android Studio**.

Open the `frontend` folder in Android Studio.

### Install Flutter Dependencies

```powershell
flutter pub get
```

### Check Connected Devices

```powershell
flutter devices
```

### Run the Application

```powershell
flutter run
```

You can run ATTENZO on:

- 🤖 Android Emulator
- 📱 Physical Android Device

---

# 🌐 4️⃣ Backend URL Configuration

Open:

```text
frontend/lib/api.dart
```

The backend URL must match the device you are using.

### 🤖 Android Emulator

Use:

```text
http://10.0.2.2:8000
```

### 📱 Physical Android Device

Use your computer's local network IP:

```text
http://192.168.x.x:8000
```

For example:

```text
http://192.168.20.168:8000
```

> ⚠️ When using a physical Android device, the phone and computer must be connected to the same Wi-Fi network.

---

# 🔄 Running ATTENZO

The recommended development setup is:

```text
┌──────────────────────┐
│       VS Code        │
│                      │
│   FastAPI Backend    │
│      Port 8000       │
└──────────┬───────────┘
           │
           │ API
           ▼
┌──────────────────────┐
│    Flutter App       │
│                      │
│  Android Emulator    │
│          OR          │
│  Physical Android    │
└──────────────────────┘
```

For testing the complete attendance workflow:

```text
👨‍🏫 Teacher
     │
     ▼
Start Class Session
     │
     ▼
Generate Dynamic QR
     │
     ▼
👨‍🎓 Student
     │
     ▼
Scan QR Code
     │
     ▼
📍 GPS Verification
     │
     ▼
✅ Attendance Marked
     │
     ▼
📊 Attendance Percentage
```

---

# 🔐 Security

Do **not** commit sensitive information to GitHub.

Make sure the following remain ignored:

```text
.env
*.db
venv/
.dart_tool/
build/
*.jks
*.keystore
credentials.json
service-account.json
```

Never upload:

- 🔑 Passwords
- 🔐 Secret keys
- 🗄️ Production databases
- 📸 Private face images
- 📜 API credentials
- 🔏 Android signing keys

---

# 🧪 Development Notes

Before running the Flutter application, make sure the FastAPI backend is running.

If the backend IP address changes, update the API configuration in:

```text
frontend/lib/api.dart
```

Then restart the Flutter application.

---

# 🏆 Project

**ATTENZO — Smart Attendance System**

Built with ❤️ using **Flutter + FastAPI**

> Making classroom attendance smarter, faster, and more secure.
