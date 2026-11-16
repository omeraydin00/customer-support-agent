# agent/nodes/classify_question.py
# -*- coding: utf-8 -*-

from llm_connection.llm_client import LLMClient

CATEGORIES = ["İade", "Teknik destek", "Ürün bilgisi", "Kargo ve teslimat", "Şikayet", "Teşekkür", "Diğer"]


class QuestionClassifier:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    def classify(self, question: str) -> str:
        prompt = (
            "Sen bir müşteri destek temsilcisisin.\n"
            "Kullanıcının mesajını şu kategorilerden birine sınıflandır: " + ", ".join(CATEGORIES) + ".\n"
            "Gecikmiş ya da gelmeyen sipariş 'Kargo ve teslimat'tır; yalnızca teşekkür eden mesaj 'Teşekkür'dür.\n\n"
            f"Mesaj: {question}"
        )
        return self.llm.choose(prompt, CATEGORIES)
