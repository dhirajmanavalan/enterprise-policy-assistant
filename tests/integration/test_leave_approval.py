from agents.orchestrator.agent import EnterpriseAssistantOrchestrator

orchestrator = EnterpriseAssistantOrchestrator()

result = orchestrator.handle_request(
    username="vilas",
    password="Vilas@123",
    user_query="Approve leave request 9"
)

print("\n===== LEAVE APPROVAL RESULT =====")
print("Status        :", result["status"])
print("Query Type    :", result["query_type"])
print("Target Agents :", result["target_agents"])
print("Response      :", result["response_result"]["final_response"])
print("Audit Result  :", result["audit_result"])
print("Approval Result :", result["leave_approval_result"])