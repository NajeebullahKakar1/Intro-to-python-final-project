from flask import Blueprint, render_template, request, session, url_for, redirect
from models.user_model import get_all_users, update_user, delete_user

"""
Admin routes allow administrators to manage all users.
Admins can:

- view all registered users
- update usernames or roles
- delete users

Only accounts with an admin role can access these pages.
This is part of the authorization requirement of the project.
"""

bp = Blueprint('admin', __name__)

def admin_only(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get('role')!='admin':
            return 'Admins only', 403
        return f(*args, **kwargs)
    return wrapped

@bp.route('/manage_users')
@admin_only
def manage_users():
    users = get_all_users()
    return render_template('manage_users.html', users=users)

@bp.route('/update_user/<int:user_id>', methods=['POST'])
@admin_only
def update_user_route(user_id):
    username = request.form.get('username')
    role = request.form.get('role')
    update_user(user_id, username, role)
    return redirect(url_for('admin.manage_users'))

@bp.route('/delete_user/<int:user_id>')
@admin_only
def delete_user_route(user_id):
    delete_user(user_id)
    return redirect(url_for('admin.manage_users'))
