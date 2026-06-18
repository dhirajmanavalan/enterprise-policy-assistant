# These are Fixed values used across the entire project
# In this file I Always import from here
# Fixed values used across the entire project

# Query Types
# Used by Query Router Agent to classify
# what type of question the user asked
class QueryType:
    POLICY = "POLICY"          # Question about company policy
    EMPLOYEE = "EMPLOYEE"      # Question about personal employee data
    LEAVE_ACTION = "LEAVE_ACTION"
    HYBRID = "HYBRID"          # Question needs both policy + employee data
    UNKNOWN = "UNKNOWN"        # Cannot classify the question


# User Roles
# Used by Authentication Agent
# Controls what data each role can access
class UserRole:
    EMPLOYEE = "employee"      # Regular employee - sees own data only
    HR = "hr"                  # HR team - sees all employee data
    ADMIN = "admin"            # Admin - full system access
    MANAGER = "manager"        # Manager - sees team data


# Agent Names
# Used in audit logs to record
# which agent handled the request
class AgentName:
    ORCHESTRATOR = "orchestrator"
    AUTH = "authentication_agent"
    ROUTER = "query_router_agent"
    POLICY_RAG = "policy_rag_agent"
    EMPLOYEE_DATA = "employee_data_agent"
    LEAVE_REQUEST = "leave_request_agent"
    RESPONSE = "response_agent"
    AUDIT = "audit_agent"


# Policy Document Types
# Used by RAG agent to tag
# which policy document the answer came from
class PolicyType:
    LEAVE = "leave_policy"
    TRAVEL = "travel_policy"
    INSURANCE = "insurance_policy"
    WFH = "wfh_policy"
    GENERAL = "general_policy"


# Response Status
# Used in API responses to tell
# the frontend what happened
class ResponseStatus:
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    UNAUTHORIZED = "unauthorized"


# Department Names
# Used in employee database
class Department:
    ENGINEERING = "Engineering"
    HR = "Human Resources"
    FINANCE = "Finance"
    MARKETING = "Marketing"
    OPERATIONS = "Operations"
    SALES = "Sales"


# Leave Types
# Used in leave balance table
class LeaveType:
    CASUAL = "casual_leave"
    SICK = "sick_leave"
    EARNED = "earned_leave"
    MATERNITY = "maternity_leave"
    PATERNITY = "paternity_leave"

class LeaveApprovalStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

# API Response Messages
# Standard messages used across all routes
class Message:
    LOGIN_SUCCESS = "Login successful"
    LOGIN_FAILED = "Invalid username or password"
    UNAUTHORIZED = "You are not authorized to access this resource"
    TOKEN_EXPIRED = "Your session has expired. Please login again"
    QUERY_SUCCESS = "Query processed successfully"
    QUERY_FAILED = "Failed to process your query. Please try again"
    SERVER_ERROR = "Internal server error. Please contact admin"
    LEAVE_REQUEST_CREATED = "Leave request submitted successfully"
    INSUFFICIENT_LEAVE_BALANCE = "Insufficient leave balance"
    INVALID_LEAVE_TYPE = "Invalid leave type"
    INVALID_DATE_RANGE = "Invalid leave date range"