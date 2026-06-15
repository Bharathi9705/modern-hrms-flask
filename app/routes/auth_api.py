from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.employee import Employee
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

auth_bp = Blueprint('auth_api', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        token = create_access_token(
            identity=user.username,
            additional_claims={'role': user.role},
            expires_delta=timedelta(hours=8)
        )
        return jsonify({'access_token': token}), 200

    return jsonify({'error': 'Invalid username or password'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    try:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400

        # Use provided password or default
        password = data.get('password', 'Welcome2026!')

        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(password),
            role=data.get('role', 'employee')
        )
        db.session.add(user)
        db.session.flush()

        employee = Employee(
            user_id=user.id,
            employee_id=data.get('employee_id', f"EMP-{int(datetime.utcnow().timestamp()) % 100000}"),
            first_name=data['first_name'],
            last_name=data['last_name'],
            department=data['department'],
            designation=data['designation'],
            salary=float(data['salary']),
            joining_date=datetime.strptime(data['joining_date'], '%Y-%m-%d').date(),
            status='Active'
        )
        db.session.add(employee)
        db.session.commit()

        return jsonify({'message': 'Profile provisioned successfully'}), 201
    except KeyError as e:
        db.session.rollback()
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400