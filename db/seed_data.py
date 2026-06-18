# Sample Data - Run ONCE to populate database
# Here I am Creating fake company data for testing

from sqlalchemy.orm import Session
from datetime import datetime
from db.models import Department, Employee, User, LeaveBalance, LeaveRequest
from shared.logger import logger

import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def seed_departments(db: Session):
    logger.info("[SEED] Creating departments...")
    departments = [
        Department(name="Engineering", code="ENG",
                   description="Software development and technical operations"),
        Department(name="Human Resources", code="HR",
                   description="Employee management and HR policies"),
        Department(name="Finance", code="FIN",
                   description="Financial planning and accounting"),
        Department(name="Marketing", code="MKT",
                   description="Marketing and brand management"),
        Department(name="Operations", code="OPS",
                   description="Business operations and administration"),
    ]
    db.add_all(departments)
    db.commit()
    logger.info(f"[SEED] {len(departments)} departments created")
    return departments


def seed_employees(db: Session):
    logger.info("[SEED] Creating employees...")

    eng = db.query(Department).filter_by(code="ENG").first()
    hr = db.query(Department).filter_by(code="HR").first()
    fin = db.query(Department).filter_by(code="FIN").first()
    mkt = db.query(Department).filter_by(code="MKT").first()
    ops = db.query(Department).filter_by(code="OPS").first()

    employees = [
        Employee(
            employee_id="EMP001", first_name="Dhiraj", last_name="kumar",
            email="kumardhiraj7720@gmail.com", phone="8489403967",
            designation="Software Engineer", department_id=eng.id,
            date_of_joining=datetime(2026, 1, 12), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP002", first_name="Deb", last_name="deepta",
            email="debdeepta@company.com", phone="1234567890",
            designation="Software Engineer", department_id=eng.id,
            date_of_joining=datetime(2026, 1, 13), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP003", first_name="Madhu", last_name="mitha",
            email="madhumitha@company.com", phone="6374632417",
            designation="Tech Lead", department_id=eng.id,
            date_of_joining=datetime(2026, 1, 14), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP004", first_name="Nagendra", last_name="Enukolu",
            email="nagendra@company.com", phone="1112223334",
            designation="HR Manager", department_id=hr.id,
            date_of_joining=datetime(2026, 1, 15), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP005", first_name="Vikram", last_name="Gupta",
            email="vikram.gupta@company.com", phone="9876543214",
            designation="HR Executive", department_id=hr.id,
            date_of_joining=datetime(2023, 2, 15), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP006", first_name="Anjali", last_name="Singh",
            email="anjali.singh@company.com", phone="9876543215",
            designation="Finance Manager", department_id=fin.id,
            date_of_joining=datetime(2018, 11, 5), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP007", first_name="Karthik", last_name="Menon",
            email="karthik.menon@company.com", phone="9876543216",
            designation="Marketing Executive", department_id=mkt.id,
            date_of_joining=datetime(2022, 9, 12), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP008", first_name="Divya", last_name="Kumar",
            email="divya.kumar@company.com", phone="9876543217",
            designation="Operations Manager", department_id=ops.id,
            date_of_joining=datetime(2020, 7, 20), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP009", first_name="Rohit", last_name="Joshi",
            email="rohit.joshi@company.com", phone="9876543218",
            designation="Junior Software Engineer", department_id=eng.id,
            date_of_joining=datetime(2024, 1, 8), employment_type="full_time"
        ),
        Employee(
            employee_id="EMP010", first_name="Meera", last_name="Iyer",
            email="meera.iyer@company.com", phone="9876543219",
            designation="Admin Executive", department_id=ops.id,
            date_of_joining=datetime(2023, 5, 22), employment_type="full_time"
        ),
    ]
    db.add_all(employees)
    db.commit()
    logger.info(f"[SEED] {len(employees)} employees created")
    return employees


