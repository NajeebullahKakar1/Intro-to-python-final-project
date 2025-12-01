from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB = "library.db"

# ---------------------- HELPERS ----------------------
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


# ---------------------- RUN ----------------------
if __name__ == "__main__":
    app.run(debug=True)
