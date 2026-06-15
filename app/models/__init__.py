# Import the shared database instance from the main app package
from app import db

# Explicitly import all data model classes to register them with SQLAlchemy
from app.models.user import User
from app.models.employee import Employee
from app.models.audit import AuditLog
from app.models.attendance import Attendance
from app.models.leave import Leave

# This allows other files to import everything directly from "app.models"
__all__ = ['db', 'User', 'Employee', 'AuditLog', 'Attendance', 'Leave']