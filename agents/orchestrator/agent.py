# MAIN ORCHESTRATOR
# Connects all agents in one complete flow
import time

from agents.specialists.authentication_agent import AuthenticationAgent
from agents.specialists.query_router_agent import QueryRouterAgent
from agents.specialists.policy_rag_agent import PolicyRAGAgent
from agents.specialists.employee_data_agent import EmployeeDataAgent
from agents.specialists.leave_request_agent import LeaveRequestAgent
from agents.specialists.leave_approval_agent import LeaveApprovalAgent
from agents.specialists.response_agent import ResponseAgent
from agents.specialists.audit_agent import AuditAgent
from shared.logger import logger


class EnterpriseAssistantOrchestrator:
    def __init__(self):
        self.authentication_agent = AuthenticationAgent()
        self.query_router_agent = QueryRouterAgent()
        self.policy_rag_agent = PolicyRAGAgent()
        self.employee_data_agent = EmployeeDataAgent()
        self.leave_request_agent = LeaveRequestAgent()
        self.leave_approval_agent = LeaveApprovalAgent()
        self.response_agent = ResponseAgent()
        self.audit_agent = AuditAgent()

        self.agent_name = "EnterpriseAssistantOrchestrator"

    def handle_request(self, username: str, password: str, user_query: str) -> dict:
        logger.info(f"[{self.agent_name}] Starting request for user: {username}")
        start_time = time.time()

        auth_result = self.authentication_agent.authenticate(username, password)
        if not auth_result.get("authenticated"):
            logger.warning(f"[{self.agent_name}] Authentication failed for: {username}")
            return {
                "status": "failed",
                "stage": "authentication",
                "message": auth_result.get("message", "Authentication failed")
            }

        authenticated_user = auth_result["user"]

        router_result = self.query_router_agent.classify_query(user_query)
        query_type = router_result["query_type"]
        target_agents = router_result["target_agents"]

        policy_result = None
        employee_result = None
        leave_request_result = None
        leave_approval_result = None

        if "PolicyRAGAgent" in target_agents:
            policy_result = self.policy_rag_agent.handle_query(user_query)

        if "EmployeeDataAgent" in target_agents:
            employee_result = self.employee_data_agent.handle_query(
                authenticated_user["username"],
                user_query
            )

        if "LeaveRequestAgent" in target_agents:
            employee_result = self.employee_data_agent.handle_query(
                authenticated_user["username"]
            )

            leave_request_result = self.leave_request_agent.handle_query(
                user_query=user_query,
                authenticated_user=authenticated_user,
                employee_result=employee_result
            )

        if "LeaveApprovalAgent" in target_agents:
            leave_approval_result = self.leave_approval_agent.handle_query(
                user_query=user_query,
                authenticated_user=authenticated_user
            )

        if query_type == "leave_action":
            final_response = leave_request_result["message"]
            agents_used = ["LeaveRequestAgent", "EmployeeDataAgent"]
            response_result = {
                "status": leave_request_result["status"],
                "final_response": final_response,
                "agents_used": agents_used
            }
        elif query_type == "leave_approval":
            final_response = leave_approval_result["message"]
            agents_used = ["LeaveApprovalAgent"]
            response_result = {
                "status": leave_approval_result["status"],
                "final_response": final_response,
                "agents_used": agents_used
            }
        else:
            response_result = self.response_agent.generate_response(
                user_query=user_query,
                policy_result=policy_result,
                employee_result=employee_result
            )

            final_response = response_result["final_response"]
            agents_used = response_result["agents_used"]

        processing_time_ms = round((time.time() - start_time) * 1000, 2)

        audit_result = self.audit_agent.log_interaction(
            authenticated_user=authenticated_user,
            user_query=user_query,
            query_type=query_type,
            agents_used=agents_used,
            final_answer=final_response,
            status=response_result["status"],
            processing_time_ms=processing_time_ms
        )

        logger.info(f"[{self.agent_name}] Request completed successfully")

        return {
            "status": response_result["status"],
            "authenticated_user": authenticated_user,
            "query_type": query_type,
            "target_agents": target_agents,
            "policy_result": policy_result,
            "employee_result": employee_result,
            "leave_request_result": leave_request_result,
            "leave_approval_result": leave_approval_result,
            "response_result": response_result,
            "audit_result": audit_result
        }