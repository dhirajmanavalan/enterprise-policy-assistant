from shared.logger import logger
import re


class QueryRouterAgent:
    def __init__(self):
        self.agent_name = "QueryRouterAgent"

        self.policy_keywords = {
            "policy", "leave policy", "travel policy", "insurance policy",
            "wfh policy", "work from home policy", "rule", "rules",
            "guideline", "guidelines", "reimbursement", "carry forward",
            "eligibility", "coverage", "benefit", "benefits"
        }

        self.employee_keywords = {
            "my leave balance",
            "leave balance",
            "how many leaves do i have",
            "how many leaves do i have left",
            "leaves do i have left",
            "my leaves",
            "my profile",
            "profile",
            "my department",
            "department",
            "my manager",
            "manager",
            "my details",
            "employee id",
            "my leave requests",
            "leave requests",
            "my email",
            "my phone",
            "my designation",
            "my info",
            "show my leave requests",
            "my leave requests",
            "leave history",
            "show leave history",
            "leave status",
            "earned leave",
            "earned leaves",
            "how many earned leave do i have",
            "how many earned leave do i have left",
            "earned leave balance",
            "sick leave balance",
            "casual leave balance",
            "remaining leaves",
            "remaining leave balance"
        }

        self.leave_action_keywords = {
            "apply leave",
            "apply for leave",
            "request leave",
            "send leave",
            "submit leave",
            "take leave",
            "book leave",
            "want leave",
            "need leave",

            # Added support
            "want sick leave",
            "want casual leave",
            "want earned leave",

            "need sick leave",
            "need casual leave",
            "need earned leave",

            "sick leave from",
            "casual leave from",
            "earned leave from",

            "sick leave for",
            "casual leave for",
            "earned leave for"
        }

        self.leave_approval_keywords = {
            "approve leave",
            "reject leave",
            "approve request",
            "reject request",
            "approve leave request",
            "reject leave request"
        }



    def classify_query(self, query: str) -> dict:
        logger.info(f"[{self.agent_name}] Classifying query: {query}")

        query_lower = query.lower()

        # Leave Approval Detection
        has_leave_approval = any(
            keyword in query_lower
            for keyword in self.leave_approval_keywords
        )

        if has_leave_approval:
            result = {
                "agent": self.agent_name,
                "query": query,
                "query_type": "leave_approval",
                "target_agents": ["LeaveApprovalAgent"],
                "status": "success"
            }

            logger.info(
                f"[{self.agent_name}] Query classified as leave_approval -> ['LeaveApprovalAgent']"
            )
            return result

        # Smart Leave Request Detection
        has_date = bool(
            re.search(r"\d{4}-\d{2}-\d{2}", query_lower)
        )

        has_leave_type = any(
            leave in query_lower
            for leave in [
                "sick leave",
                "casual leave",
                "earned leave",
                "maternity leave",
                "paternity leave"
            ]
        )

        has_leave_action = any(
            keyword in query_lower
            for keyword in self.leave_action_keywords
        )

        if (has_date and has_leave_type) or has_leave_action:
            result = {
                "agent": self.agent_name,
                "query": query,
                "query_type": "leave_action",
                "target_agents": ["LeaveRequestAgent"],
                "status": "success"
            }

            logger.info(
                f"[{self.agent_name}] Query classified as leave_action -> ['LeaveRequestAgent']"
            )
            return result

        # Policy / Employee Detection
        has_policy = any(
            keyword in query_lower
            for keyword in self.policy_keywords
        )

        has_employee = (
                any(keyword in query_lower for keyword in self.employee_keywords)
                or "leave balance" in query_lower
                or "earned leave" in query_lower
                or "sick leave" in query_lower
                or "casual leave" in query_lower
        )

        if has_policy and has_employee:
            query_type = "hybrid"
            target_agents = ["PolicyRAGAgent", "EmployeeDataAgent"]

        elif has_policy:
            query_type = "policy"
            target_agents = ["PolicyRAGAgent"]

        elif has_employee:
            query_type = "employee"
            target_agents = ["EmployeeDataAgent"]

        else:
            query_type = "policy"
            target_agents = ["PolicyRAGAgent"]

        result = {
            "agent": self.agent_name,
            "query": query,
            "query_type": query_type,
            "target_agents": target_agents,
            "status": "success"
        }

        logger.info(
            f"[{self.agent_name}] Query classified as {query_type} -> {target_agents}"
        )

        return result