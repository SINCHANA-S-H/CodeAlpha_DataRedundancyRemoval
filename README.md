# CodeAlpha Data Redundancy Removal System

A Flask-based web application that detects and prevents duplicate records using SHA-256 hashing and SQLite database validation.

## 📌 Project Overview

The Data Redundancy Removal System is designed to identify duplicate data records before they are stored in the database.

The application generates a unique SHA-256 hash for each record and compares it with existing records. If the same data is submitted again, the system detects it as a duplicate and prevents redundant storage.

## 🚀 Features

- Duplicate data detection
- SHA-256 hashing for record verification
- SQLite database integration
- Add and store unique records
- Search existing records
- Real-time duplicate alerts
- Clean and responsive web interface
- Secure handling of ignored local files using `.gitignore`

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **SQLite**
- **HTML5**
- **CSS3**
- **SHA-256 Hashing**
- **Git & GitHub**

## 📂 Project Structure

```text
CodeAlpha_DataRedundancyRemoval/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── pyrightconfig.json
│
├── templates/
│   └── index.html
│
└── static/
    └── css/
        └── style.css