from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("API Key Found:", bool(api_key))

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Say Hello in one line"
        }
    ]
)

print("\nResponse:")
print(response.choices[0].message.content)