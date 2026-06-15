from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.utils.auth_decorator import token_required

attendance_bp = Blueprint('attendance_api', __name__)

def get_employee_for_user(user):
    return Employee.query.filter_by(user_id=user.id).first()

@attendance_bp.route('', methods=['GET'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin', 'employee'])
def get_all_attendance(current_user):
    if current_user.role == 'employee':
        emp = get_employee_for_user(current_user)
        if not emp:
            return jsonify([]), 200
        logs = Attendance.query.filter_by(employee_id=emp.id).order_by(Attendance.date.desc()).all()
    else:
        logs = Attendance.query.order_by(Attendance.date.desc()).all()

    result = []
    for log in logs:
        emp = Employee.query.get(log.employee_id)
        name = f"{emp.first_name} {emp.last_name}" if emp else "Unknown"
        result.append({
            "id": log.id,
            "employee_name": name,
            "date": log.date,
            "clock_in": log.clock_in,
            "clock_out": log.clock_out,
            "status": log.status
        })
    return jsonify(result), 200

@attendance_bp.route('/status', methods=['GET'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin', 'employee'])
def get_attendance_status(current_user):
    emp = get_employee_for_user(current_user)
    if not emp:
        return jsonify({"status": "checked_out", "clock_in_time": None}), 200

    today = datetime.now().strftime('%Y-%m-%d')
    active_shift = Attendance.query.filter_by(employee_id=emp.id, date=today, clock_out=None).first()

    if active_shift:
        return jsonify({"status": "clocked_in", "clock_in_time": active_shift.clock_in}), 200
    return jsonify({"status": "checked_out", "clock_in_time": None}), 200

@attendance_bp.route('/clock-action', methods=['POST'])
@token_required(allowed_roles=['super_admin', 'hr_manager', 'admin', 'employee'])
def clock_action(current_user):
    emp = get_employee_for_user(current_user)
    if not emp:
        return jsonify({"error": "No employee profile found."}), 404

    data = request.get_json() or {}
    action_type = data.get('action')
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')

    if action_type == 'clock_in':
        existing = Attendance.query.filter_by(employee_id=emp.id, date=today, clock_out=None).first()
        if existing:
            return jsonify({"error": "Already clocked in."}), 400
        new_log = Attendance(employee_id=emp.id, date=today, clock_in=current_time, status='Present')
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Clocked in successfully."}), 201

    elif action_type == 'clock_out':
        active_shift = Attendance.query.filter_by(employee_id=emp.id, date=today, clock_out=None).first()
        if not active_shift:
            return jsonify({"error": "No active shift found."}), 400
        active_shift.clock_out = current_time
        db.session.commit()
        return jsonify({"message": "Clocked out successfully."}), 200

    return jsonify({"error": "Invalid action. Use 'clock_in' or 'clock_out'."}), 400