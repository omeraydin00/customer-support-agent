# streamlit_app.py
# -*- coding: utf-8 -*-

import html
from concurrent.futures import ThreadPoolExecutor

import streamlit as st

from llm_connection.llm_client import LLMClient
from agent.nodes.classify_question import QuestionClassifier
from agent.nodes.extract_intent import IntentExtractor
from agent.nodes.detect_sentiment import SentimentDetector
from agent.nodes.priority_scoring import PriorityScorer
from agent.nodes.logger import ConversationLogger
from agent.nodes.knowledge_base_search import KnowledgeBaseSearcher
from agent.nodes.summary_generator import SummaryGenerator

st.set_page_config(page_title="Customer Support Agent", page_icon="💬", layout="wide")

# LLM ve düğümleri başlat
llm_client = LLMClient()
classifier = QuestionClassifier(llm_client)
intent_extractor = IntentExtractor(llm_client)
sentiment_detector = SentimentDetector(llm_client)
priority_scorer = PriorityScorer(llm_client)
logger = ConversationLogger()
knowledge_searcher = KnowledgeBaseSearcher()
summary_generator = SummaryGenerator(llm_client)

EXAMPLES = [
    "Siparişim 10 gündür gelmedi, çok sinirliyim!",
    "Ürünümü nasıl iade edebilirim?",
    "Kulaklığın sol tarafı ses vermiyor.",
    "Ürünü çok beğendim, teşekkür ederim!",
]

PRIORITY_COLOR = {"Yüksek": "red", "Orta": "orange", "Düşük": "green"}
SENTIMENT_COLOR = {"Öfkeli": "red", "Üzgün": "violet", "Endişeli": "orange", "Mutlu": "green", "Nötr": "gray"}

st.markdown(
    """
    <style>
    .block-container { max-width: 1180px; padding-top: 2.2rem; }
    h1 { font-size: 2rem !important; letter-spacing: -0.5px; }
    .answer { padding: 18px 20px; border-radius: 12px; background: rgba(240, 90, 140, 0.07);
              border: 1px solid rgba(240, 90, 140, 0.25); font-size: 1.02rem; line-height: 1.6; }
    .label { color: #6b6f80; font-size: 0.85rem; margin-bottom: 2px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def analyse(message):
    # The four labels don't depend on each other, so they are asked at the same time
    with ThreadPoolExecutor(max_workers=4) as pool:
        category = pool.submit(classifier.classify, message)
        intent = pool.submit(intent_extractor.extract, message)
        sentiment = pool.submit(sentiment_detector.detect, message)
        priority = pool.submit(priority_scorer.score, message)
        labels = {
            "category": category.result(),
            "intent": intent.result(),
            "sentiment": sentiment.result(),
            "priority": priority.result(),
        }

    kb_answer = knowledge_searcher.search(message)
    if kb_answer:
        response, source = kb_answer, "Bilgi bankası"
    else:
        response, source = llm_client.generate_response(message, labels), "Model"
    summary = summary_generator.summarize(message, response)
    return logger.log(user_input=message, response=response, summary=summary, source=source, **labels)


def badge(label, value, color):
    st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f":{color}-badge[{value}]")


st.title("Customer Support Agent")
st.caption("Müşteri mesajını sınıflandırır, aciliyetini belirler ve yanıt taslağını hazırlar. Llama 3, bu bilgisayarda.")

tab_new, tab_log = st.tabs(["Yeni mesaj", "Geçmiş"])

with tab_new:
    left, right = st.columns([5, 7], gap="large")

    with left:
        with st.form("mesaj"):
            message = st.text_area("Müşteri mesajı", key="message", height=130, placeholder="Mesajı buraya yapıştırın")
            sent = st.form_submit_button("Yanıtla", type="primary", use_container_width=True)
        st.markdown('<div class="label">Örnekler</div>', unsafe_allow_html=True)
        for example in EXAMPLES:
            if st.button(example, use_container_width=True):
                st.session_state.pending = example
                st.rerun()

    pending = st.session_state.pop("pending", None)
    if pending:
        message, sent = pending, True

    with right:
        if sent and message.strip():
            with st.spinner("Mesaj inceleniyor, yanıt hazırlanıyor..."):
                try:
                    st.session_state.result = analyse(message.strip())
                except Exception as error:
                    st.session_state.result = None
                    st.error(f"Ollama'ya ulaşılamadı: {error}")

        result = st.session_state.get("result")
        if result:
            st.markdown('<div class="label">Mesaj</div>', unsafe_allow_html=True)
            st.markdown(f"> {result['user_input']}")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                badge("Kategori", result["category"], "blue")
            with c2:
                badge("Amaç", result["intent"], "blue")
            with c3:
                badge("Duygu", result["sentiment"], SENTIMENT_COLOR.get(result["sentiment"], "gray"))
            with c4:
                badge("Öncelik", result["priority"], PRIORITY_COLOR.get(result["priority"], "gray"))

            st.markdown(f'<div class="label">Yanıt taslağı ({result["source"].lower()})</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer">{html.escape(result["response"])}</div>', unsafe_allow_html=True)
            st.markdown("")
            st.markdown('<div class="label">Ekip için özet</div>', unsafe_allow_html=True)
            st.markdown(result["summary"])
        else:
            st.info("Soldan bir mesaj yazın ya da bir örnek seçin.")

with tab_log:
    logs = list(reversed(logger.read()))
    if not logs:
        st.info("Henüz kayıt yok.")
    else:
        urgent = sum(1 for log in logs if log.get("priority") == "Yüksek")
        m1, m2, m3 = st.columns(3)
        m1.metric("Mesaj", len(logs))
        m2.metric("Yüksek öncelikli", urgent)
        m3.metric("Bilgi bankasından", sum(1 for log in logs if log.get("source") == "Bilgi bankası"))
        st.dataframe(
            [
                {
                    "Zaman": log["timestamp"].replace("T", " "),
                    "Mesaj": log["user_input"],
                    "Kategori": log["category"],
                    "Duygu": log["sentiment"],
                    "Öncelik": log["priority"],
                    "Özet": log.get("summary", ""),
                }
                for log in logs
            ],
            use_container_width=True,
            hide_index=True,
        )
