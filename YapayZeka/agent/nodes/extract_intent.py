# agent/nodes/extract_intent.py

from llm_connection.llm_client import LLMClient

INTENTS = ["İade", "Değişim", "Bilgi", "Sipariş takibi", "Şikayet", "Geri bildirim", "Diğer"]


class IntentExtractor:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    def extract(self, question: str) -> str:
        prompt = (
            "Sen bir müşteri destek temsilcisisin. "
            "Kullanıcının mesajına bakarak ne istediğini belirle: " + ", ".join(INTENTS) + ".\n"
            "Ürünü öven ya da teşekkür eden mesaj 'Geri bildirim'dir.\n\n"
            f"Mesaj: {question}"
        )
        return self.llm.choose(prompt, INTENTS)
