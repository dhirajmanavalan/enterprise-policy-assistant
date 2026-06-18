from agents.specialists.audit_agent import AuditAgent

if __name__ == "__main__":
    agent = AuditAgent()

    authenticated_user = {
        "user_id": 1,
        "username": "abidhi",
        "role": "employee",
        "department": "Engineering"
    }

    result = agent.log_interaction(
        authenticated_user=authenticated_user,
        user_query="What is the leave carry forward rule and how many leaves do I have left?",
        query_type="hybrid",
        agents_used=["PolicyRAGAgent", "EmployeeDataAgent", "ResponseAgent"],
        final_answer="Earned leave can be carried forward up to 30 days. Your current leave balance is Casual: 12, Sick: 10, Earned: 15.",
        status="success",
        processing_time_ms=142.7
    )

    print("\n===== AUDIT AGENT RESULT =====")
    print("Agent       :", result["agent"])
    print("Status      :", result["status"])
    print("Message     :", result["message"])
    print("Audit Log ID:", result.get("audit_log_id"))
    print("Query ID    :", result.get("query_id"))