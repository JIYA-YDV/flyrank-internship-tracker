# 🧠 My AI Stack — Jiya Yadav
> MSc. IT Student · AI Intern @ FlyRank · Week 6 Capstone (General AI Fluency Impact Project)

This document captures my hands-on understanding of the modern AI stack — the tools I've explored, the ones I chose for this project, and the lessons I learned when reality forced me to pivot.

---

## 🎯 Overview

I built a **Postpartum AI Companion** — an empathetic health assistant for new mothers, deployed live on the internet. This capstone gave me hands-on experience across the entire AI development lifecycle: model selection, prompt engineering, UI frameworks, deployment, and safety design.

---

## 🤖 LLMs I've Explored

Throughout my internship, I experimented with several frontier language models to understand their strengths and trade-offs.

| Model | Provider | Best For | My Rating | Notes |
|-------|----------|----------|-----------|-------|
| **Claude 3.5 Sonnet** | Anthropic | Long reasoning, safe outputs, tone control | ⭐⭐⭐⭐⭐ | Most helpful for empathetic writing — used to draft system prompts |
| **GPT-4o** | OpenAI | Coding, structured output, function calling | ⭐⭐⭐⭐⭐ | Great for boilerplate + debugging |
| **Gemini 1.5 Pro** | Google | Multimodal input, huge context window | ⭐⭐⭐⭐ | Useful for document-heavy tasks |
| **Llama 3.3 70B** | Meta (via Groq) | Fast inference, open-weight, FREE | ⭐⭐⭐⭐⭐ | What I actually shipped with — blazing fast |
| **LLM Arena** | LMSYS | Blind model comparison | ⭐⭐⭐⭐ | Great for evaluating models without bias |

### Key Takeaway
There's no "best" LLM — only the best fit for your **constraints** (cost, latency, safety, deployment). I originally planned GPT-4o but pivoted to Llama 3.3 via Groq because it's free, fast, and quality is nearly identical for my use case.

---

## 🏗️ My Actual Build Stack (Shipped)

### 🧩 Agent Layer
- **LLM:** Llama 3.3 70B (via Groq API — free, sub-second responses)
- **Language:** Python 3.11
- **AI SDK:** `groq` Python client
- **Memory:** In-session conversation history (OpenAI message format)
- **Streaming:** Token-by-token response streaming for natural feel

### 🎨 Interface Layer
- **Chat UI:** Gradio 5.x with custom dark theme
- **Portfolio Website:** HTML + CSS (custom-built, no framework)
- **Design System:** Pink/purple gradient brand palette
- **Fonts:** Inter (Google Fonts)

### 🚀 Deploy Layer
- **Agent:** Hugging Face Spaces (ZeroGPU — free tier)
- **Website:** GitHub Pages (static hosting)
- **Version Control:** Git + GitHub (conventional commits)
- **Secrets:** `.env` locally, HF Space secrets in production

### 🛡️ Safety Layer
- Medical disclaimers on every response
- Never-diagnose policy in system prompt
- Crisis referral protocols (911 + Maternal Mental Health Hotline)
- Empathy-first response structure

---

## 🔄 What I Actually Built vs. What I Planned

This capstone taught me that **real projects never go as planned** — and that pivoting quickly is a core AI engineering skill.

| Original Plan | What I Actually Used | Why I Switched |
|---------------|---------------------|----------------|
| OpenAI GPT-4o | Groq Llama 3.3 70B | OpenAI credits exhausted mid-build → learned to migrate APIs in minutes |
| Chainlit UI | Gradio | Chainlit's free tier didn't support easy public deployment |
| Docker on HF Spaces | Gradio SDK on ZeroGPU | Docker requires paid HF plan; ZeroGPU is free |
| Single repo per project | Portfolio hub with sub-pages | Cleaner for multiple future capstones |

**Each pivot taught me something.** Nothing was wasted — the debugging IS the learning.

---

## 🔑 Core AI Concepts I Now Understand

### Prompt Engineering
- **System prompts** shape the agent's persona, safety rules, and tone
- **Temperature (0.7)** balances warmth with consistency
- **Max tokens (1000)** keeps responses focused, not overwhelming
- **Message role structure** (system → user → assistant) enables conversation memory

### Streaming Responses
- Instead of waiting for the full response, tokens are yielded as they arrive
- Creates a natural, conversational feel
- Critical for user retention on longer replies

### AI Safety in Healthcare
- **Never diagnose** — only inform and refer
- **Validate emotions first**, then provide information
- **Screen for crisis signals** and refer to hotlines immediately
- **Always disclaim** — recommend professional consultation

### Retrieval-Augmented Generation (RAG) — Learned but Not Used Here
- Grounds LLM in your own data (documents, knowledge base)
- Reduces hallucination — critical in medical contexts
- Planned for v2 with vector DB (Pinecone or Supabase pgvector)

### Cost & Latency Awareness
- API rate limits and credits are real constraints
- Free tiers (Groq, HF Spaces) enable rapid prototyping
- Streaming perceived latency < actual latency

---

## 💡 What I Built

### Postpartum AI Companion
A warm, empathetic 24/7 AI health companion supporting new mothers through postpartum recovery — physically, mentally, and emotionally.

**Why this problem?**
New mothers are critically underserved by healthcare systems globally. At 3 AM, when no one is awake and you feel sad for no reason — this agent is there. Non-judgmental. Always available. Safety-conscious.

**Where you can try it:**
- 🌐 **Portfolio:** https://jiya-ydv.github.io/flyrank-internship-tracker/
- 🤖 **Live Agent:** https://huggingface.co/spaces/YDVJIYA/postpartum_AI_companion

---

## 🎓 Lessons From This Capstone

1. **Pivoting is a skill.** Every "failure" (rate limits, encoding bugs, deployment errors) taught me something the tutorial never would.
2. **Free tiers force creativity.** Constraints made me a better engineer.
3. **Security first, always.** Never commit API keys. `.gitignore` isn't optional.
4. **File encoding matters.** UTF-8 vs Windows-1252 broke my deployment for hours.
5. **Git history tells your story.** 15+ meaningful commits show how I think — not just what I built.
6. **Empathy in AI is design work.** The system prompt was harder to write than the code.
7. **Deployment is the real test.** Working locally ≠ shipped. Getting it live on the internet was the hardest and most rewarding part.

---

## 🛠️ Tools I Used Daily During This Capstone

| Category | Tool | Purpose |
|----------|------|---------|
| **AI Development** | Claude (Anthropic) | Pair programming, prompt writing, debugging |
| **Code Editor** | VS Code | Local dev environment |
| **Terminal** | Windows PowerShell | Running commands, git, Python |
| **Version Control** | Git + GitHub | Source control, portfolio hosting |
| **AI Deployment** | Hugging Face Spaces | Chatbot hosting (free tier) |
| **API Provider** | Groq Console | LLM inference (free tier) |
| **Design** | Custom CSS | Portfolio + chatbot styling |

---

## 🚀 What's Next

- Add **RAG** with a vetted medical knowledge base
- Multi-language support (Hindi first — my mother tongue)
- Voice input/output for accessibility during breastfeeding
- Anonymous usage analytics to improve prompts
- Explore fine-tuning on postpartum-specific data

---

## 📝 Final Reflection

Six weeks ago, "AI" felt like magic. Now it feels like **engineering with constraints, ethics, and empathy**. I understand the stack — not just as tools, but as trade-offs. I've shipped something real that could help real people. That feels good.

**— Jiya Yadav**
*MSc. IT Student · AI Intern @ FlyRank · 2026*