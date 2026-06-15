from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config['SECRET_KEY'] = 'hrms_super_secret_encryption_key_2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../hrms.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt_secure_token_key_hrms_2026_32b'  # fixed: 32+ bytes
    app.config['JWT_EXPIRY_HOURS'] = 8

    db.init_app(app)
    JWTManager(app)

    from app.routes.auth_api import auth_bp
    from app.routes.attendance_api import attendance_bp
    from app.routes.dashboard_api import dashboard_bp
    from app.routes.employee_api import employee_bp   # ← ADD THIS
    from app.routes.leave_api import leave_bp         # ← ADD THIS
    from app.routes.views import views_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(employee_bp, url_prefix='/api/employees')  # ← ADD THIS
    app.register_blueprint(leave_bp, url_prefix='/api/leaves')        # ← ADD THIS
    app.register_blueprint(views_bp)

    with app.app_context():
        db.create_all()

    # Print routing map
    print("\n=== FLASK ACTIVE ROUTING MAP ===")
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule} --> Endpoint: {rule.endpoint} (Methods: {sorted(rule.methods)})")
    print("=================================\n")

    return app