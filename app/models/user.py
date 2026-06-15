from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # super_admin, hr_manager, employee
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

   # Inside your User class:
    employee_profile = db.relationship('Employee', back_populates='user', uselist=False, cascade='all, delete-orphan')
    audit_events = db.relationship('AuditLog', backref='user', lazy='dynamic')