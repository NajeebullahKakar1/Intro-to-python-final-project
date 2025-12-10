from flask import Blueprint, render_template, request, session, url_for, redirect
from models.borrow_model import borrow_book, return_book, get_history_for_user
from models.book_model import get_book

"""
Borrow and return routes let a logged-in user check out and return books.
The system updates the book's availability and also records each action
in the borrow history table so it can be shown later.
"""

bp = Blueprint('borrow', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped

@bp.route('/borrow/<int:book_id>')
@login_required
def borrow(book_id):
    user = session.get('username')
    b = get_book(book_id)
    if not b or b['available']==0:
        return redirect(url_for('book.dashboard'))
    borrow_book(user, book_id)
    return redirect(url_for('book.dashboard'))

@bp.route('/return/<int:book_id>')
@login_required
def return_book_route(book_id):
    user = session.get('username')
    b = get_book(book_id)
    if not b or b['available']==1:
        return redirect(url_for('book.dashboard'))
    return_book(user, book_id)
    return redirect(url_for('book.dashboard'))

"""
This page shows the logged-in user's borrowing history.
It includes the book title and whether it was borrowed or returned.
The history is pulled by joining the borrow table and the books table.
"""


@bp.route('/history')
@login_required
def history():
    user = session.get('username')
    records = get_history_for_user(user)
    return render_template('history.html', records=records)
