"""
Flask Library Management System Documentation
This document outlines the specifications and functionality of a Flask-based Library Management System. The application utilizes SQLite as the database. It allows users to register, log in, manage books, and maintain their user sessions.
Technologies Used
- Flask: A micro web framework for Python.
- SQLite: A lightweight database for storing user and book information.
- Werkzeug: A library for password hashing and security.
Application Setup
Prerequisites:
Before running the application, make sure you have the following installed:
- Python (version 3.x)
- Flask
- SQLite
Installation
1. Clone the repository containing the app code:
   bash
   git clone <repository-url>
2. Navigate to the directory:
   bash
   cd <repository-directory>
3. Install the required packages:
   bash
   pip install Flask Werkzeug
4. Create the SQLite database:
   bash
   touch library.db
   
Main Functionalities
User Registration
- Route: /register
- Method: GET, POST
- Function: Allows new users to register by submitting a username and password. Passwords are hashed for security.
User Login
- Route: /login
- Method: GET, POST
- Function: Authenticates users through their credentials. Successful logins create a session for the user.
User Dashboard
- Route: /dashboard
- Method: GET
- Function: Displays the user's dashboard once logged in. Only accessible to authenticated users.
User Logout
- Route: /logout
- Method: POST
- Function: Ends the user's session and redirects them to the login page.
Security Features
- Password Hashing*: Uses werkzeug.security to hash passwords during registration and verifies them during login.
- Session Management: Flask's built-in session management to handle user logins securely.
"""
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB = "library.db"

# ---------------------- HELPERS ----------------------
"""
This document details the specific functions used in the Flask-based Library Management System, highlighting their purpose and how they interact within the application.
Function Specifications
1. query(sql, params=(), fetchone=False, fetchall=False)
Purpose: Executes a given SQL query against the SQLite database and handles the results based on the specified parameters.
Parameters:
- sql (str): The SQL query to be executed.
- params (tuple, optional): A sequence of parameters to use in the SQL query. Default is an empty tuple.
- fetchone (bool, optional): If True, fetches a single result row. Default is False.
- fetchall (bool, optional): If True, fetches all result rows. Default is False.
Returns:
- A single row (as a dictionary) if fetchone is True.
- A list of rows (as dictionaries) if fetchall is True.
- None if neither is specified.
2. login_required(f)
Purpose: A decorator to ensure that the user is authenticated before accessing certain routes. It checks for the username in the session.
Parameters:
- f (function): The original function that needs the authentication requirement.
Returns:
- The wrapped function if the user is authenticated.
- Redirects to the login page if the user is not authenticated.
3. admin_required(f)
Purpose: A decorator that restricts access to specific routes, ensuring that only users with the admin role in their session can access the decorated function.
Parameters:
- f (function): The original function that needs to be restricted to admins.

Returns:
- The wrapped function if the user has admin privileges.
- A 403 Forbidden response if the user is not an admin.
"""

def query(sql, params=(), fetchone=False, fetchall=False):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    if fetchone:
        return cur.fetchone()
    if fetchall:
        return cur.fetchall()
    return None

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapped

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "role" not in session or session["role"] != "admin":
            return "Admins only", 403
        return f(*args, **kwargs)
    return wrapped

# ---------------------- INIT DB ----------------------
"""
This document provides an overview of the init_db function used in the Flask-based Library Management System, along with a detailed description of the database schema it creates. The function sets up the necessary tables to manage users, books, and borrowing transactions.
Function Specification
init_db()
Purpose: Initializes the SQLite database by creating the required tables for the Library Management System if they do not already exist. 
Database Tables Created:
1. Users Table
   - Description:
     - id: A unique identifier for each user (Primary Key, Auto-incremented).
     - username: A unique username for each user (Text).
     - password: The user's hashed password (Text).
     - role: The user's role in the system (Text; default is 'user').

2. Books Table
   - Description:
     - id: A unique identifier for each book (Primary Key, Auto-incremented).
     - title: The title of the book (Text).
     - author: The author of the book (Text).
     - year: The publication year of the book (Text).
     - language: The language in which the book is written (Text).
     - available: A flag indicating if the book is available for borrowing (Integer; default is 1).


3. Borrow Table
   - Description:
     - id: A unique identifier for each borrowing record (Primary Key, Auto-incremented).
     - username: The username of the person borrowing the book (Text).
     - book_id: The ID of the book being borrowed (Integer; Foreign Key referencing Books).
     - status: The status of the borrowing transaction (Text; e.g., "borrowed", "returned").
"""
def init_db():
    query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    query("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year TEXT,
            language TEXT,
            available INTEGER DEFAULT 1
        )
    """)
    query("""
        CREATE TABLE IF NOT EXISTS borrow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            book_id INTEGER,
            status TEXT
        )
    """)

init_db()

# ---------------------- AUTH ROUTES ----------------------
"""
User Authentication and Registration Functions Documentation
This document outlines the user authentication and registration functionality within the Flask-based Library Management System. It includes routes for user registration, login, and logout, detailing how each route operates and their interactions with the database.
Functional Specifications
1. Register()
Route: /register  
Methods: GET, POST
Purpose
Allows new users to register by providing a username and password. The function also assigns a user role based on whether the username is in the predefined list of admin usernames.
Functionality

