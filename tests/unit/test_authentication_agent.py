from agents.specialists.authentication_agent import AuthenticationAgent

if __name__ == "__main__":
    agent = AuthenticationAgent()

    result = agent.authenticate("abidhi", "Abi@123")

    print("\n===== AUTHENTICATION AGENT RESULT =====")
    print(result)