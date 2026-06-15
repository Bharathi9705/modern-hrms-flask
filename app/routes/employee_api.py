from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.employee import Employee
from app.utils.auth_decorator import token_required
from app import db
from datetime import datetime

employee_bp = Blueprint('employee_api', __name__)

@employee_bp.route('', methods=['GET'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin'])
def get_all_employees(current_user):
    dept_filter = request.args.get('department')
    search_q = request.args.get('search')

    query = Employee.query.join(User)
    if dept_filter:
        query = query.filter(Employee.department == dept_filter)
    if search_q:
        query = query.filter(
            (Employee.first_name.ilike(f"%{search_q}%")) |
            (Employee.last_name.ilike(f"%{search_q}%")) |
            (Employee.employee_id.ilike(f"%{search_q}%"))
        )

    employees = query.all()
    return jsonify([emp.to_dict() for emp in employees]), 200

@employee_bp.route('', methods=['POST'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin'])
def provision_employee(current_user):
    data = request.get_json() or {}
    try:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists.'}), 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data.get('password', 'Welcome2026!')),
            role=data.get('role', 'employee')
        )
        db.session.add(new_user)
        db.session.commit()

        new_profile = Employee(
            user_id=new_user.id,
            employee_id=f"EMP-{int(datetime.utcnow().timestamp()) % 100000}",
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone'),
            department=data['department'],
            designation=data['designation'],
            salary=float(data['salary']),
            joining_date=datetime.strptime(data['joining_date'], '%Y-%m-%d').date(),
            status='Active'
        )
        db.session.add(new_profile)
        db.session.commit()
        return jsonify(new_profile.to_dict()), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

@employee_bp.route('/<int:emp_id>', methods=['DELETE'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin'])
def purge_employee(current_user, emp_id):
    emp = Employee.query.get_or_404(emp_id)
    associated_user = User.query.get(emp.user_id)

    db.session.delete(emp)
    if associated_user:
        db.session.delete(associated_user)

    db.session.commit()
    return jsonify({'success': 'Employee deleted successfully.'}), 200