from agents.specialists.policy_rag_agent import PolicyRAGAgent

if __name__ == "__main__":
    agent = PolicyRAGAgent()

    query = "What is the leave carry forward rule?"
    result = agent.handle_query(query)

    print("\n===== POLICY RAG AGENT RESULT =====")
    print("Agent       :", result["agent"])
    print("Query Type  :", result["query_type"])
    print("Status      :", result["status"])
    print("User Query  :", result["user_query"])
    print("\nRetrieved Context:\n")
    print(result["retrieved_context"])