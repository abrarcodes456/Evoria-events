# 🏛️ EVORIA Events — Venue Booking Web Application

> *"Where Every Moment Becomes a Memory"*

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-6.0.4-green?style=for-the-badge&logo=django)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge)

---

## 📌 About The Project

**EVORIA Events** is a full-stack venue booking web application built using **Python Django**. It allows customers to book a premium event venue located in **Theni, Tamil Nadu** for various celebrations including weddings, birthdays, corporate events, and more.

This is a real-world business project demonstrating complete web application development from database design to deployment.

---

## ✨ Features

### 👤 User Features
- Register and login with secure authentication
- Book venue with event type selection
- Dynamic catering price toggle (JavaScript — no page refresh)
- Date conflict detection — prevents double booking
- View all personal bookings
- Cancel confirmed bookings
- Contact us form with message

### 🔧 Admin Features
- Secure admin dashboard (staff only)
- Real-time booking statistics
  - Total users, Total bookings
  - Confirmed, Upcoming, Completed events
- View and manage all bookings
- Update booking status (confirmed/completed/cancelled)
- View all registered users
- Read contact messages with read/unread status

### ⚙️ Automatic Features
- Bookings auto-confirmed on submission
- Past events auto-marked as completed
- Date conflict detection and blocking
- Automated email notifications via Gmail SMTP

---

## 📧 Email Notifications

| Email | Trigger |
|---|---|
| Booking Confirmation | When user books venue |
| Booking Cancellation | When booking is cancelled |
| Contact Message | When user submits contact form |

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python, Django 6.0.4 |
| Database | SQLite + Django ORM |
| Frontend | HTML5, CSS3, JavaScript |
| Authentication | Django Auth System |
| Email | Gmail SMTP |
| Fonts | Google Fonts (Playfair Display + Poppins) |
| Deployment | Railway.app |
| Version Control | Git + GitHub |

---

## 💰 Pricing

| Package | Price |
|---|---|
| Without Catering | ₹35,000/day |
| With Catering | ₹55,000/day |

---

## 📁 Project Structure

```
EVORIA/
├── evoria/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venue/
│   ├── models.py        # Booking, UserProfile, ContactMessage
│   ├── views.py         # 12 view functions
│   ├── urls.py          # 12 URL patterns
│   ├── admin.py
│   ├── templates/       # 10 HTML templates
│   └── static/          # CSS + images
├── requirements.txt
├── Procfile
├── runtime.txt
└── manage.py
```

---

## 🗄️ Database Models

### UserProfile
Extends Django User with phone number using OneToOne relationship.

### Booking
Stores all event booking details with ForeignKey to User.
Fields: `event_type`, `event_name`, `event_date`, `guest_count`, `phone`, `catering`, `special_requests`, `total_price`, `status`, `created_at`

### ContactMessage
Stores contact form submissions.
Fields: `name`, `email`, `phone`, `subject`, `message`, `is_read`, `created_at`

---

## 🚀 Local Setup

```bash
# Clone the repository
git clone https://github.com/abrarcodes456/Evoria-events.git
cd Evoria-events

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file with your secrets
# EMAIL_PASSWORD=your-gmail-app-password
# SECRET_KEY=your-django-secret-key
# DEBUG=True

# Run migrations
python manage.py migrate

# Run the server
python manage.py runserver
```

---

## 🌐 Live Demo

🔗 **[View Live App](https://evoria-events.onrender.com)**

---

## 📸 Django Concepts Used

- Models with ForeignKey and OneToOneField relationships
- Function Based Views (12 views)
- URL routing and template inheritance
- Django ORM for database queries
- `@login_required` and `@user_passes_test` decorators
- Messages framework and CSRF protection
- Static files with Whitenoise
- Environment variables with python-dotenv

---

## 👨‍💻 Developer

**Abrar Shaukathali**
- 🎓 B.Sc Computer Science — Mother Theresa Arts and Science College, Theni
- 💼 Python Developer | Django | Machine Learning
- 📍 Theni, Tamil Nadu, India
- 🔗 [GitHub](https://github.com/abrarcodes456)

---

## 📄 License

This project is for portfolio and demonstration purposes.

---

*by Abrar Shaukathali*
