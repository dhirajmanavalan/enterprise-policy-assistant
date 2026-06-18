# All database query functions for audit logs
# Audit Agent uses this file

from sqlalchemy.orm import Session
from db.models import AuditLog
from shared.logger import logger
from datetime import datetime
from typing import List


def create_audit_log(
    db: Session,
    query_id: str,
    user_id: int,
    username: str,
    role: str,
    department: str,
    raw_query: str,
    query_type: str,
    agents_used: List[str],
    final_answer: str,
    status: str,
    processing_time_ms: float
) -> AuditLog:
    """
    Save one interaction to audit_logs table.
    Called by Audit Agent after every query.
    """
    audit = AuditLog(
        query_id=query_id,
        user_id=user_id,
        username=username,
        role=role,
        department=department,
        raw_query=raw_query,
        query_type=query_type,
        agents_used=", ".join(agents_used),
        final_answer=final_answer,
        status=status,
        processing_time_ms=processing_time_ms,
        timestamp=datetime.now()
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

    logger.debug(f"[AUDIT REPO] Log saved for query: {query_id}")
    return audit


def get_audit_logs_by_user(db: Session, username: str) -> List[AuditLog]:
    """Get all audit logs for a specific user"""
    return db.query(AuditLog).filter_by(
        username=username
    ).order_by(AuditLog.timestamp.desc()).all()


def get_all_audit_logs(db: Session, limit: int = 100) -> List[AuditLog]:
    """Get recent audit logs - for HR and Admin only"""
    return db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).limit(limit).all()