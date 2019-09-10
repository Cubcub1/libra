from functools import wraps

from flask import g

from .errors import forbidden


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_fuction(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('权限不够')
            return f(*args, **kwargs)

        return decorated_fuction

    return decorator
