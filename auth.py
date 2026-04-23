import jwt
from functools import wraps
from flask import request, jsonify
from models import User

def token_required(app, db):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                try:
                    token = request.headers["Authorization"].split()[1]
                except IndexError:
                    pass
            if not token:
                return jsonify({"error": "Token missing"}), 401
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms = ['HS256'])
                current_user = User.query.get(data["user_id"])
            except:
                return jsonify({"error": "Invalid token"}), 401
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(f):
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if current_user.role != "admin":
            return jsonify({"error": "Adimn access required"}), 403
        return f(current_user, *args, **kwargs)
    return wrapper
  
