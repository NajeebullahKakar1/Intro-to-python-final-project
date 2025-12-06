This project is a Library Management System built using Flask. It allows librarians and library members to manage books and borrowing activities. Users can add, edit, and search books, manage member accounts, check out and return books, and view borrowing history. The system uses Flask for the backend, SQLite for the database, and HTML, CSS, and JavaScript for the frontend.

 Features
- Add new books with title, author, year, language, and details
- Edit book information and manage availability
- Search for books by title, author, language, or year
- Register and manage library members
- Check out and return books
- View borrowing history for users and books
- Login and role-based access for librarians and members


Technologies Used
- Python (Flask)
- SQLite
- HTML, CSS, JavaScript
- Flask-WTF
- Flask-Login
- Flask-Bcrypt
- Jinja Templates
- 

Project Structure
project/
│── app.py
│── database.db
│── requirements.txt
│
├── models/
│   └── models.py
│
├── routes/
│   └── auth.py
│   └── books.py
│   └── users.py
│   └── checkout.py
│
├── templates/
│   └── base.html
│   └── login.html
│   └── add_book.html
│   └── edit_book.html
│   └── search.html
│   └── users.html
│
├── static/
│   └── style.css
│   └── script.js
│
└── tests/
    └── test_app.py

    

Database Schema
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'user'
);

-- Books Table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year TEXT,
    language TEXT,
    available INTEGER DEFAULT 1
);

-- Borrow Table
CREATE TABLE borrow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    book_id INTEGER,
    status TEXT
);



 License / Notes

This project is for educational purposes only.  
All code and content are created by the project group members.  
Do not copy or reuse this project for commercial purposes.
