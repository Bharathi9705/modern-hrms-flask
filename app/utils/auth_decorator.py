from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models.user import User

def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]

            if not token:
                return jsonify({'error': 'Access token missing.'}), 401

            try:
                data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                
                # FIX: 'sub' contains username string, not ID — query by username
                current_user = User.query.filter_by(username=data['sub']).first()
                
                if not current_user:
                    return jsonify({'error': 'User not found.'}), 401

                if allowed_roles and current_user.role not in allowed_roles:
                    return jsonify({'error': 'Insufficient permissions.'}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Session expired. Please login again.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token.'}), 401

            return f(current_user, *args, **kwargs)
        return decorated
    return decorator