# Customer Support Agent

Reads a customer message, works out what it is about and drafts a reply, all on a local model.

Python · Ollama (Llama 3) · Streamlit

<img alt="Customer Support Agent" src="screenshots/3.png" />

Each message goes through a few small steps, every one of them a separate module that talks to Llama 3 through Ollama's local API: it is put in a category (return, technical support, product information, complaint), its intent and tone are detected, and it gets a priority. Common questions are answered from a small knowledge base; everything else is answered by the model, then summarised in a sentence or two. Every conversation is saved to `conversation_logs.json`.

<p>
  <img width="49%" alt="Waiting for the answer" src="screenshots/2.png" />
  <img width="49%" alt="Answer and summary" src="screenshots/5.png" />
</p>

## Running it

You need Python 3.10 or newer and [Ollama](https://ollama.com).

```bash
ollama pull llama3

git clone https://github.com/omeraydin00/customer-support-agent.git
cd customer-support-agent/YapayZeka
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Type a message in the page that opens and press **Cevapla**.

## Structure

```
YapayZeka/
├── streamlit_app.py        the page and the order of the steps
├── llm_connection/         the Ollama client
├── agent/nodes/            classification, intent, tone, priority,
│                           knowledge base, summary and logging
└── conversation_logs.json
```
