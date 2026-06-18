from mistralai.client import Mistral
from shared.config import settings
from shared.logger import logger

API_KEY = settings.mistral_api_key
MODEL_NAME = settings.mistral_model_small

if not API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in project settings")

client = Mistral(api_key=API_KEY)


def generate_llm_response(system_prompt: str, user_prompt: str) -> str:
    logger.info(f"[LLM CLIENT] Calling Mistral model: {MODEL_NAME}")

    response = client.chat.complete(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()