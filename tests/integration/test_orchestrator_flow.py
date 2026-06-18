from agents.orchestrator import EnterpriseAssistantOrchestrator

if __name__ == "__main__":
    orchestrator = EnterpriseAssistantOrchestrator()

    result = orchestrator.handle_request(
        username="guhan",
        password="Guhan@123",
        user_query="What is the leave carry forward rule and how many leaves do I have left?"
    )

    print("\n===== ORCHESTRATOR RESULT =====")
    print("Status        :", result["status"])

    if result["status"] == "success":
        print("User          :", result["authenticated_user"]["username"])
        print("Role          :", result["authenticated_user"]["role"])
        print("Query Type    :", result["query_type"])
        print("Target Agents :", result["target_agents"])
        print("\nFinal Response:\n")
        print(result["response_result"]["final_response"])
        print("\nAudit Result:")
        print(result["audit_result"])
    else:
        print("Stage         :", result.get("stage"))
        print("Message       :", result.get("message"))