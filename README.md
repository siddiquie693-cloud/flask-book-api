# 📚 Flask Book API

A production-ready RESTful API built with Flask that supports user authentication, role-based authorization, and full CRUD operations for managing books.

---

## 🚀 Features

* 🔐 JWT-based Authentication (Login & Register)
* 👤 Role-Based Access Control (Admin/User)
* 📖 CRUD Operations for Books
* 🔍 Search & Pagination Support
* 📝 Logging System
* 🗄️ SQLite Database Integration

---

## 🛠️ Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Bcrypt
* PyJWT
* SQLite

---

## 📂 Project Structure

```
flask-book-api/
│
├── app.py            # Main application file
├── models.py         # Database models
├── auth.py           # Authentication & authorization logic
├── requirements.txt  # Dependencies
├── README.md         # Project documentation
├── .gitignore        # Ignored files
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/flask-book-api.git
cd flask-book-api
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:5000
```

---

## 🔑 Authentication

### Register User

**POST /register**

```json
{
  "username": "user1",
  "password": "123456",
  "role": "admin"
}
```

### Login

**POST /login**

```json
{
  "username": "user1",
  "password": "123456"
}
```

Response:

```json
{
  "token": "your_jwt_token"
}
```

Use this token in headers:

```
Authorization: Bearer <token>
```

---

## 📚 API Endpoints

### 📖 Get Books

**GET /books**

* Query Params:

  * `search` (optional)
  * `page` (default: 1)
  * `limit` (default: 5)

---

### ➕ Add Book (Admin Only)

**POST /books**

```json
{
  "title": "Book Name",
  "author": "Author Name"
}
```

---

### ✏️ Update Book (Admin Only)

**PUT /books/{id}**

---

### ❌ Delete Book (Admin Only)

**DELETE /books/{id}**

---

## 📝 Logging

All important actions such as user registration, login, and book operations are logged in:

```
app.log
```

## 🔮 Future Improvements

* Swagger / API Documentation
* Docker Support
* Deployment (AWS / Render)
* Unit Testing

---

👨‍💻 Author

MD Sahil Siddiquie
GitHub: https://github.com/siddiquie693-cloud
---

## ⭐ If you like this project

Give it a star on GitHub ⭐
