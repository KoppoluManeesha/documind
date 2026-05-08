import os

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def analyze_document(text: str):
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[
                {"role": "user", "content": f"Analyze this document:\n\n{text}"}
            ]
        )
        return response.content[0].text

    except Exception as e:
        return f"[MOCK AI RESPONSE] Analysis unavailable. Reason: {str(e)}"