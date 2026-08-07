# My AI Stack — Jiya Yadav
> MSc. IT Student | AI Intern @ FlyRank | Week 6 Capstone

---

## 🧠 LLMs I've Used & What I Think

| Model | Provider | Best For | My Rating |
|-------|----------|----------|-----------|
| Claude 3.5 Sonnet | Anthropic | Long reasoning, safe outputs | ⭐⭐⭐⭐⭐ |
| GPT-4o | OpenAI | Coding, structured output | ⭐⭐⭐⭐⭐ |
| Gemini 1.5 Pro | Google | Multimodal, long context | ⭐⭐⭐⭐ |
| LLM Arena | LMSYS | Blind model comparison | ⭐⭐⭐⭐ |

---

## 🏗️ My Build Stack (This Project)

### Agent Layer
- **LLM:** GPT-4o via OpenAI API
- **Language:** Python 3.11
- **Framework:** Chainlit (chat UI) + OpenAI SDK
- **Memory:** Conversation history (in-session)
- **Knowledge Base:** Custom markdown → injected as context

### Interface Layer
- **Chat UI:** Chainlit (local + deployable)
- **Website:** HTML/CSS (deployed on GitHub Pages)

### Deploy Layer
- **Agent:** Chainlit Cloud / Railway
- **Website:** GitHub Pages

---

## 🔑 Key Concepts I Understand

### Prompt Engineering
- System prompts define agent persona
- Few-shot examples improve consistency
- Temperature controls creativity vs precision

### RAG (Retrieval Augmented Generation)
- Ground LLM in your own data
- Prevents hallucination in medical context ← critical for postpartum

### AI Safety in Healthcare
- Always include "consult a doctor" disclaimers
- Never diagnose — only inform and support
- Empathetic tone is non-negotiable

---

## 💡 What I Built
A postpartum health support chatbot that acts as a knowledgeable,
empathetic companion for new mothers — built with Python + OpenAI API,
deployed on the web.