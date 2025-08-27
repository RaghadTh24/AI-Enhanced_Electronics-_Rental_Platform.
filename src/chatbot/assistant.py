import uuid
import requests
import json

OPENROUTER_API_KEY = "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"
# قالب التعليمات للنموذج
system_prompt = """
You are an assistant bot for RENTTECH, an electronic device rental platform.

Please reply in the same language as the user, whether Arabic or English.
Be short and professional.

Platform features:
- Create account, login, edit profile
- Rent devices by browsing, selecting duration, and paying
- Rate and review devices
- Receive alerts when a device becomes available
"""

class Conversation:
    def __init__(self):
        self.messages = [{"role": "system", "content": system_prompt}]
        self.active = True

conversations = {}

def get_or_create_conversation(conversation_id: str):
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation()
    return conversations[conversation_id]

def query_openrouter_api(conversation: Conversation) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "meta-llama/llama-4-maverick:free",
            "messages": conversation.messages
        }

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data, ensure_ascii=False)
        )

        response_data = response.json()

        if response.status_code == 200:
            return response_data['choices'][0]['message']['content']
        else:
            return f"Error: {response_data.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"API Error: {str(e)}"

def handle_conversation(user_message, conversation_id=None):
    conversation = get_or_create_conversation(conversation_id or str(uuid.uuid4()))
    conversation.messages.append({"role": "user", "content": user_message})
    reply = query_openrouter_api(conversation)
    conversation.messages.append({"role": "assistant", "content": reply})
    return reply