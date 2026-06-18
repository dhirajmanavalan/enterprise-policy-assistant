from agents.specialists.query_router_agent import QueryRouterAgent

if __name__ == "__main__":
    agent = QueryRouterAgent()

    test_queries = [
        "What is the leave policy?",
        "What is my leave balance?",
        "What is the leave policy and how many earned leaves do I have left?"
    ]

    for query in test_queries:
        result = agent.classify_query(query)

        print("\n===== QUERY ROUTER RESULT =====")
        print("Query         :", result["query"])
        print("Query Type    :", result["query_type"])
        print("Target Agents :", result["target_agents"])
        print("Status        :", result["status"])