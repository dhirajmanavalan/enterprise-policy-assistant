from sqlalchemy import text
from db.session import engine
from shared.logger import logger


class LeaveRequestRepository:
    def create_leave_request(
        self,
        employee_id: int,
        leave_type: str,
        start_date: str,
        end_date: str,
        days_count: int,
        reason: str,
        status: str = "pending"
    ) -> dict:
        query = text("""
            INSERT INTO leave_requests
            (
                employee_id,
                leave_type,
                start_date,
                end_date,
                days_count,
                reason,
                status,
                approved_by,
                applied_on,
                updated_at
            )
            VALUES
            (
                :employee_id,
                :leave_type,
                :start_date,
                :end_date,
                :days_count,
                :reason,
                :status,
                NULL,
                NOW(),
                NOW()
            )
        """)

        with engine.begin() as connection:
            result = connection.execute(query, {
                "employee_id": employee_id,
                "leave_type": leave_type,
                "start_date": start_date,
                "end_date": end_date,
                "days_count": days_count,
                "reason": reason,
                "status": status
            })
            inserted_id = result.lastrowid

        logger.info(f"[LeaveRequestRepository] Leave request created with id: {inserted_id}")

        return {
            "id": inserted_id,
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "days_count": days_count,
            "reason": reason,
            "status": status,
            "approved_by": None
        }

    def get_pending_leave_days(self, employee_id: int, leave_type: str) -> int:
        query = text("""
            SELECT COALESCE(SUM(days_count), 0) AS pending_days
            FROM leave_requests
            WHERE employee_id = :employee_id
              AND leave_type = :leave_type
              AND status = 'pending'
        """)

        with engine.begin() as connection:
            row = connection.execute(query, {
                "employee_id": employee_id,
                "leave_type": leave_type
            }).mappings().first()

        return int(row["pending_days"]) if row else 0

    def get_leave_request_by_id(self, request_id: int) -> dict | None:
        query = text("""
            SELECT id, employee_id, leave_type, start_date, end_date,
                   days_count, reason, status, approved_by, applied_on, updated_at
            FROM leave_requests
            WHERE id = :request_id
        """)

        with engine.begin() as connection:
            row = connection.execute(query, {
                "request_id": request_id
            }).mappings().first()

        return dict(row) if row else None

    def approve_leave_request(self, request_id: int, approved_by: int) -> dict:
        query = text("""
            UPDATE leave_requests
            SET status = 'approved',
                approved_by = :approved_by,
                updated_at = NOW()
            WHERE id = :request_id
              AND status = 'pending'
        """)

        with engine.begin() as connection:
            result = connection.execute(query, {
                "request_id": request_id,
                "approved_by": approved_by
            })

        if result.rowcount == 0:
            return {
                "status": "failed",
                "message": "No pending leave request found for approval"
            }

        logger.info(f"[LeaveRequestRepository] Leave request approved: {request_id}")

        return {
            "status": "success",
            "message": f"Leave request {request_id} approved successfully"
        }

    def reject_leave_request(self, request_id: int, approved_by: int) -> dict:
        query = text("""
            UPDATE leave_requests
            SET status = 'rejected',
                approved_by = :approved_by,
                updated_at = NOW()
            WHERE id = :request_id
              AND status = 'pending'
        """)

        with engine.begin() as connection:
            result = connection.execute(query, {
                "request_id": request_id,
                "approved_by": approved_by
            })

        if result.rowcount == 0:
            return {
                "status": "failed",
                "message": "No pending leave request found for rejection"
            }

        logger.info(f"[LeaveRequestRepository] Leave request rejected: {request_id}")

        return {
            "status": "success",
            "message": f"Leave request {request_id} rejected successfully"
        }