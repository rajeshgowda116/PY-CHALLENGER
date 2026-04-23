# 🚀 PY Challenger

PY Challenger is a Python coding challenge platform designed to help users practice Python from **basic to advanced levels** while tracking their **progress, streaks, and consistency**.

---

## 🌟 Features

* 🔐 User Authentication (Login / Register)
* 📊 Dashboard with:

  * Daily streak 🔥
  * Problems solved
  * Coding activity
* 📚 Topic-wise problem sections:

  * Python Basics
  * Strings
  * Lists
  * Loops
  * Functions
  * OOP
* 🧠 Coding Problems:

  * Beginner → Advanced
* 🧪 Test Cases support
* 🖥 Code Editor (for solving problems)
* 📈 Progress tracking system
* 🏆 (Optional) Leaderboard

---

## 🛠 Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite (Development)
* PostgreSQL (Production)

### Tools

* Monaco Editor (Code Editor)
* Judge0 API (Code Execution)

---

## 📂 Project Structure

```
pychallenger/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│
├── apps/
│   ├── users/
│   ├── problems/
│   ├── submissions/
│
├── templates/
├── static/
```

---

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/pychallenger.git
cd pychallenger
```

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply migrations

```bash
python manage.py migrate
```

5. Run server

```bash
python manage.py runserver
```

---

## 🔑 Admin Access

Create superuser:

```bash
python manage.py createsuperuser
```

Access admin panel:

```
http://127.0.0.1:8000/admin
```

---

## 📌 Future Improvements

* AI Hint System 🤖
* Daily Challenge 🔥
* Leaderboard 🏆
* Code execution sandbox (Docker)
* Multi-language support

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Commit changes
4. Push and create PR

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 💡 Author

Developed by **Rajesh Gouda**

---

⭐ If you like this project, give it a star!
