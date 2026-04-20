# 📸 Instagram Giveaway Comment Picker

A modern, full-stack web application for picking giveaway winners from Instagram comments. Built with a high-performance **Django** backend and a beautiful **Next.js** glassmorphism frontend.

## ✨ Features
- 🔗 **Instagram Integration**: Paste any public Instagram Post or Reel URL.
- 🕷️ **AI-Powered Scraper**: Uses Playwright to intelligently scroll and fetch the most liked comments.
- 🏆 **Top 10 Display**: View the most popular comments based on like count.
- 🎲 **Random Winner Picker**: Select a winner with a vibrant confetti celebration.
- ☁️ **Hybrid Persistence**:
  - **SQLite**: Securely handles logins and admin data.
  - **MongoDB Atlas**: Scalable cloud storage for scraped comment history.
- 🛡️ **Secure Deployment**: Fully configured with `.env` secrets and `.gitignore`.

## 🛠️ Tech Stack
- **Frontend**: Next.js 16 (App Router), Tailwind CSS v4, Lucide Icons, Canvas Confetti.
- **Backend**: Django 6.0, Django REST Framework, Playwright (Chromium).
- **Database**: Hybrid (SQLite + MongoDB Atlas).

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
playwright install chromium
python manage.py migrate
python manage.py runserver
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Environment Variables
Create a `backend/.env` file:
```env
SECRET_KEY=your_django_key
MONGO_HOST=your_mongodb_atlas_url
MONGO_DB_NAME=comment_picker
```

## 📜 License
MIT
