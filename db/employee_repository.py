# All database query functions for employees
# Employee Data Agent uses this file

from sqlalchemy.orm import Session
from db.models import Employee, LeaveBalance, LeaveRequest, User, Department
from shared.logger import logger
from typing import Optional
import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def get_employee_by_username(db: Session, username: str) -> Optional[Employee]:
    user = db.query(User).filter_by(username=username).first()
    if user:
        return user.employee
    return None


def get_employee_by_id(db: Session, employee_id: str) -> Optional[Employee]:
    return db.query(Employee).filter_by(employee_id=employee_id).first()


def get_leave_balance(db: Session, employee_db_id: int, year: int = 2026):
    return db.query(LeaveBalance).filter_by(
        employee_id=employee_db_id,
        year=year
    ).first()


def get_leave_requests(db: Session, employee_db_id: int):
    return db.query(LeaveRequest).filter_by(
        employee_id=employee_db_id
    ).order_by(LeaveRequest.applied_on.desc()).all()


def get_leave_requests_by_employee(db: Session, employee_db_id: int):
    return db.query(LeaveRequest).filter_by(
        employee_id=employee_db_id
    ).order_by(
        LeaveRequest.applied_on.desc()
    ).all()

def update_leave_balance_after_approval(
    db: Session,
    employee_db_id: int,
    leave_type: str,
    days_count: int,
    year: int = 2026
) -> dict:

    leave_balance = db.query(LeaveBalance).filter_by(
        employee_id=employee_db_id,
        year=year
    ).first()

    if not leave_balance:
        return {
            "status": "failed",
            "message": "Leave balance row not found"
        }

    leave_type = leave_type.strip().lower()

    if leave_type in ["casual", "casual_leave", "cl"]:

        if leave_balance.casual_leave_remaining < days_count:
            return {
                "status": "failed",
                "message": "Insufficient casual leave balance"
            }

        leave_balance.casual_leave_used += days_count

    elif leave_type in ["sick", "sick_leave", "sl"]:

        if leave_balance.sick_leave_remaining < days_count:
            return {
                "status": "failed",
                "message": "Insufficient sick leave balance"
            }

        leave_balance.sick_leave_used += days_count

    elif leave_type in ["earned", "earned_leave", "el"]:

        if leave_balance.earned_leave_remaining < days_count:
            return {
                "status": "failed",
                "message": "Insufficient earned leave balance"
            }

        leave_balance.earned_leave_used += days_count

    else:
        return {
            "status": "failed",
            "message": f"Unsupported leave type: {leave_type}"
        }

    db.commit()
    db.refresh(leave_balance)

    logger.info(
        f"[EMPLOYEE REPO] Leave balance updated for employee_id={employee_db_id}, "
        f"leave_type={leave_type}, days_count={days_count}"
    )

    return {
        "status": "success",
        "message": "Leave balance updated successfully",
        "remaining_balance": {
            "casual_leave": leave_balance.casual_leave_remaining,
            "sick_leave": leave_balance.sick_leave_remaining,
            "earned_leave": leave_balance.earned_leave_remaining
        }
    }


def get_employee_profile(db: Session, username: str) -> dict:
    employee = get_employee_by_username(db, username)

    if not employee:
        return {"found": False, "error": "Employee not found"}

    leave_balance = get_leave_balance(db, employee.id)

    profile = {
        "found": True,
        "employee_id": employee.employee_id,
        "full_name": employee.full_name,
        "designation": employee.designation,
        "department": employee.department.name if employee.department else "N/A",
        "email": employee.email,
        "phone": employee.phone,
        "date_of_joining": str(employee.date_of_joining.date()),
        "employment_type": employee.employment_type,
        "leave_balance": {
            "year": 2026,
            "casual_leave": {
                "total": leave_balance.casual_leave_total if leave_balance else 0,
                "used": leave_balance.casual_leave_used if leave_balance else 0,
                "remaining": leave_balance.casual_leave_remaining if leave_balance else 0
            },
            "sick_leave": {
                "total": leave_balance.sick_leave_total if leave_balance else 0,
                "used": leave_balance.sick_leave_used if leave_balance else 0,
                "remaining": leave_balance.sick_leave_remaining if leave_balance else 0
            },
            "earned_leave": {
                "total": leave_balance.earned_leave_total if leave_balance else 0,
                "used": leave_balance.earned_leave_used if leave_balance else 0,
                "remaining": leave_balance.earned_leave_remaining if leave_balance else 0
            }
        }
    }

    logger.debug(f"[EMPLOYEE REPO] Profile fetched for {username}")
    return profile