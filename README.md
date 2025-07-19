# 💸 Expense Tracker Web App

A full-featured web application to track your personal expenses. Built with Django, this app allows users to register, log in, and manage their income and expenses through a user-friendly dashboard with visual charts and category/month filters.

---

## 🚀 Features

- 🔐 **User Authentication** – Secure login, logout, and registration system.
- 📊 **Dashboard View** – Interactive dashboard with filtering by month and category.
- 📁 **Transaction Management** – Add, edit, and delete income/expense records.
- 📅 **Monthly Insights** – Visual breakdown using bar and pie charts (Chart.js).
- 🎯 **Category-wise Analysis** – Track how you're spending your money by category.
- 🧾 **Responsive UI** – Clean and simple interface, enhanced with Bootstrap.

---

## 🛠️ Tech Stack

| Technology | Description                     |
|------------|---------------------------------|
| Django     | Web framework for backend logic |
| Python     | Server-side programming         |
| HTML/CSS   | Frontend structure and styling  |
| SQLite     | Lightweight development database|
| Chart.js   | Chart rendering in the dashboard|

---

## 🔧 Installation

1. **Clone the repository**

git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

2. **Create and activate virtual environment**

python -m venv env
env\Scripts\activate  # for Windows

3. **Install dependencies**

pip install -r requirements.txt

4. **Run migrations**

python manage.py makemigrations
python manage.py migrate

5. **Start the development server**

python manage.py runserver

6. **Visit in browser**

http://127.0.0.1:8000/