# All Database Table Definitions
# Each class = one table in MySQL

from sqlalchemy import (
    Column, Integer, String, Boolean,
    DateTime, Float, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from db.base import Base


# TABLE 1 — departments
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

    employees = relationship("Employee", back_populates="department")

    def __repr__(self):
        return f"<Department {self.name}>"


# TABLE 2 — employees
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    designation = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    date_of_joining = Column(DateTime, nullable=False)
    employment_type = Column(
        Enum("full_time", "part_time", "contract"),
        default="full_time"
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("Department", back_populates="employees")
    user = relationship("User", back_populates="employee", uselist=False)
    leave_balance = relationship("LeaveBalance", back_populates="employee")
    leave_requests = relationship(
        "LeaveRequest",
        back_populates="employee",
        foreign_keys="LeaveRequest.employee_id"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Employee {self.employee_id}>"


# TABLE 3 — users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum("employee", "hr", "admin", "manager"),
        default="employee",
        nullable=False
    )
    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        unique=True,
        nullable=False
    )
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    employee = relationship("Employee", back_populates="user")

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"


# TABLE 4 — leave_balances
class LeaveBalance(Base):
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    year = Column(Integer, nullable=False, default=2026)

    casual_leave_total = Column(Integer, default=12)
    casual_leave_used = Column(Integer, default=0)

    sick_leave_total = Column(Integer, default=10)
    sick_leave_used = Column(Integer, default=0)

    earned_leave_total = Column(Integer, default=15)
    earned_leave_used = Column(Integer, default=0)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    employee = relationship("Employee", back_populates="leave_balance")

    @property
    def casual_leave_remaining(self):
        return self.casual_leave_total - self.casual_leave_used

    @property
    def sick_leave_remaining(self):
        return self.sick_leave_total - self.sick_leave_used

    @property
    def earned_leave_remaining(self):
        return self.earned_leave_total - self.earned_leave_used

    def __repr__(self):
        return f"<LeaveBalance Employee:{self.employee_id} Year:{self.year}>"


# TABLE 5 — leave_requests
class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type = Column(
        Enum("casual_leave", "sick_leave", "earned_leave"),
        nullable=False
    )
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    days_count = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(
        Enum("pending", "approved", "rejected"),
        default="pending"
    )
    approved_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    applied_on = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    employee = relationship(
        "Employee",
        back_populates="leave_requests",
        foreign_keys=[employee_id]
    )

    def __repr__(self):
        return f"<LeaveRequest {self.employee_id} - {self.leave_type}>"


# TABLE 6 — audit_logs
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    username = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)
    department = Column(String(100), nullable=True)
    raw_query = Column(Text, nullable=False)
    query_type = Column(String(20), nullable=False)
    agents_used = Column(String(255), nullable=True)
    final_answer = Column(Text, nullable=True)
    status = Column(String(20), default="success")
    processing_time_ms = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<AuditLog {self.query_id}>"