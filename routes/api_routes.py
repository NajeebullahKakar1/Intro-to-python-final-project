from flask import Blueprint, jsonify, request, session
from models.book_model import get_all_books, get_book, search_books, add_book
from models.user_model import get_all_users
from models.borrow_model import borrow_book, return_book, get_history_for_user

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/books', methods=['GET'])
def api_books():
    q = request.args.get('q','')
    if q:
        books = search_books(q)
    else:
        books = get_all_books()
    return jsonify([dict(b) for b in books])

@bp.route('/books/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    b = get_book(book_id)
    if not b:
        return jsonify({'error':'not found'}), 404
    return jsonify(dict(b))

@bp.route('/books', methods=['POST'])
def api_add_book():
    if session.get('role')!='admin':
        return jsonify({'error':'admin only'}), 403
    data = request.json or {}
    add_book(data.get('title'), data.get('author'), data.get('year'), data.get('language'))
    return jsonify({'ok':True}), 201

@bp.route('/borrow/<int:book_id>', methods=['POST'])
def api_borrow(book_id):
    user = session.get('username')
    if not user:
        return jsonify({'error':'login required'}), 401
    b = get_book(book_id)
    if not b or b['available']==0:
        return jsonify({'error':'unavailable'}), 400
    borrow_book(user, book_id)
    return jsonify({'ok':True})

@bp.route('/return/<int:book_id>', methods=['POST'])
def api_return(book_id):
    user = session.get('username')
    if not user:
        return jsonify({'error':'login required'}), 401
    return_book(user, book_id)
    return jsonify({'ok':True})

@bp.route('/users', methods=['GET'])
def api_users():
    if session.get('role')!='admin':
        return jsonify({'error':'admin only'}), 403
    users = get_all_users()
    return jsonify([dict(u) for u in users])
