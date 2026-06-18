from pathlib import Path
import json

from shared.logger import logger
from shared.llm_client import generate_llm_response


class ResponseAgent:
    def __init__(self):
        self.agent_name = "ResponseAgent"
        self.prompt_path = Path(__file__).parent / "prompt.txt"

    def _load_prompt(self) -> str:
        with open(self.prompt_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def _prepare_policy_result(self, policy_result: dict | None) -> dict:
        if not policy_result:
            return {"available": False, "message": "No policy result available"}

        return {
            "available": policy_result.get("status") == "success",
            "status": policy_result.get("status"),
            "message": policy_result.get("message"),
            "retrieved_context": policy_result.get("retrieved_context", "")
        }

    def _prepare_employee_result(self, employee_result: dict | None) -> dict:
        if not employee_result:
            return {"available": False, "message": "No employee result available"}

        return {
            "available": employee_result.get("status") == "success",
            "status": employee_result.get("status"),
            "message": employee_result.get("message"),
            "data": employee_result.get("data", {})
        }

    def _build_user_prompt(
        self,
        user_query: str,
        policy_result: dict | None = None,
        employee_result: dict | None = None
    ) -> str:
        policy_payload = self._prepare_policy_result(policy_result)
        employee_payload = self._prepare_employee_result(employee_result)

        return f"""
User Query:
{user_query}

Policy Result:
{json.dumps(policy_payload, indent=2)}

Employee Result:
{json.dumps(employee_payload, indent=2)}

Task:
Generate the final answer for the employee using only the above information.
""".strip()

    def generate_response(
        self,
        user_query: str,
        policy_result: dict | None = None,
        employee_result: dict | None = None
    ) -> dict:
        logger.info(f"[{self.agent_name}] Generating final LLM-based response for query: {user_query}")

        try:
            system_prompt = self._load_prompt()
            user_prompt = self._build_user_prompt(
                user_query=user_query,
                policy_result=policy_result,
                employee_result=employee_result
            )

            final_text = generate_llm_response(system_prompt, user_prompt)

            agents_used = []
            if policy_result:
                agents_used.append(policy_result.get("agent", "PolicyRAGAgent"))
            if employee_result:
                agents_used.append(employee_result.get("agent", "EmployeeDataAgent"))

            logger.info(f"[{self.agent_name}] Final LLM response generated successfully")

            return {
                "agent": self.agent_name,
                "status": "success",
                "user_query": user_query,
                "final_response": final_text,
                "agents_used": agents_used
            }

        except Exception as e:
            logger.exception(f"[{self.agent_name}] Failed to generate LLM response: {str(e)}")
            return {
                "agent": self.agent_name,
                "status": "error",
                "user_query": user_query,
                "final_response": f"Failed to generate response: {str(e)}",
                "agents_used": []
            }