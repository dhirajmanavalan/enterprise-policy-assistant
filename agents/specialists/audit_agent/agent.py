# Saves user interaction logs into audit_logs table

import time
import uuid

from db.session import SessionLocal
from db.audit_repository import create_audit_log
from shared.logger import logger


class AuditAgent:
    def __init__(self):
        self.agent_name = "AuditAgent"

    def log_interaction(
        self,
        authenticated_user: dict,
        user_query: str,
        query_type: str,
        agents_used: list[str],
        final_answer: str,
        status: str = "success",
        processing_time_ms: float = 0.0
    ) -> dict:
        """
        Store one user interaction in audit_logs table.
        """
        logger.info(f"[{self.agent_name}] Creating audit log for query: {user_query}")

        db = SessionLocal()

        try:
            query_id = str(uuid.uuid4())

            audit = create_audit_log(
                db=db,
                query_id=query_id,
                user_id=authenticated_user["user_id"],
                username=authenticated_user["username"],
                role=authenticated_user["role"],
                department=authenticated_user.get("department"),
                raw_query=user_query,
                query_type=query_type,
                agents_used=agents_used,
                final_answer=final_answer,
                status=status,
                processing_time_ms=processing_time_ms
            )

            logger.info(f"[{self.agent_name}] Audit log created successfully: {query_id}")

            return {
                "agent": self.agent_name,
                "status": "success",
                "message": "Audit log created successfully",
                "audit_log_id": audit.id,
                "query_id": audit.query_id
            }

        except Exception as e:
            logger.exception(f"[{self.agent_name}] Failed to create audit log: {str(e)}")
            return {
                "agent": self.agent_name,
                "status": "error",
                "message": f"Failed to create audit log: {str(e)}"
            }

        finally:
            db.close()