from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import create_user, get_user_by_username
"""
This file contains all the routes related to user accounts.
It handles:

- registering new users
- logging in
- logging out

It also checks the usernames to decide if someone should automatically
become an admin (James1 or James2). The routes here work with the
user_model to save and fetch info from the database.
"""


bp = Blueprint('auth', __name__)
ADMIN_USERS = ['James1', 'James2']

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if get_user_by_username(username):
            return render_template('register.html', error='User exists')
        hashed = generate_password_hash(password)
        role = 'admin' if username in ADMIN_USERS else 'user'
        create_user(username, hashed, role)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username'].strip()
        password = request.form['password']
        u = get_user_by_username(username)
        if u and check_password_hash(u['password'], password):
            session['username']=u['username']
            session['role']=u['role']
            return redirect(url_for('book.dashboard'))
        return render_template('login.html', error='Invalid')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
