<div align="center">

# Customer Support Agent

**A local LLM pipeline that reads a customer message, understands it and answers it.**

Every message is classified, its intent and sentiment are detected, it gets a priority score, and it is answered from a knowledge base or by Llama 3. All running locally.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Llama%203-000000?style=flat-square&logo=ollama&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

</div>

---

## Why

Support teams spend a large part of their day on simple, repetitive questions and on deciding which messages need attention first. This agent triages every incoming message and drafts an answer, so people can focus on the cases that really need them.

## How it works

The agent is built as a chain of small, independent nodes. Each node has one job and talks to Llama 3 through Ollama's local API.

```mermaid
flowchart TD
    U[Customer message] --> C[QuestionClassifier<br/>Return · Tech support · Product info · Complaint]
    U --> I[IntentExtractor<br/>Return · Exchange · Info · Complaint]
    U --> S[SentimentDetector<br/>Angry · Sad · Happy · Neutral]
    U --> P[PriorityScorer<br/>High · Medium · Low]
    U --> K{KnowledgeBaseSearcher<br/>known question?}
    K -- yes --> A[Answer from knowledge base]
    K -- no --> L[LLMClient<br/>Llama 3 answer]
    A --> M[SummaryGenerator<br/>1–2 sentence summary]
    L --> M
    C & I & S & P & M --> G[ConversationLogger<br/>conversation_logs.json]
    G --> UI[Streamlit dashboard]
```

| Node | Responsibility |
|---|---|
| `QuestionClassifier` | Assigns the message to a support category |
| `IntentExtractor` | Determines what the customer wants to do |
| `SentimentDetector` | Detects the emotional tone of the message |
| `PriorityScorer` | Scores urgency as high, medium or low |
| `KnowledgeBaseSearcher` | Returns a ready answer for frequently asked questions |
| `LLMClient` | Generates a polite Turkish answer when the knowledge base has none |
| `SummaryGenerator` | Summarizes the answer in one or two sentences |
| `ConversationLogger` | Appends every result to `conversation_logs.json` |

## Screenshots

| | |
|---|---|
| <img src="screenshots/1.png" alt="Screenshot 1" /> | <img src="screenshots/2.png" alt="Screenshot 2" /> |
| <img src="screenshots/3.png" alt="Screenshot 3" /> | <img src="screenshots/4.png" alt="Screenshot 4" /> |
| <img src="screenshots/5.png" alt="Screenshot 5" /> | <img src="screenshots/6.png" alt="Screenshot 6" /> |

## Getting started

**Requirements:** Python 3.10+ and [Ollama](https://ollama.com).

```bash
# 1. Pull the model (Ollama serves it on localhost:11434)
ollama pull llama3

# 2. Clone and install
git clone https://github.com/omeraydin00/customer-support-agent.git
cd customer-support-agent/YapayZeka
pip install streamlit requests

# 3. Run
streamlit run streamlit_app.py
```

The dashboard opens in your browser. Type a customer message and press **CEVAPLA**.

## Project structure

```
YapayZeka/
├── streamlit_app.py          # Dashboard and pipeline wiring
├── llm_connection/
│   └── llm_client.py         # Ollama client for answer generation
├── agent/nodes/
│   ├── classify_question.py
│   ├── extract_intent.py
│   ├── detect_sentiment.py
│   ├── priority_scoring.py
│   ├── knowledge_base_search.py
│   ├── summary_generator.py
│   └── logger.py
└── conversation_logs.json    # Saved conversations
```

---

<div align="center">
Built by <a href="https://github.com/omeraydin00">Ömer Faruk Aydın</a>
</div>
