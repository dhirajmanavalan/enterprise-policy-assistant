# Handles policy-related user questions.
# using the RAG pipeline.

from rag.pipeline import query_rag
from shared.logger import logger


class PolicyRAGAgent:
    def __init__(self, top_k: int = 3):
        self.top_k = top_k
        self.agent_name = "PolicyRAGAgent"

    def handle_query(self, user_query: str) -> dict:
        """
        Process a policy-related user query.

        Steps:
        1. Receive user query
        2. Call RAG pipeline
        3. Return structured response
        """
        logger.info(f"[{self.agent_name}] Received query: {user_query}")

        context = query_rag(user_query, top_k=self.top_k)

        status = (
            "success"
            if context and context != "No relevant policy context found."
            else "no_result"
        )

        result = {
            "agent": self.agent_name,
            "query_type": "policy",
            "user_query": user_query,
            "retrieved_context": context,
            "status": status
        }

        logger.info(f"[{self.agent_name}] Completed query with status: {status}")
        return result