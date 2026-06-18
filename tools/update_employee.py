# Run: python -m tools.update_employee

import bcrypt
from db.session import SessionLocal
from db.models import Employee, User, LeaveBalance


def update_employee():
    db = SessionLocal()

    try:
        # WHICH EMPLOYEE TO UPDATE
        target_employee_id  = "EMP001"        # Dhiraj's employee ID
        target_username     = "dhiru_offl"  # Dhiraj's username

        # WHAT TO UPDATE
        new_designation     = "Software Engineer 2"
        new_phone           = "8489403967"    # keep same or change

        # Step 1 — Update Employee Details
        employee = db.query(Employee).filter_by(
            employee_id=target_employee_id
        ).first()

        if not employee:
            print(f"✗ Employee {target_employee_id} not found")
            return

        old_designation = employee.designation
        employee.designation = new_designation
        employee.phone = new_phone
        db.commit()

        print(f"✓ Employee updated  : {employee.full_name}")
        print(f"  Designation      : {old_designation} → {new_designation}")

        # Step 2 — Check User Record
        user = db.query(User).filter_by(
            username=target_username
        ).first()

        if user:
            print(f"✓ User confirmed    : {user.username}")
            print(f"  Role             : {user.role}")
        else:
            print(f"✗ User {target_username} not found")

        # Step 3 — Check Leave Balance
        leave = db.query(LeaveBalance).filter_by(
            employee_id=employee.id,
            year=2026
        ).first()

        if leave:
            print(f"✓ Leave balance     : Confirmed for {target_employee_id}")
            print(f"  Casual Remaining : {leave.casual_leave_remaining}")
            print(f"  Sick Remaining   : {leave.sick_leave_remaining}")
            print(f"  Earned Remaining : {leave.earned_leave_remaining}")

        print("")
        print("=" * 45)
        print("   EMPLOYEE UPDATED SUCCESSFULLY")
        print("=" * 45)
        print(f"  Name        : {employee.full_name}")
        print(f"  Emp ID      : {target_employee_id}")
        print(f"  New Role    : {new_designation}")
        print(f"  Username    : {target_username}")
        print("=" * 45)

    except Exception as e:
        db.rollback()
        print(f"✗ Update failed: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    update_employee()