"""
Employee ORM Model Definition for Flask-SQLAlchemy.
"""
from datetime import datetime, timezone
from app.database import db

class Employee(db.Model):
    """
    Employee Model representing the employees table in SQLite database.
    """
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    department = db.Column(db.String(80), nullable=False, index=True)
    role = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """
        Convert Employee ORM object to a clean dictionary representation for JSON responses.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'role': self.role,
            'salary': round(self.salary, 2),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Employee id={self.id} name='{self.name}' email='{self.email}' dept='{self.department}'>"
