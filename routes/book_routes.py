from flask import Blueprint, render_template, request, session, url_for, redirect
from models.book_model import get_all_books, search_books, add_book, get_book, update_book, delete_book
"""
The dashboard is the main page users see after logging in.
It displays all the books and also allows searching by title, author,
year, or language.

Admins get an extra form to add books directly from this page.
Normal users only see book details and the borrow/return buttons.
"""


bp = Blueprint('book', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped

def admin_only(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get('role')!='admin':
            return 'Admins only', 403
        return f(*args, **kwargs)
    return wrapped

@bp.route('/')
@login_required
def dashboard():
    q = request.args.get('q','').strip()
    if q:
        books = search_books(q)
    else:
        books = get_all_books()
    return render_template('dashboard.html', books=books, admin=(session.get('role')=='admin'), q=q)

@bp.route('/add_book', methods=['POST'])
@admin_only
def add_book_route():
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    language = request.form.get('language')
    add_book(title, author, year, language)
    return redirect(url_for('book.dashboard'))

"""
These routes allow admins to manage the books in the system.
- /manage_books shows a list of all books
- /edit_book lets the admin edit book details
- /delete_book removes a book completely

Only admins are allowed to use these pages. This helps separate
regular users from librarians.
"""


@bp.route('/manage_books')
@admin_only
def manage_books():
    books = get_all_books()
    return render_template('manage_books.html', books=books)

@bp.route('/edit_book/<int:book_id>', methods=['GET','POST'])
@admin_only
def edit_book(book_id):
    book = get_book(book_id)
    if request.method=='POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        language = request.form.get('language')
        available = 1 if request.form.get('available')=='on' else 0
        update_book(book_id, title, author, year, language, available)
        return redirect(url_for('book.manage_books'))
    return render_template('edit_book.html', book=book)

@bp.route('/delete_book/<int:book_id>')
@admin_only
def delete_book_route(book_id):
    delete_book(book_id)
    return redirect(url_for('book.manage_books'))
