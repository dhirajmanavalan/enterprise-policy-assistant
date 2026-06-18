import re
from datetime import datetime
from shared.logger import logger
from db.leave_request_repository import LeaveRequestRepository


class LeaveRequestAgent:
    def __init__(self):
        self.agent_name = "LeaveRequestAgent"
        self.repo = LeaveRequestRepository()

        self.leave_type_map = {
            "casual": "casual_leave",
            "casual leave": "casual_leave",
            "sick": "sick_leave",
            "sick leave": "sick_leave",
            "earned": "earned_leave",
            "earned leave": "earned_leave",
            "maternity": "maternity_leave",
            "maternity leave": "maternity_leave",
            "paternity": "paternity_leave",
            "paternity leave": "paternity_leave",
        }

    def handle_query(self, user_query: str, authenticated_user: dict, employee_result: dict = None) -> dict:
        logger.info(f"[{self.agent_name}] Processing leave request: {user_query}")
        logger.info(f"[{self.agent_name}] authenticated_user = {authenticated_user}")

        try:
            parsed = self.parse_leave_request(user_query)

            if not parsed["success"]:
                return {
                    "agent": self.agent_name,
                    "status": "failed",
                    "message": parsed["message"]
                }

            leave_type = parsed["leave_type"]
            start_date = parsed["start_date"]
            end_date = parsed["end_date"]
            total_days = parsed["total_days"]
            reason = parsed["reason"]

            if employee_result is None:
                return {
                    "agent": self.agent_name,
                    "status": "failed",
                    "message": "Employee leave balance is required for leave validation"
                }

            leave_balance_data = employee_result.get("data", {}).get("leave_balance", {})
            logger.info(f"[{self.agent_name}] leave_balance_data = {leave_balance_data}")

            raw_balance = leave_balance_data.get(leave_type, 0)

            if isinstance(raw_balance, dict):
                available_balance = (
                    raw_balance.get("remaining")
                    or raw_balance.get("available")
                    or raw_balance.get("balance")
                    or raw_balance.get("total")
                    or 0
                )
            else:
                available_balance = raw_balance

            db_employee_id = self.get_numeric_employee_id(authenticated_user)

            pending_days = self.repo.get_pending_leave_days(
                db_employee_id,
                leave_type
            )

            effective_available = int(available_balance) - int(pending_days)

            if effective_available < total_days:
                return {
                    "agent": self.agent_name,
                    "status": "failed",
                    "message": f"Insufficient leave balance. Available: {effective_available}, Requested: {total_days}",
                    "leave_type": leave_type,
                    "available_balance": effective_available,
                    "requested_days": total_days
                }

            saved_request = self.repo.create_leave_request(
                employee_id=db_employee_id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                days_count=total_days,
                reason=reason,
                status="pending"
            )

            logger.info(f"[{self.agent_name}] Leave request submitted successfully")

            return {
                "agent": self.agent_name,
                "status": "success",
                "message": f"Your {leave_type} request for {total_days} day(s) has been submitted and is pending approval.",
                "data": saved_request
            }

        except Exception as e:
            logger.error(f"[{self.agent_name}] Error: {str(e)}")
            return {
                "agent": self.agent_name,
                "status": "failed",
                "message": str(e)
            }

    def get_numeric_employee_id(self, authenticated_user: dict) -> int:
        """
        Always use Employee table primary key.
        Example:
        employees.id = 11

        Do NOT use:
        users.id
        EMP011
        """

        employee_db_id = authenticated_user.get("employee_db_id")

        if employee_db_id is None:
            raise ValueError(
                "Authenticated user does not contain employee_db_id"
            )

        return int(employee_db_id)

    def parse_leave_request(self, user_query: str) -> dict:
        query_lower = user_query.lower()

        leave_type = None
        for key, value in self.leave_type_map.items():
            if key in query_lower:
                leave_type = value
                break

        if not leave_type:
            return {
                "success": False,
                "message": (
                    "Please specify the leave type: "
                    "casual, sick, earned, maternity, or paternity."
                )
            }

        date_matches = re.findall(r"\d{4}-\d{2}-\d{2}", user_query)
        if len(date_matches) < 2:
            return {
                "success": False,
                "message": "Please provide start date and end date in YYYY-MM-DD format."
            }

        start_date_obj = datetime.strptime(date_matches[0], "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(date_matches[1], "%Y-%m-%d").date()

        if start_date_obj > end_date_obj:
            return {
                "success": False,
                "message": "Start date cannot be after end date."
            }

        total_days = (end_date_obj - start_date_obj).days + 1

        reason = "Personal reason"
        if "because" in query_lower:
            idx = query_lower.index("because")
            reason = user_query[idx + len("because"):].strip()

        return {
            "success": True,
            "leave_type": leave_type,
            "start_date": str(start_date_obj),
            "end_date": str(end_date_obj),
            "total_days": total_days,
            "reason": reason
        }