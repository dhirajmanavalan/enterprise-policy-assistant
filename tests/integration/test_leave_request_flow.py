from agents.orchestrator import EnterpriseAssistantOrchestrator

orchestrator = EnterpriseAssistantOrchestrator()

result = orchestrator.handle_request(
    username="pallavi",
    password="Pallavi@123",
    user_query="Apply casual leave from 2026-06-17 to 2026-06-24 because of attending new interview"
)

print("\n===== LEAVE REQUEST RESULT =====")
print("Status        :", result["status"])
print("Query Type    :", result["query_type"])
print("Target Agents :", result["target_agents"])
print("Response      :", result["response_result"]["final_response"])
print("Audit Result  :", result["audit_result"])
print("Leave Result  :", result["leave_request_result"])