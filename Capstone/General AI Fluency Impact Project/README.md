\# 💛 Postpartum AI Companion

\### FlyRank AI Internship · Week 6 Capstone · General AI Fluency (FL)



> A warm, empathetic 24/7 AI health companion supporting new mothers through postpartum recovery — physically, mentally, and emotionally.



\*\*Built by \[Jiya Yadav](https://github.com/JIYA-YDV)\*\* · MSc. IT Student · 12 hour capstone



\---



\## 🔗 Live Links



| Resource | URL |

|----------|-----|

| 🌐 \*\*Portfolio Website\*\* | \[jiya-ydv.github.io/flyrank-internship-tracker](https://jiya-ydv.github.io/flyrank-internship-tracker/) |

| 🤖 \*\*Live Chatbot\*\* | \[huggingface.co/spaces/YDVJIYA/postpartum\_AI\_companion](https://huggingface.co/spaces/YDVJIYA/postpartum\_AI\_companion) |

| 📁 \*\*Source Code\*\* | \[GitHub Repository](https://github.com/JIYA-YDV/flyrank-internship-tracker) |

| 📘 \*\*AI Stack Doc\*\* | \[ai-stack.md](./ai-stack.md) |



\---



\## ✅ Capstone Requirements Met



| Requirement | Deliverable | Status |

|-------------|-------------|--------|

| Master the AI stack | Comprehensive \[ai-stack.md](./ai-stack.md) with real usage of 5+ LLMs | ✅ |

| Build personal brand website | Live portfolio hub on GitHub Pages | ✅ |

| Ship a personal agent | Deployed postpartum AI chatbot on Hugging Face | ✅ |



\---



\## 🤖 The Agent: What It Does



\### Purpose

New mothers are critically underserved by healthcare systems globally. At 3 AM, when the baby won't sleep and you feel sad for no reason — this agent is there. Non-judgmental. Always available. Safety-conscious.



\### Capabilities

\- 💛 \*\*Empathetic responses\*\* — Validates feelings BEFORE informing

\- 🧠 \*\*Conversation memory\*\* — Remembers context throughout the chat

\- 🚨 \*\*Crisis detection\*\* — Recognizes distress signals + refers to hotlines

\- ⚡ \*\*Streaming responses\*\* — Token-by-token for natural conversation

\- 🌙 \*\*Available 24/7\*\* — Free, anonymous, no signup



\### Knowledge Areas

\- Postpartum physical recovery (C-section, vaginal, pelvic floor)

\- Postpartum mental health (baby blues, PPD, PPA, PPP)

\- Breastfeeding support (latch, supply, mastitis)

\- Newborn care basics (safe sleep, feeding schedules)

\- Partner/family support guidance



\### Safety Rules (Non-Negotiable)

\- \*\*Never diagnoses\*\* — informs and refers only

\- \*\*Never advises stopping medication\*\*

\- \*\*Always ends with:\*\* "Please consult your doctor to confirm what's right for you"

\- \*\*Emergency detection:\*\* Immediate hotline referral for self-harm mentions



\---



\## 🏗️ Tech Stack

┌─────────────────────────────────────┐

│ User → Portfolio Website (GH Pages)│

│ ↓ iframe │

│ Gradio Chat UI (HF Spaces) │

│ ↓ │

│ Python App with Safety Prompts │

│ ↓ │

│ Groq API (Llama 3.3 70B) │

└─────────────────────────────────────┘



text '''

| Layer | Tool | Why |

|-------|------|-----|

| \*\*LLM\*\* | Llama 3.3 70B via Groq | Free, fast (<1s), quality on par with GPT-4 |

| \*\*UI\*\* | Gradio 5.x + custom dark theme | Free HF deployment support |

| \*\*Backend\*\* | Python 3.11 | Standard for AI workflows |

| \*\*Deployment (Agent)\*\* | Hugging Face Spaces (ZeroGPU) | Free public hosting for Gradio apps |

| \*\*Deployment (Site)\*\* | GitHub Pages | Free static site hosting |

| \*\*Version Control\*\* | Git + GitHub | Portfolio + source visible to recruiters |



'''



\## 📁 Project Structure



text '''

General AI Fluency Impact Project/

├── README.md ← You are here

├── ai-stack.md ← AI tools \& concepts documentation

├── docs/

│ └── capstone-report.pdf ← Formal submission document

├── agent/

│ ├── app.py ← Main Gradio chatbot

│ ├── prompts.py ← System prompt (Jiya persona + safety)

│ ├── requirements.txt ← Python dependencies

│ └── .env ← API keys (gitignored)

└── website/

├── index.html ← Project landing page

├── style.css ← Custom pink theme

└── agent.html ← Chatbot embed page



'''


\---



\## 🚀 Run Locally



\### Prerequisites

\- Python 3.11+

\- Free \[Groq API key](https://console.groq.com)

\- Windows PowerShell / Mac Terminal / Linux shell



\### Setup



```bash

\# 1. Clone the repository

git clone https://github.com/JIYA-YDV/flyrank-internship-tracker.git

cd "flyrank-internship-tracker/Capstone/General AI Fluency Impact Project/agent"



\# 2. Create virtual environment

python -m venv venv



\# Windows PowerShell

.\\venv\\Scripts\\Activate.ps1



\# Mac/Linux

source venv/bin/activate



\# 3. Install dependencies

pip install -r requirements.txt



\# 4. Add your Groq API key

\# Create a file named .env with:

GROQ\_API\_KEY=gsk\_your\_key\_here



\# 5. Run the app

python app.py



\# 6. Open in browser

\# http://localhost:7860





🧪 Try These Prompts



"I had my baby 2 weeks ago and I'm feeling really sad and I don't know why"



"Is it normal to feel overwhelmed with a newborn?"



"How can I tell if I have postpartum depression?"



"I'm having trouble breastfeeding — what should I do?"





🎓 What This Project Taught Me

Technical Skills

Rapid API migration — Pivoted from OpenAI to Groq in under an hour when credits ran out

Framework selection — Tried Chainlit, switched to Gradio for deployability

Deployment engineering — Wrestled with Docker, ZeroGPU, and encoding bugs

Version control discipline — 15+ conventional commits telling the real story

Security-first mindset — .gitignore, secrets management, key rotation practices

Soft Skills

Debugging patience — Some errors took hours; systematic elimination works

Documentation as thinking — Writing forces clarity

Design + engineering — Empathetic AI needs both technical skill and human intuition

Shipping > perfection — A deployed 80% > a perfect 0%

🔮 Roadmap (v2 Ideas)

&#x20;RAG with vetted medical knowledge base (WHO, ACOG guidelines)

&#x20;Multi-language support (Hindi first)

&#x20;Voice input/output for hands-free use while breastfeeding

&#x20;Symptom-tracking mode with weekly summaries

&#x20;Partner mode with tips for supporting new mothers

&#x20;Fine-tuned model on postpartum-specific data

⚠️ Important Disclaimers

This is NOT medical advice.



The agent provides information and emotional support only

Always consult your doctor, midwife, or pediatrician for medical decisions

For emergencies, call 911 immediately

Maternal Mental Health Hotline: 1-833-943-5746

Privacy:



No conversations are stored server-side

Each session starts fresh

No personal data is collected

📜 License

MIT License — free to fork, adapt, and improve.



🙏 Acknowledgments

FlyRank AI Internship for the capstone framework

Groq for free, fast LLM inference

Hugging Face for free deployment infrastructure

New mothers everywhere — this is for you 💛

Built with intention, empathy, and a lot of git commits by Jiya Yadav 🌸

