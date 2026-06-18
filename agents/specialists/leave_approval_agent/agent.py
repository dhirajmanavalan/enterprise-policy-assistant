import re

from db.session import SessionLocal
from db.models import LeaveRequest
from db.employee_repository import update_leave_balance_after_approval
from shared.logger import logger


class LeaveApprovalAgent:
    def __init__(self):
        self.agent_name = "LeaveApprovalAgent"

    def handle_query(self, user_query: str, authenticated_user: dict) -> dict:
        db = SessionLocal()

        role = authenticated_user.get("role", "").lower()

        # Only HR, Manager, Admin can approve/reject
        if role not in ["hr", "manager", "admin"]:
            return {
                "agent": self.agent_name,
                "status": "failed",
                "message": "You are not authorized to approve or reject leave requests."
            }

        try:
            logger.info(f"[{self.agent_name}] Processing request: {user_query}")
            logger.info(f"[{self.agent_name}] authenticated_user: {authenticated_user}")

            approver_username = authenticated_user.get("username", "unknown")
            approver_id = authenticated_user.get("employee_db_id") or authenticated_user.get("user_id")

            if approver_id is None:
                return {
                    "agent": self.agent_name,
                    "status": "failed",
                    "message": "Authenticated user does not contain a numeric approver ID"
                }

            approver_id = int(approver_id)

            match = re.search(r"(\d+)", user_query)

            if not match:
                return {
                    "agent": self.agent_name,
                    "status": "failed",
                    "message": "No leave request ID found in query"
                }

            request_id = int(match.group(1))

            leave_request = db.query(LeaveRequest).filter_by(id=request_id).first()

            if not leave_request:
                return {
                    "agent": self.agent_name,
                    "status": "failed",
                    "message": f"Leave request {request_id} not found"
                }

            current_status = str(leave_request.status).lower()

            if current_status in ["approved", "rejected"]:
                return {
                    "agent": self.agent_name,
                    "status": "failed",
                    "message": f"Leave request {request_id} is already {current_status}"
                }

            query_lower = user_query.lower()

            # =====================
            # REJECT FLOW
            # =====================
            if "reject" in query_lower:

                leave_request.status = "rejected"
                leave_request.approved_by = approver_id

                db.commit()
                db.refresh(leave_request)

                logger.info(
                    f"[{self.agent_name}] Leave request {request_id} rejected successfully"
                )

                return {
                    "agent": self.agent_name,
                    "status": "success",
                    "message": f"Leave request {request_id} rejected successfully",
                    "request_id": request_id,
                    "employee_id": leave_request.employee_id,
                    "leave_type": leave_request.leave_type,
                    "days_count": leave_request.days_count,
                    "approved_by": approver_username,
                    "approved_by_id": approver_id
                }

            # =====================
            # APPROVE FLOW
            # =====================

            leave_request.status = "approved"
            leave_request.approved_by = approver_id

            db.commit()
            db.refresh(leave_request)

            balance_result = update_leave_balance_after_approval(
                db=db,
                employee_db_id=leave_request.employee_id,
                leave_type=leave_request.leave_type,
                days_count=leave_request.days_count,
                year=leave_request.start_date.year
            )

            if balance_result["status"] != "success":
                logger.warning(
                    f"[{self.agent_name}] Leave request {request_id} approved, "
                    f"but balance update failed: {balance_result['message']}"
                )

                return {
                    "agent": self.agent_name,
                    "status": "success",
                    "message": f"Leave request {request_id} approved successfully, but balance update failed: {balance_result['message']}",
                    "request_id": request_id,
                    "employee_id": leave_request.employee_id,
                    "leave_type": leave_request.leave_type,
                    "days_count": leave_request.days_count,
                    "approved_by": approver_username,
                    "approved_by_id": approver_id,
                    "balance_update_status": "failed"
                }

            logger.info(
                f"[{self.agent_name}] Leave request {request_id} approved successfully"
            )

            return {
                "agent": self.agent_name,
                "status": "success",
                "message": f"Leave request {request_id} approved successfully and balance updated",
                "request_id": request_id,
                "employee_id": leave_request.employee_id,
                "leave_type": leave_request.leave_type,
                "days_count": leave_request.days_count,
                "approved_by": approver_username,
                "approved_by_id": approver_id,
                "balance_update_status": "success"
            }

        except Exception as e:
            db.rollback()

            logger.error(
                f"[{self.agent_name}] Error: {str(e)}"
            )

            return {
                "agent": self.agent_name,
                "status": "failed",
                "message": str(e)
            }

        finally:
            db.close()