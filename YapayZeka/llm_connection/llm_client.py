# llm_connection/llm_client.py

import json
import os

import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("SUPPORT_MODEL", "llama3")


class LLMClient:
    def __init__(self, model: str = MODEL):
        self.base_url = f"{OLLAMA_URL}/api/generate"
        self.model = model

    def generate(self, prompt: str, temperature: float, schema: dict | None = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if schema:
            payload["format"] = schema
        response = requests.post(self.base_url, json=payload, timeout=180)
        response.raise_for_status()
        return response.json()["response"].strip()

    def choose(self, prompt: str, labels: list[str]) -> str:
        # Ollama's structured output keeps the answer to one of the labels,
        # instead of "1) iade" or a label followed by an English explanation
        schema = {
            "type": "object",
            "properties": {"label": {"type": "string", "enum": labels}},
            "required": ["label"],
        }
        raw = self.generate(prompt, temperature=0, schema=schema)
        try:
            label = json.loads(raw)["label"]
        except (json.JSONDecodeError, KeyError):
            label = raw
        return label if label in labels else labels[-1]

    def generate_response(self, prompt: str, context: dict | None = None) -> str:
        system_prompt = (
            "Sen kibar ve yardımsever bir müşteri destek temsilcisisin. Kullanıcıya TÜRKÇE cevap ver. "
            "En fazla dört cümle yaz. Söz veremeyeceğin bir şeyi (iade onayı, kargo tarihi) vaat etme; "
            "gerekiyorsa sipariş numarasını iste."
        )
        if context:
            system_prompt += (
                f" Mesajın kategorisi: {context['category']}, duygusu: {context['sentiment']}, "
                f"önceliği: {context['priority']}. Tonunu buna göre ayarla."
            )
        full_prompt = f"{system_prompt}\n\nKullanıcının mesajı: {prompt}\n\nYanıt:"
        return self.generate(full_prompt, temperature=0.4).strip('"')
