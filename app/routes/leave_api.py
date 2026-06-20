from flask import Blueprint, request, jsonify
from app.models.leave import Leave
from app.models.employee import Employee
from app.utils.auth_decorator import token_required
from app import db
from datetime import datetime

leave_bp = Blueprint('leave_api', __name__)

def enrich_leave(record):
    """Add employee_name to a leave dict."""
    d = record.to_dict()
    emp = Employee.query.get(record.employee_id)
    d['employee_name'] = f"{emp.first_name} {emp.last_name}" if emp else "Unknown"
    return d

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

    return jsonify([enrich_leave(r) for r in records]), 200

@leave_bp.route('/apply', methods=['POST'])
@token_required(allowed_roles=['employee', 'super_admin', 'hr_manager', 'admin'])
def post_leave(current_user):
    emp = Employee.query.filter_by(user_id=current_user.id).first()
    if not emp:
        return jsonify({'error': 'No employee profile found for this user.'}), 404

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
        return jsonify(enrich_leave(new_leave)), 201
    except KeyError as e:
        db.session.rollback()
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
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
        return jsonify({'error': 'Status must be Approved or Rejected'}), 400

    record.status = next_status
    record.reviewed_by = current_user.id
    db.session.commit()
    return jsonify(enrich_leave(record)), 200