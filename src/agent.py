from typing import List, Dict
from .memory import ConversationMemory
from .config import OPENAI_API_KEY
import openai

class SupportAgent:
    def __init__(self, memory: ConversationMemory):
        self.memory = memory
        self.use_llm = bool(OPENAI_API_KEY)
        if self.use_llm:
            openai.api_key = OPENAI_API_KEY

    def rule_based_reply(self, user_text: str) -> str:
        t = user_text.lower().strip()
        if not t:
            return "I’m here. What’s on your mind right now?"
        if any(k in t for k in ["anxious", "anxiety", "overwhelmed", "stress", "stressed"]):
            return "Thanks for sharing that. Let’s take a slow breath. What feels most heavy—workload, expectations, or uncertainty?"
        if any(k in t for k in ["sad", "down", "lonely", "low"]):
            return "I hear you. You don’t have to carry this alone. Would it help to name one gentle action for today?"
        if any(k in t for k in ["angry", "frustrated", "irritated"]):
            return "That’s valid. Frustration often points to something you care about. Do you want to vent or pick one next step?"
        if any(k in t for k in ["focus", "stuck", "procrastinate", "scattered", "unproductive"]):
            return "Let’s shrink it. What’s the 10-minute version of the task? We’ll start there and celebrate the micro-win."
        return "Thanks for telling me. If you can, describe what you’re feeling in one sentence. We’ll find a small next step."

    def llm_reply(self, user_text: str) -> str:
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": (
                "You are a supportive, non-clinical AI companion. "
                "Be concise, compassionate, and avoid medical advice. "
                "Help the user name feelings and choose small, safe next steps."
            )}
        ] + self.memory.as_chat_messages() + [{"role": "user", "content": user_text}]

        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=180
        )
        return resp.choices[0].message["content"]

    def respond(self, user_text: str) -> str:
        self.memory.add("user", user_text)
        reply = self.llm_reply(user_text) if self.use_llm else self.rule_based_reply(user_text)
        self.memory.add("assistant", reply)
        return reply