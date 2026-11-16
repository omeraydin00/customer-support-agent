# agent/nodes/summary_generator.py
# -*- coding: utf-8 -*-

from llm_connection.llm_client import LLMClient


class SummaryGenerator:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    def summarize(self, question: str, answer: str) -> str:
        prompt = (
            "Bir müşteri mesajı ve ona verilen yanıt aşağıda. Destek ekibi için TÜRKÇE tek cümlelik bir özet yaz: "
            "müşteri ne istedi, ne cevap verildi. Yalnızca özeti yaz.\n\n"
            f"Mesaj: {question}\n\nYanıt: {answer}\n\nÖzet:"
        )
        return self.llm.generate(prompt, temperature=0.2).strip('"')
