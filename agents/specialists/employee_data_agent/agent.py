# Retrieves employee-specific data from DB

from db.session import SessionLocal
from db.employee_repository import (
    get_employee_profile,
    get_employee_by_username,
    get_leave_requests_by_employee
)
from shared.logger import logger


class EmployeeDataAgent:
    def __init__(self):
        self.agent_name = "EmployeeDataAgent"

    def handle_query(self, username: str, user_query: str = "") -> dict:
        logger.info(f"[{self.agent_name}] Fetching employee data for: {username}")

        db = SessionLocal()

        try:
            employee = get_employee_by_username(db, username)

            if not employee:
                return {
                    "agent": self.agent_name,
                    "query_type": "employee",
                    "status": "failed",
                    "message": "Employee not found",
                    "data": None
                }

            query_lower = user_query.lower()

            # Leave Requests
            if any(keyword in query_lower for keyword in [
                "show my leave requests",
                "my leave requests",
                "leave history",
                "show leave history",
                "leave status"
            ]):

                requests = get_leave_requests_by_employee(
                    db,
                    employee.id
                )

                leave_data = []

                for req in requests:
                    leave_data.append({
                        "request_id": req.id,
                        "leave_type": req.leave_type,
                        "start_date": str(req.start_date.date()),
                        "end_date": str(req.end_date.date()),
                        "days_count": req.days_count,
                        "status": req.status
                    })

                return {
                    "agent": self.agent_name,
                    "query_type": "leave_requests",
                    "status": "success",
                    "message": "Leave requests fetched successfully",
                    "data": leave_data
                }

            # Default Profile Flow
            profile = get_employee_profile(db, username)

            if not profile.get("found"):
                return {
                    "agent": self.agent_name,
                    "query_type": "employee",
                    "status": "failed",
                    "message": profile.get("error", "Employee not found"),
                    "data": None
                }

            return {
                "agent": self.agent_name,
                "query_type": "employee",
                "status": "success",
                "message": "Employee data fetched successfully",
                "data": profile
            }

        except Exception as e:
            logger.exception(
                f"[{self.agent_name}] Error fetching employee data for {username}: {str(e)}"
            )

            return {
                "agent": self.agent_name,
                "query_type": "employee",
                "status": "error",
                "message": f"System error: {str(e)}",
                "data": None
            }

        finally:
            db.close()