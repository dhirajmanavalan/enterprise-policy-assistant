# Run: python -m tools.add_employee

import bcrypt
from db.session import SessionLocal
from db.models import Employee, User, LeaveBalance
from datetime import datetime


def add_new_employee():
    db = SessionLocal()

    try:
        # NEW EMPLOYEE DETAILS
        emp_id = "EMP020"
        first_name = "Santhosh"
        last_name = ""
        email = "santhosh@company.com"
        phone = "9876543213"
        designation = "Operations Manager"
        department_id = 5
        joining_date = datetime(2026, 2, 20)
        username = "santhosh"
        password = "Santhosh@123"
        role = "manager"

        # Step 1 — Create Employee Record
        employee = Employee(
            employee_id=emp_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            designation=designation,
            department_id=department_id,
            date_of_joining=joining_date,
            employment_type="full_time"
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        print(f"✓ Employee created : {employee.full_name}")
        print(f"  Employee ID      : {emp_id}")
        print(f"  DB ID            : {employee.id}")

        # Step 2 — Create User Login
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            username=username,
            password_hash=hashed,
            role=role,
            employee_id=employee.id
        )
        db.add(user)
        db.commit()
        print(f"✓ User created     : {username}")
        print(f"  Role             : {role}")

        # Step 3 — Create Leave Balance
        leave = LeaveBalance(
            employee_id=employee.id,
            year=2026,
            casual_leave_total=12, casual_leave_used=0,
            sick_leave_total=10,   sick_leave_used=0,
            earned_leave_total=15, earned_leave_used=0
        )
        db.add(leave)
        db.commit()
        print(f"✓ Leave balance    : Created for {emp_id}")

        print("")
        print("=" * 45)
        print("   NEW EMPLOYEE ADDED SUCCESSFULLY")
        print("=" * 45)
        print(f"  Name       : {first_name} {last_name}")
        print(f"  Emp ID     : {emp_id}")
        print(f"  Department : Engineering")
        print(f"  Role       : {designation}")
        print(f"  Username   : {username}")
        print(f"  Password   : {password}")
        print("=" * 45)

    except Exception as e:
        db.rollback()
        print(f"✗ Failed: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    add_new_employee()

    # Remember if you add employees use this numbers for employee_id
    # 1 Engineering
    # 2 Human Resources
    # 3 Finance
    # 4 Marketing
    # 5 Operations