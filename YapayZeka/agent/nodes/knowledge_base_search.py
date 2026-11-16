# agent/nodes/knowledge_base_search.py

import re

# Basit bilgi bankası verileri (örnek veriler): anahtar kelimeler ve hazır cevap
KNOWLEDGE_BASE = [
    ({"kargo", "teslimat", "gelir", "ulaşır"}, "Kargolar genellikle 2-5 iş günü içerisinde teslim edilir."),
    ({"iade"}, "İade etmek için ürünü teslim aldıktan sonra 14 gün içinde müşteri hizmetlerimize başvurabilirsiniz."),
    ({"garanti"}, "Tüm ürünlerimizde 2 yıl garanti süresi bulunmaktadır."),
    ({"ödeme", "taksit", "kart"}, "Kredi kartı, banka kartı ve kapıda ödeme seçeneklerimiz vardır."),
    ({"iptal"}, "Siparişinizi kargoya verilmeden önce iptal edebilirsiniz, lütfen destek ekibimizle iletişime geçin."),
]

QUESTION_WORDS = {"nasıl", "ne", "nedir", "nelerdir", "kaç", "mı", "mi", "mu", "mü", "zaman", "kadar"}


class KnowledgeBaseSearcher:
    def search(self, question: str) -> str:
        # Only plain questions are answered from here; "kargom 10 gündür gelmedi" is a complaint
        # about one order and needs a real reply, not the usual delivery times
        words = set(re.findall(r"\w+", question.lower()))
        if not words & QUESTION_WORDS:
            return ""
        for keywords, answer in KNOWLEDGE_BASE:
            if any(word.startswith(k) for word in words for k in keywords):
                return answer
        return ""  # Eğer bulunamazsa boş string döner
