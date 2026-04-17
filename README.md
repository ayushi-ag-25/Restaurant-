# 🏨 BestBliss Hotel — Table Booking System

> *A full-stack web application for hotel table reservations, built with Flask & MySQL*

<!-- Replace above with your actual banner/screenshot -->

---

## 🌐 Live Demo

> **Deployed URL:** ``

---

## 📸 Preview

| Page | Screenshot |
|------|------------|
| 🏠 Home | ![Home]() |
| 🔐 Login | ![Login]() |
| 📋 Dashboard | ![Dashboard]() |
| 📅 Booking | ![Booking]() |
| 👤 Profile | ![Profile]() |

<!-- Add your screenshots inside the img tags above -->

---

## ✨ Features

- 🔐 **User Authentication** — Register, Login, Logout with session management
- 📅 **Table Booking** — Book different table types with date, time & special requests
- 📜 **Booking History** — View all past reservations
- ⭐ **Feedback System** — Submit ratings and reviews
- 👤 **User Profile** — View and edit personal information
- 🔒 **Route Protection** — All private pages protected with login check decorator
- 📵 **No-Cache Headers** — Prevents browser back button after logout
- 📱 **Responsive Design** — Works on mobile, tablet and desktop

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript, Tailwind CSS |
| DB Connector | mysql-connector-python |
| Deployment | Railway / Render / Any WSGI host |

---

## 📁 Project Structure

```
BestBliss/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
│
├── static/
│   ├── s.css               # Main stylesheet
│   ├── j.js                # JavaScript file
│   ├── book.jpg            # Booking page image
│   ├── cas.jpg             # Casual dining image
│   ├── met.jpg             # Meeting room image
│   ├── rof.gif             # Rooftop image
│   ├── f.jpg               # Function hall image
│   ├── cc3.png             # Dashboard banner
│   └── tile.png            # Dashboard background
│
└── templates/
    ├── hote.html           # Home / Landing page
    ├── hotelloginpage.html # Login page
    ├── register.html       # Registration page
    ├── dashboard.html      # User dashboard
    ├── booking.html        # Table booking form
    ├── historybook.html    # Booking history
    ├── feedback.html       # Feedback form
    ├── profile.html        # User profile
    └── editprofile.html    # Edit profile
```

---

## 🗄️ Database Schema

### `LOGIN` Table
| Column | Type | Description |
|--------|------|-------------|
| ID | INT (PK, AUTO) | Unique user ID |
| GENDER | VARCHAR(10) | Male / Female / Other |
| MOBILE | BIGINT (UNIQUE) | Mobile number (used as username) |
| PASSWORD | VARCHAR(50) | User password |
| NAME | VARCHAR(20) | Full name |
| MAIL | VARCHAR(50) | Email address |

### `BOOKINGS` Table
| Column | Type | Description |
|--------|------|-------------|
| BID | INT (PK, AUTO) | Booking ID |
| ID | INT | User ID (foreign ref) |
| NAME | VARCHAR(20) | Guest name |
| MOBILE | BIGINT | Guest mobile |
| DOC | DATE | Date of booking |
| TOC | TIME | Time of booking |
| TABLETYPE | VARCHAR(30) | Type of table |
| REQUEST | VARCHAR(500) | Special requests |

### `FEEDBACKS` Table
| Column | Type | Description |
|--------|------|-------------|
| FID | INT (PK, AUTO) | Feedback ID |
| ID | INT | User ID (foreign ref) |
| NAME | VARCHAR(20) | User name |
| MOBILE | BIGINT | User mobile |
| RATE | INT | Rating (1–5) |
| FEEDBACK | VARCHAR(500) | Feedback message |

---

## ⚙️ Local Setup Guide

### Prerequisites

Make sure you have the following installed:
- Python 3.8+
- MySQL Server
- pip

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/bestbliss-hotel.git
cd bestbliss-hotel
```

---

### Step 2 — Create Virtual Environment

```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:

```bash
pip install flask mysql-connector-python
```

---

### Step 4 — Set Up MySQL Database

Open MySQL and create a database:

```sql
CREATE DATABASE bestbliss;
```

The tables will be **created automatically** when you run the app for the first time (`init_db()` runs on startup).

---

### Step 5 — Configure Environment Variables

Create a `.env` file in the root folder:

```env
SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=bestbliss
DB_PORT=3306
```

> ⚠️ Never commit `.env` to GitHub! Add it to `.gitignore`

---

### Step 6 — Run the Application

```bash
python app.py
```

Visit: **http://127.0.0.1:5000**

---

## 🔐 Authentication Flow

```
User visits /book (login page)
        ↓
Enters mobile number + password
        ↓
AJAX fetch → POST /check
        ↓
Flask checks MySQL LOGIN table
        ↓
✅ Match → session created → redirect /dashboard
❌ No match → error message shown
```

Session stores:
- `session['userid']` — user's ID
- `session['name']` — user's name

---

## 🛡️ Route Protection

A custom `@checklogin` decorator protects private routes:

```python
@checklogin
def dashboard():
    ...
```

If not logged in → redirected to `/book` (login page)

Protected routes:
- `/dashboard`
- `/bookpage`
- `/booking`
- `/history`
- `/feedback`
- `/feedsave`
- `/profile`
- `/editprofile`
- `/changeprofile`

---

## 📋 Table Types Available

| Type | Price |
|------|-------|
| 🍽️ Casual Dinner Tables | ₹200 / table |
| 🤝 Guest Meetings | ₹500 / table |
| 🌃 Rooftop Party | ₹1000 / table |
| 🎉 Function Halls | ₹2500 / table |

---

## 🚀 Deployment Guide (Railway)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and create a new project
3. Connect your GitHub repository
4. Add a MySQL plugin in Railway
5. Set environment variables in Railway dashboard:
   - `SECRET_KEY`
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
   - `DB_PORT`
6. Railway auto-detects Flask and deploys!

> Make sure `init_db()` is called at startup — it's already handled in `app.py` ✅

---

## 📦 requirements.txt

```
flask
mysql-connector-python
gunicorn
```

---

## 🙋 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your@email.com

---

## 📄 License

This project is for educational/personal use.

---

*Made with ❤️ for BestBliss Hotel*
