from agents.specialists.employee_data_agent import EmployeeDataAgent

if __name__ == "__main__":
    agent = EmployeeDataAgent()

    result = agent.handle_query("abidhi")

    print("\n===== EMPLOYEE DATA AGENT RESULT =====")
    print("Agent      :", result["agent"])
    print("Query Type :", result["query_type"])
    print("Status     :", result["status"])
    print("Message    :", result["message"])
    print("Data       :", result["data"])