from flask import Blueprint, request, jsonify
from app.models.leave import Leave
from app.models.employee import Employee
from app.utils.auth_decorator import token_required
from app import db
from datetime import datetime

leave_bp = Blueprint('leave_api', __name__)

@leave_bp.route('', methods=['GET'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin', 'employee'])
def retrieve_leaves(current_user):
    if current_user.role == 'employee':
        emp = Employee.query.filter_by(user_id=current_user.id).first()
        if not emp:
            return jsonify([]), 200
        records = Leave.query.filter_by(employee_id=emp.id).order_by(Leave.created_at.desc()).all()
    else:
        records = Leave.query.order_by(Leave.created_at.desc()).all()

    result = []
    for r in records:
        emp = Employee.query.get(r.employee_id)
        name = f"{emp.first_name} {emp.last_name}" if emp else "Unknown"
        d = r.to_dict()
        d['employee_name'] = name
        result.append(d)

    return jsonify(result), 200

@leave_bp.route('/apply', methods=['POST'])
@token_required(allowed_roles=['employee', 'super_admin', 'hr_manager', 'admin'])
def post_leave(current_user):
    emp = Employee.query.filter_by(user_id=current_user.id).first()
    if not emp:
        return jsonify({'error': 'No employee profile found'}), 404

    data = request.get_json() or {}
    try:
        new_leave = Leave(
            employee_id=emp.id,
            leave_type=data['leave_type'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            reason=data['reason'],
            status='Pending'
        )
        db.session.add(new_leave)
        db.session.commit()
        return jsonify(new_leave.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@leave_bp.route('/<int:leave_id>', methods=['PUT'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin'])
def transition_leave_state(current_user, leave_id):
    record = Leave.query.get_or_404(leave_id)
    data = request.get_json() or {}
    next_status = data.get('status')

    if next_status not in ['Approved', 'Rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    record.status = next_status
    record.reviewed_by = current_user.id
    db.session.commit()
    return jsonify(record.to_dict()), 200