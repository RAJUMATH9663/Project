from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import google.generativeai as genai
from django.conf import settings

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Be concise, accurate, and friendly. "
    "Ask clarifying questions when needed."
)


def _get_gemini_model():
    if not settings.GEMINI_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY in environment.")
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model_name = "models/gemini-flash-latest"
    try:
        return genai.GenerativeModel(model_name, system_instruction=SYSTEM_PROMPT)
    except TypeError:
        return genai.GenerativeModel(model_name)

# 🔹 Home page (optional, to avoid 404)
def home(request):
    return render(request, "chatbot/chat.html")

# 🔹 Gemini Chat API
@api_view(['POST'])
def chat_api(request):
    try:
        payload = request.data if isinstance(request.data, dict) else {}
        message = payload.get("message") or request.POST.get("message")
        reset = payload.get("reset") is True

        if reset:
            request.session["chat_history"] = []
            if not message:
                return Response({"ok": True})

        if not message:
            return Response({"error": "Message is required"}, status=400)

        history = request.session.get("chat_history", [])
        model = _get_gemini_model()
        chat = model.start_chat(history=history)
        response = chat.send_message(message)

        history = history + [
            {"role": "user", "parts": [message]},
            {"role": "model", "parts": [response.text]},
        ]
        request.session["chat_history"] = history

        return Response({"reply": response.text})
    except Exception as e:
        return Response({"error": str(e)}, status=500)