# Shared Pydantic models used across project
# These are data shapes — not database tables
# Used for passing data between agents

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from shared.constants import QueryType, ResponseStatus, AgentName


# User Session Model
# Holds logged-in user information
# Passed between agents during a session
class UserSession(BaseModel):
    user_id: int
    username: str
    role: str
    department: str
    employee_id: str
    token: str


# Query Model
# Represents the user's question
# after it enters the system
class QueryModel(BaseModel):
    query_id: str = Field(description="Unique ID for this query")
    user_session: UserSession
    raw_query: str = Field(description="Original question from user")
    query_type: str = Field(default=QueryType.UNKNOWN)
    timestamp: datetime = Field(default_factory=datetime.now)


# Policy RAG Result
# What the Policy RAG Agent returns
# Contains answer + source document info
class PolicyRAGResult(BaseModel):
    answer: str
    source_documents: List[str] = []
    policy_type: str = ""
    confidence_score: float = 0.0
    retrieved_chunks: int = 0


# Employee Data Result
# What the Employee Data Agent returns
# Contains personal employee information
class EmployeeDataResult(BaseModel):
    employee_id: str
    full_name: str
    department: str
    designation: str
    data: dict = {}
    found: bool = False

class LeaveRequestInput(BaseModel):
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    total_days: int = 0
    attachment_path: Optional[str] = None


class LeaveRequestResult(BaseModel):
    request_id: str
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    total_days: int
    approval_status: str
    message: str


# Agent Result
# Standard result shape every agent returns
# Makes it easy to pass between agents
class AgentResult(BaseModel):
    agent_name: str
    status: str = ResponseStatus.SUCCESS
    data: dict = {}
    error: Optional[str] = None
    processing_time_ms: float = 0.0


# Final Response Model
# The final answer sent back to the user
# through the API
class FinalResponse(BaseModel):
    query_id: str
    answer: str
    query_type: str
    agents_used: List[str] = []
    sources: List[str] = []
    status: str = ResponseStatus.SUCCESS
    timestamp: datetime = Field(default_factory=datetime.now)
    processing_time_ms: float = 0.0


# Audit Log Model
# What gets saved to audit table
# for every interaction
class AuditLogModel(BaseModel):
    query_id: str
    user_id: int
    username: str
    role: str
    raw_query: str
    query_type: str
    agents_used: List[str] = []
    final_answer: str
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    processing_time_ms: float = 0.0