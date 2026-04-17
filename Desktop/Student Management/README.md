# 🎓 Smart Student Management System (Flask Web App)

A full-stack, role-based web application built using Flask that allows efficient management of student records, academic performance, and secure user access.

This project upgrades a console-based system into a modern web application with authentication, analytics, and a clean user interface.

---

## 🚀 Features

### 🔐 Authentication & Security
- Role-based login (Admin & Student)
- Password hashing using Werkzeug
- Strong password validation (uppercase, lowercase, numbers)
- First-time login password change enforcement
- Admin-controlled password reset system

---

### 👨‍🏫 Admin Features
- Add new students (auto user account creation)
- View all students in a structured table
- Search by ID or name
- Update student details (with skip option)
- Delete student records
- Reset student passwords
- Sort students by name or percentage

---

### 👨‍🎓 Student Features
- Login using Student ID
- View personal details
- View performance report
- Change password securely

---

### 📊 Performance & Analytics
- Subject-wise marks tracking
- Automatic calculation of:
  - Total
  - Percentage
  - Grade
- Visual charts using Chart.js
- Statistics:
  - Average marks
  - Highest score
  - Lowest score

---

### 🗂️ Data Management
- Persistent storage using JSON files (`data.txt`, `users.txt`)
- Auto-sync between file and application
- Handles duplicate and invalid entries

---

### ⚠️ Error Handling & Validation
- Input validation for all fields
- Marks range check (0–100)
- Prevents empty inputs
- Handles missing records gracefully

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, Bootstrap
- **Database:** JSON (File Handling)
- **Charts:** Chart.js
- **Security:** Werkzeug (Password Hashing)

---

## 📁 Project Structure
project/
│
├── app.py
├── model.py
├── service.py
├── auth.py
├── data.txt
├── users.txt
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── dashboard.html
│ ├── add_student.html
│ ├── view.html
│ ├── update.html
│ ├── report.html
│ ├── search.html
│ ├── change_password.html
│ └── force_change.html


---
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

bash
git clone https://github.com/your-username/student-management.git
cd student-management

### 2️⃣ Install Dependencies
pip install flask

### 3️⃣ Run the Application
python app.py

### 4️⃣ Open in Browser
http://127.0.0.1:5000/

### 🔑 Default Credentials
Admin
Username: Nanisha
Password: python

Username: Preetha
Password: sql

Student
Login using Student ID
Default password: 1234
Must change password on first login

### 🔐 Password Security
Passwords are stored using hashing (Werkzeug)
Cannot be retrieved once stored
Admin can reset passwords to default

### 📊 Sample Functional Flow
Admin logs in
Adds a student
System auto-creates user account
Student logs in using ID
Forced password change
Student views report with chart

### 🧠 Key Concepts Used
Object-Oriented Programming (OOP)
File Handling (JSON)
CRUD Operations
Role-Based Access Control
Exception Handling
Data Visualization

### 🎯 Highlights
Clean UI with Bootstrap
Secure authentication system
Real-time data updates
Analytical reports with charts
Modular and scalable design

### 🚀 Future Enhancements
Export reports (PDF/CSV)
Dashboard analytics
Database integration (MySQL)
Email-based password reset
Graphical dashboard charts

### 🏆 Conclusion

This project demonstrates a complete student management system with secure authentication, structured data handling, and analytical reporting using Flask.
