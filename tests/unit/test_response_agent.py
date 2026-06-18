from agents.specialists.response_agent import ResponseAgent
from agents.specialists.employee_data_agent import EmployeeDataAgent
from agents.specialists.policy_rag_agent import PolicyRAGAgent


if __name__ == "__main__":
    response_agent = ResponseAgent()
    employee_agent = EmployeeDataAgent()
    policy_agent = PolicyRAGAgent()

    user_query = "What is the leave carry forward rule and how many leaves do I have left?"
    username = "abidhi"

    policy_result = policy_agent.handle_query(user_query)
    employee_result = employee_agent.handle_query(username)

    result = response_agent.generate_response(
        user_query=user_query,
        policy_result=policy_result,
        employee_result=employee_result
    )

    print("\n===== RESPONSE AGENT RESULT =====")
    print("Agent       :", result["agent"])
    print("Status      :", result["status"])
    print("Agents Used :", result["agents_used"])
    print("User Query  :", result["user_query"])
    print("\nFinal Response:\n")
    print(result["final_response"])