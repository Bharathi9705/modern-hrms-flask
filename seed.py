from app import create_app, db
from app.models.user import User
from app.models.employee import Employee
from werkzeug.security import generate_password_hash
from datetime import date

app = create_app()

with app.app_context():
    # Drop and recreate all tables fresh
    db.drop_all()
    db.create_all()

    # Create admin user
    admin_user = User(
        username='hai',
        email='hai@company.com',
        password_hash=generate_password_hash('admin'),
        role='admin'
    )
    db.session.add(admin_user)
    db.session.flush()

    # Create employee profile for admin
    admin_emp = Employee(
        user_id=admin_user.id,
        employee_id='EMP-0001',
        first_name='Hai',
        last_name='Admin',
        department='Engineering',
        designation='System Administrator',
        salary=75000.00,
        joining_date=date(2024, 1, 1),
        status='Active'
    )
    db.session.add(admin_emp)
    db.session.commit()

    print("\n=============================================")
    print(" SUCCESS! Database recreated fresh.")
    print(" Login credentials:")
    print(" Username: hai")
    print(" Password: admin")
    print("=============================================\n")