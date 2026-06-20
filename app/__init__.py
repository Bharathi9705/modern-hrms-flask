import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Use environment variables in production, fallback for local dev
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hrms_super_secret_encryption_key_2026')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt_secure_token_key_hrms_2026_32b')
    app.config['JWT_EXPIRY_HOURS'] = 8
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Use /tmp for SQLite on Render (ephemeral), or local file for dev
    if os.environ.get('RENDER'):
        # Production on Render — use /tmp
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/hrms.db'
    else:
        # Local development
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../hrms.db'

    db.init_app(app)
    JWTManager(app)

    from app.routes.auth_api import auth_bp
    from app.routes.attendance_api import attendance_bp
    from app.routes.dashboard_api import dashboard_bp
    from app.routes.employee_api import employee_bp
    from app.routes.leave_api import leave_bp
    from app.routes.views import views_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(leave_bp, url_prefix='/api/leaves')
    app.register_blueprint(views_bp)

    with app.app_context():
        db.create_all()
        # Auto-seed admin user if DB is empty (for Render first deploy)
        _seed_if_empty()

    return app


def _seed_if_empty():
    """Create default admin if no users exist (first deploy on Render)."""
    from app.models.user import User
    from app.models.employee import Employee
    from werkzeug.security import generate_password_hash
    from datetime import date

    if User.query.count() == 0:
        admin = User(
            username='hai',
            email='hai@company.com',
            password_hash=generate_password_hash('admin'),
            role='admin'
        )
        db.session.add(admin)
        db.session.flush()

        admin_emp = Employee(
            user_id=admin.id,
            employee_id='EMP-0001',
            first_name='Hai',
            last_name='Admin',
            department='Engineering',
            designation='System Administrator',
            salary=80000.00,
            joining_date=date(2024, 1, 1),
            status='Active'
        )
        db.session.add(admin_emp)
        db.session.commit()
        print("✅ Default admin user created: hai / admin")