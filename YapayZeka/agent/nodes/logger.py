# agent/nodes/logger.py

import json
import os
from datetime import datetime


class ConversationLogger:
    def __init__(self, log_file='conversation_logs.json'):
        self.log_file = log_file
        # Eğer dosya yoksa boş bir liste oluştur
        if not os.path.exists(self.log_file):
            self._write([])

    def _write(self, logs):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

    def read(self):
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    def log(self, user_input, category, intent, sentiment, priority, response, summary="", source=""):
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "user_input": user_input,
            "category": category,
            "intent": intent,
            "sentiment": sentiment,
            "priority": priority,
            "response": response,
            "summary": summary,
            "source": source,
        }

        # Eski kayıtları oku, yeni kaydı ekle, yaz
        logs = self.read()
        logs.append(entry)
        self._write(logs)
        return entry
