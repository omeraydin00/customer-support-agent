# agent/nodes/priority_scoring.py

from llm_connection.llm_client import LLMClient

LEVELS = ["Yüksek", "Orta", "Düşük"]


class PriorityScorer:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    def score(self, message: str) -> str:
        prompt = (
            "Sen bir müşteri destek temsilcisisin. "
            "Kullanıcının mesajının aciliyetini değerlendir: Yüksek, Orta ya da Düşük.\n"
            "Gecikmiş, yanlış ya da hasarlı sipariş ve öfkeli müşteri Yüksek; soru sormak Orta; "
            "teşekkür ve olumlu geri bildirim Düşüktür.\n\n"
            f"Mesaj: {message}"
        )
        return self.llm.choose(prompt, LEVELS)