def seed_users(db: Session):
    logger.info("[SEED] Creating user accounts...")

    # Get all employees to map employee_id string to db id
    emp_map = {
        "EMP001": db.query(Employee).filter_by(employee_id="EMP001").first(),
        "EMP002": db.query(Employee).filter_by(employee_id="EMP002").first(),
        "EMP003": db.query(Employee).filter_by(employee_id="EMP003").first(),
        "EMP004": db.query(Employee).filter_by(employee_id="EMP004").first(),
        "EMP005": db.query(Employee).filter_by(employee_id="EMP005").first(),
        "EMP006": db.query(Employee).filter_by(employee_id="EMP006").first(),
        "EMP007": db.query(Employee).filter_by(employee_id="EMP007").first(),
        "EMP008": db.query(Employee).filter_by(employee_id="EMP008").first(),
        "EMP009": db.query(Employee).filter_by(employee_id="EMP009").first(),
        "EMP010": db.query(Employee).filter_by(employee_id="EMP010").first(),
    }

    users = [
        # Regular employees - role: employee
        User(
            username="dhiru_offl",
            password_hash=hash_password("Dhi@123"),
            role="employee",
            employee_id=emp_map["EMP001"].id
        ),
        User(
            username="deb.deep",
            password_hash=hash_password("Deb@123"),
            role="employee",
            employee_id=emp_map["EMP002"].id
        ),
        User(
            username="rohit.joshi",
            password_hash=hash_password("Employee@123"),
            role="employee",
            employee_id=emp_map["EMP009"].id
        ),
        User(
            username="karthik.menon",
            password_hash=hash_password("Employee@123"),
            role="employee",
            employee_id=emp_map["EMP007"].id
        ),
        User(
            username="meera.iyer",
            password_hash=hash_password("Employee@123"),
            role="employee",
            employee_id=emp_map["EMP010"].id
        ),
        # Manager role
        User(
            username="madhu.mitha",
            password_hash=hash_password("Madhu@123"),
            role="manager",
            employee_id=emp_map["EMP003"].id
        ),
        User(
            username="divya.kumar",
            password_hash=hash_password("Manager@123"),
            role="manager",
            employee_id=emp_map["EMP008"].id
        ),
        User(
            username="anjali.singh",
            password_hash=hash_password("Manager@123"),
            role="manager",
            employee_id=emp_map["EMP006"].id
        ),
        # HR role - can see all employee data
        User(
            username="nagendra.enukolu",
            password_hash=hash_password("Nagendra@123"),
            role="hr",
            employee_id=emp_map["EMP004"].id
        ),
        User(
            username="vikram.gupta",
            password_hash=hash_password("HR@123456"),
            role="hr",
            employee_id=emp_map["EMP005"].id
        ),
    ]

    db.add_all(users)
    db.commit()
    logger.info(f"[SEED] {len(users)} user accounts created")
    return users


def seed_leave_balances(db: Session):
    logger.info("[SEED] Creating leave balances...")

    employees = db.query(Employee).all()
    leave_balances = []

    for emp in employees:
        leave_balances.append(
            LeaveBalance(
                employee_id=emp.id,
                year=2026,
                casual_leave_total=12,
                casual_leave_used=2,
                sick_leave_total=10,
                sick_leave_used=1,
                earned_leave_total=15,
                earned_leave_used=3
            )
        )

    db.add_all(leave_balances)
    db.commit()
    logger.info(f"[SEED] {len(leave_balances)} leave balances created")
    return leave_balances


def seed_leave_requests(db: Session):
    logger.info("[SEED] Creating sample leave requests...")

    emp1 = db.query(Employee).filter_by(employee_id="EMP001").first()
    emp2 = db.query(Employee).filter_by(employee_id="EMP002").first()
    emp9 = db.query(Employee).filter_by(employee_id="EMP009").first()

    leave_requests = [
        LeaveRequest(
            employee_id=emp1.id,
            leave_type="casual_leave",
            start_date=datetime(2026, 5, 10),
            end_date=datetime(2026, 5, 11),
            days_count=2,
            reason="Personal work",
            status="approved"
        ),
        LeaveRequest(
            employee_id=emp2.id,
            leave_type="sick_leave",
            start_date=datetime(2026, 4, 20),
            end_date=datetime(2026, 4, 20),
            days_count=1,
            reason="Fever and cold",
            status="approved"
        ),
        LeaveRequest(
            employee_id=emp9.id,
            leave_type="earned_leave",
            start_date=datetime(2026, 6, 25),
            end_date=datetime(2026, 6, 27),
            days_count=3,
            reason="Family vacation",
            status="pending"
        ),
    ]

    db.add_all(leave_requests)
    db.commit()
    logger.info(f"[SEED] {len(leave_requests)} leave requests created")
    return leave_requests


def run_all_seeds():
    """
    Master function - runs all seeds in correct order.
    Run this ONCE to populate entire database.
    """
    from db.session import SessionLocal

    logger.info("=" * 50)
    logger.info("[SEED] Starting database seeding...")
    logger.info("=" * 50)

    db = SessionLocal()

    try:
        # Check if already seeded
        existing_departments = db.query(Department).count()
        existing_employees = db.query(Employee).count()
        existing_users = db.query(User).count()

        logger.info(
            f"[SEED] Existing counts -> departments: {existing_departments}, "
            f"employees: {existing_employees}, users: {existing_users}"
        )

        if existing_departments > 0 and existing_employees > 0 and existing_users > 0:
            logger.info("[SEED] Database already fully seeded. Skipping seed.")
            return

        # Run seeds in correct order
        # Orders matters - departments first, then employees, then users
        seed_departments(db)
        seed_employees(db)
        seed_users(db)
        seed_leave_balances(db)
        seed_leave_requests(db)

        logger.info("=" * 50)
        logger.info("[SEED] All seed data created successfully!")
        logger.info("=" * 50)

    except Exception as e:
        db.rollback()
        logger.error(f"[SEED] Seeding failed: {str(e)}")
        raise e
    finally:
        db.close()

    # Login Credentials Summary
    # Use these to test your system

    # USERNAME          PASSWORD        ROLE
    # dhiru_offl        Dhi@123         employee
    # deb.deep          Deb@123         employee
    # rohit.joshi       Employee@123    employee
    # karthik.menon     Employee@123    employee
    # meera.iyer        Employee@123    employee
    # madhu.mitha       Madhu@123       manager
    # divya.kumar       Manager@123     manager
    # anjali.singh      Manager@123     manager
    # nagendra.enukolu  Nagendra@123    hr
    # vikram.gupta      HR@123456       hr