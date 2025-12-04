from typing import List, Dict

class ConversationMemory:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.turns: List[Dict[str, str]] = []

    def add(self, role: str, content: str):
        self.turns.append({"role": role, "content": content})
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]

    def as_chat_messages(self):
        return [{"role": t["role"], "content": t["content"]} for t in self.turns]

    def transcript_text(self):
        lines = []
        for t in self.turns:
            prefix = "You" if t["role"] == "user" else "Companion"
            lines.append(f"{prefix}: {t['content']}")
        return "\n".join(lines)