from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from .assistant import handle_conversation  # تأكد من وجود هذا الملف داخل مجلد chatbot

@csrf_exempt
def chatbot_page(request):
    return render(request, 'chatbot/chatbot.html')

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")
        conversation_id = data.get("conversation_id", None)

        if not user_message:
            return JsonResponse({"error": "Empty message"}, status=400)

        reply = handle_conversation(user_message, conversation_id)
        return JsonResponse({"response": reply})

    return JsonResponse({"error": "Invalid request method"}, status=405)