- GET Request: When accessed via GET, the registration form is rendered.
- POST Request: 
  - Retrieves the username and password from the form.
  - Hashes the password for secure storage.
  - Checks if the username is in the predefined ADMIN_USERS list to assign the role.
  - Inserts the new user into the users table in the database.
  - Redirects to the login page after successful registration.
2. login()

Route: /login  
Methods: GET, POST
Purpose
Handles user authentication by checking username and password against the records in the database. If the credentials are valid, it initiates a user session.
Functionality
- GET Request: When accessed via GET, the login form is rendered.
- POST Request:
  - Retrieves the username and password from the form.
  - Queries the database for the user information.
  - Verifies the provided password against the stored hashed password.
  - If authentication is successful, stores the username and role in the session and redirects to the main page.
  - If authentication fails, re-renders the login form with an error message.
3. logout()
Route: /logout  
Methods: GET
Purpose
Ends the user session by clearing the session data and redirecting to the login page.
Functionality
- Clears all session data to log the user out.
- Redirects the user to the login page.
"""

ADMIN_USERS = ["James1", "James2"]

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password)

        role = "admin" if username in ADMIN_USERS else "user"

        query("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
              (username, hashed_pw, role))
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = query("SELECT * FROM users WHERE username=?", (username,), fetchone=True)
        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect("/")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------------- DASHBOARD ----------------------
"""
This document describes the dashboard function in the Flask-based Library Management System. This function serves as the main user dashboard, displaying a list of books and allowing for search functionality based on user input.
Function Specification
Dashboard()
Route: /dashboard  
Methods: GET  
Decorator: @login_required
Purpose
The dashboard function renders a user's dashboard, displaying available books and providing a search feature to filter results based on title, author, or language. It can distinguish between regular users and admins, affecting the rendered template.
Functionality
1. User Authentication: 
   - The function is protected by the @login_required decorator, which ensures that only authenticated users can access it.
2. Search Query Handling: 
   - The function retrieves the search query parameter (q) from the URL. If a query is provided, it searches the books table for titles, authors, or languages that contain the search term.
   - If no query is provided, it fetches all books from the database.
3. Database Query Execution:
   - Executes the appropriate SQL query:
4. Data Preparation:
   - Converts each book record into a dictionary format for easier rendering in the template.
5. Template Rendering:
   - Uses the render_template function to display the dashboard.html template, passing the following context:
     - books: List of books to be displayed.
     - admin: A boolean indicating if the user is an admin.
     - session: The current user session data.
"""

@app.route("/")
@login_required
def dashboard():
    q = request.args.get("q", "")  # get the search query
    if q:
        books = query(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR language LIKE ?",
            ('%'+q+'%', '%'+q+'%', '%'+q+'%'),
            fetchall=True
        )
    else:
        books = query("SELECT * FROM books", fetchall=True)

    books = [dict(b) for b in books]
    return render_template(
        "dashboard.html",
        books=books,
        admin=(session["role"] == "admin"),
        session=session,
        q=q
    )

# ---------------------- ADD BOOK ----------------------
@app.route("/add_book", methods=["POST"])
@admin_required
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    year = request.form["year"]
    language = request.form["language"]
    query("INSERT INTO books (title, author, year, language) VALUES (?, ?, ?, ?)",
          (title, author, year, language))
    return redirect("/")

# ---------------------- BORROW / RETURN ----------------------
@app.route("/borrow/<int:book_id>")
@login_required
def borrow(book_id):
    book = query("SELECT * FROM books WHERE id=?", (book_id,), fetchone=True)
    if book["available"]:
        query("UPDATE books SET available=0 WHERE id=?", (book_id,))
        query("INSERT INTO borrow (username, book_id, status) VALUES (?, ?, ?)",
              (session["username"], book_id, "borrowed"))
    return redirect("/")

@app.route("/return/<int:book_id>")
@login_required
def return_book(book_id):
    book = query("SELECT * FROM books WHERE id=?", (book_id,), fetchone=True)
    if not book["available"]:
        query("UPDATE books SET available=1 WHERE id=?", (book_id,))
        query("INSERT INTO borrow (username, book_id, status) VALUES (?, ?, ?)",
              (session["username"], book_id, "returned"))
    return redirect("/")

# ---------------------- HISTORY ----------------------
@app.route("/history")
@login_required
def history():
    records = query("""
        SELECT borrow.*, books.title 
        FROM borrow 
        JOIN books ON borrow.book_id = books.id
        WHERE borrow.username=?
        ORDER BY borrow.id DESC
    """, (session["username"],), fetchall=True)
    return render_template("history.html", records=records)
# Only admins can access this
@app.route("/manage_users")
@login_required
@admin_required
def manage_users():
    users = query("SELECT id, username, role FROM users", fetchall=True)
    return render_template("manage_users.html", users=users)

# Update user role or username
@app.route("/update_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def update_user(user_id):
    new_username = request.form.get("username")
    new_role = request.form.get("role")
    query("UPDATE users SET username=?, role=? WHERE id=?",
          (new_username, new_role, user_id))
    return redirect("/manage_users")

# Delete user
@app.route("/delete_user/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):
    query("DELETE FROM users WHERE id=?", (user_id,))
    return redirect("/manage_users")



# ---------------------- RUN ----------------------
if __name__ == "__main__":
    app.run(debug=True)
