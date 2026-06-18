from mistralai.client import Mistral
from shared.config import settings

client = Mistral(api_key=settings.mistral_api_key)

response = client.chat.complete(
    model=settings.mistral_model_small,
    messages=[
        {"role": "user", "content": "Say hello in one short sentence."}
    ]
)

print(response.choices[0].message.content)