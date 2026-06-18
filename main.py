from agents.orchestrator.agent import EnterpriseAssistantOrchestrator

def main():
    orchestrator = EnterpriseAssistantOrchestrator()

    print("=== Enterprise Policy Assistant ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    query = input("Ask your question: ").strip()

    result = orchestrator.handle_request(
        username=username,
        password=password,
        user_query=query
    )

    print("\n========== RESULT ==========")

    print(f"Status           : {result['status']}")
    print(f"Query Type       : {result['query_type']}")

    print("\n----- Authenticated User -----")
    user = result["authenticated_user"]

    print(f"Username         : {user['username']}")
    print(f"Role             : {user['role']}")
    print(f"Employee ID      : {user['employee_id']}")
    print(f"Full Name        : {user['full_name']}")
    print(f"Department       : {user['department']}")

    if result["leave_approval_result"]:
        approval = result["leave_approval_result"]

        print("\n----- Leave Approval Result -----")
        print(f"Request ID       : {approval['request_id']}")
        print(f"Employee DB ID   : {approval['employee_id']}")
        print(f"Leave Type       : {approval['leave_type']}")
        print(f"Days Count       : {approval['days_count']}")
        print(f"Approved By      : {approval['approved_by']}")
        print(f"Message          : {approval['message']}")

    print("\n----- Final Response -----")
    print(result["response_result"]["final_response"])

    print("\n----- Audit Log -----")
    audit = result["audit_result"]

    print(f"Audit Log ID     : {audit['audit_log_id']}")
    print(f"Query ID         : {audit['query_id']}")

    print("\n============================")

if __name__ == "__main__":
    main()