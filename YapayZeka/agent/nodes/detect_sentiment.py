# agent/nodes/detect_sentiment.py

from llm_connection.llm_client import LLMClient

SENTIMENTS = ["Öfkeli", "Üzgün", "Endişeli", "Mutlu", "Nötr"]


class SentimentDetector:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    def detect(self, question: str) -> str:
        prompt = (
            "Sen bir müşteri temsilcisisin. "
            "Kullanıcının mesajındaki duyguyu belirle: " + ", ".join(SENTIMENTS) + ".\n"
            "Duygu belirtmeyen düz bir soru Nötr'dür.\n\n"
            f"Mesaj: {question}"
        )
        return self.llm.choose(prompt, SENTIMENTS)
