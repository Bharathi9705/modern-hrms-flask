from app import create_app, db
from app.models.user import User
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.leave import Leave
from werkzeug.security import generate_password_hash
from datetime import date, datetime

app = create_app()

with app.app_context():
    print("\n🔄 Resetting database...")
    db.drop_all()
    db.create_all()

    # ── Admin user + employee profile ──
    admin = User(
        username='hai',
        email='hai@company.com',
        password_hash=generate_password_hash('admin'),
        role='admin'
    )
    db.session.add(admin)
    db.session.flush()  # get admin.id

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
    db.session.flush()

    # ── Sample employee 1 ──
    emp1_user = User(
        username='john_doe',
        email='john@company.com',
        password_hash=generate_password_hash('Welcome2026!'),
        role='employee'
    )
    db.session.add(emp1_user)
    db.session.flush()

    emp1 = Employee(
        user_id=emp1_user.id,
        employee_id='EMP-0002',
        first_name='John',
        last_name='Doe',
        department='Engineering',
        designation='Software Engineer',
        salary=60000.00,
        joining_date=date(2024, 3, 15),
        status='Active'
    )
    db.session.add(emp1)
    db.session.flush()

    # ── Sample employee 2 ──
    emp2_user = User(
        username='jane_smith',
        email='jane@company.com',
        password_hash=generate_password_hash('Welcome2026!'),
        role='employee'
    )
    db.session.add(emp2_user)
    db.session.flush()

    emp2 = Employee(
        user_id=emp2_user.id,
        employee_id='EMP-0003',
        first_name='Jane',
        last_name='Smith',
        department='HR Operations',
        designation='HR Manager',
        salary=65000.00,
        joining_date=date(2024, 2, 1),
        status='Active'
    )
    db.session.add(emp2)
    db.session.flush()

    # ── Sample employee 3 ──
    emp3_user = User(
        username='raj_kumar',
        email='raj@company.com',
        password_hash=generate_password_hash('Welcome2026!'),
        role='employee'
    )
    db.session.add(emp3_user)
    db.session.flush()

    emp3 = Employee(
        user_id=emp3_user.id,
        employee_id='EMP-0004',
        first_name='Raj',
        last_name='Kumar',
        department='Marketing Team',
        designation='Marketing Lead',
        salary=55000.00,
        joining_date=date(2024, 4, 10),
        status='Active'
    )
    db.session.add(emp3)
    db.session.flush()

    # ── Sample attendance records ──
    today = date.today().strftime('%Y-%m-%d')
    db.session.add(Attendance(employee_id=emp1.id, date=today, clock_in='09:02:00', clock_out='17:30:00', status='Present'))
    db.session.add(Attendance(employee_id=emp2.id, date=today, clock_in='09:15:00', clock_out=None, status='Present'))
    db.session.add(Attendance(employee_id=admin_emp.id, date=today, clock_in='08:45:00', clock_out='18:00:00', status='Present'))

    # ── Sample leave requests ──
    db.session.add(Leave(
        employee_id=emp1.id,
        leave_type='Casual',
        start_date=date(2026, 6, 20),
        end_date=date(2026, 6, 21),
        reason='Personal work',
        status='Pending'
    ))
    db.session.add(Leave(
        employee_id=emp2.id,
        leave_type='Sick',
        start_date=date(2026, 6, 18),
        end_date=date(2026, 6, 18),
        reason='Fever and cold',
        status='Approved'
    ))
    db.session.add(Leave(
        employee_id=emp3.id,
        leave_type='Earned',
        start_date=date(2026, 6, 25),
        end_date=date(2026, 6, 27),
        reason='Family vacation',
        status='Pending'
    ))

    db.session.commit()

    print("\n✅ Database seeded successfully!")
    print("=" * 45)
    print(" LOGIN CREDENTIALS")
    print("=" * 45)
    print(" Admin:  hai / admin")
    print(" Emp 1:  john_doe / Welcome2026!")
    print(" Emp 2:  jane_smith / Welcome2026!")
    print(" Emp 3:  raj_kumar / Welcome2026!")
    print("=" * 45)
    print(f" Created: 4 users, 4 employees")
    print(f" Attendance: 3 records for today")
    print(f" Leave requests: 3 sample records")
    print("=" * 45 + "\n")