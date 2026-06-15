from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def login_view():
    return render_template('login.html')

@views_bp.route('/view/dashboard')
def dashboard_view():
    return render_template('dashboard.html')

@views_bp.route('/view/employees')
def employees_view():
    return render_template('employees.html')

@views_bp.route('/view/attendance')
def attendance_view():
    return render_template('attendance.html')

@views_bp.route('/view/leaves')
def leaves_view():
    return render_template('leaves.html')