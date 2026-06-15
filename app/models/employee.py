from app import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50), nullable=False, index=True)
    designation = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Numeric(12, 2), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Active') # Active, On_Leave, Terminated
    avatar_url = db.Column(db.Text, nullable=True)

    # FIXED: Changed backref to back_populates to resolve the duplicate mapping error
    user = db.relationship('User', back_populates='employee_profile', lazy=True)

    # Core relationship connections
    attendance_records = db.relationship('Attendance', backref='employee', lazy=True, cascade='all, delete-orphan')
    leave_applications = db.relationship('Leave', backref='employee', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'name': f"{self.first_name} {self.last_name}",
            # These lines will now work perfectly without crashing!
            'email': self.user.email if self.user else "N/A",
            'username': self.user.username if self.user else "N/A",
            'role': self.user.role if self.user else "employee",
            'phone': self.phone,
            'department': self.department,
            'designation': self.designation,
            'salary': float(self.salary),
            'joining_date': self.joining_date.isoformat() if self.joining_date else "N/A",
            'status': self.status,
            'avatar_url': self.avatar_url or f"https://ui-avatars.com/api/?name={self.first_name}+{self.last_name}&background=4f46e5&color=fff"
        }