from pathlib import Path
from dotenv import dotenv_values

env_path = Path(__file__).resolve().parent / ".env"
print("ENV exists:", env_path.exists())
print("ENV path:", env_path)

values = dotenv_values(env_path)
print("ENV keys:", list(values.keys()))
print("MISTRAL_API_KEY raw:", values.get("MISTRAL_API_KEY"))
print("MISTRAL_MODEL_SMALL raw:", values.get("MISTRAL_MODEL_SMALL"))
print("MISTRAL_MODEL_LARGE raw:", values.get("MISTRAL_MODEL_LARGE"))