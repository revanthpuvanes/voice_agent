import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("API key not found")

client = MistralClient(api_key=api_key)

def call_mistral(prompt):
    response = client.chat(
        model="mistral-small",
        messages=[
            ChatMessage(role="user", content=prompt)
        ]
    )
    return response.choices[0].message.content