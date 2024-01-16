'''Decorators to restrict certain functions of ZRApp to certain user roles'''
from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    '''Decorator to restrict function to specific user role'''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    '''Decorator to restrict function to admin only'''
    return permission_required(Permission.ADMIN)(f)
