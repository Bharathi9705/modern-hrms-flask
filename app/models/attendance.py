from app import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    clock_in = db.Column(db.String(30), nullable=True)
    clock_out = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(20), default='Present')