# Postpartum AI Companion 💛
FlyRank AI Internship · Week 6 Capstone · General AI Fluency (FL)
<p align="center">

A warm, empathetic 24/7 AI health companion supporting new mothers through postpartum recovery—physically, mentally, and emotionally.

<br>

Built by Jiya Yadav
12-Hour Capstone

</p>
✨ Overview
The Postpartum AI Companion is an AI-powered chatbot designed to provide compassionate, evidence-informed support for mothers during the postpartum period.

It focuses on:

💛 Emotional support
🧠 Mental health awareness
👶 Newborn care guidance
🤱 Breastfeeding support
🚨 Safe crisis escalation

The assistant never replaces professional healthcare and always prioritizes user safety.

# Live Links 🔗
Resource	Link

🌐 Portfolio Website	https://jiya-ydv.github.io/flyrank-internship-tracker/

🤖 Live Chatbot	https://huggingface.co/spaces/YDVJIYA/postpartum_AI_companion

📁 Source Code	https://github.com/JIYA-YDV/flyrank-internship-tracker

📘 AI Stack Documentation	ai-stack.md


# Capstone Requirements ✅

Master the AI stack	ai-stack.md documenting 5+ LLMs	✅

Personal portfolio website	GitHub Pages deployment	✅

Working AI Agent	Hugging Face deployment	✅

# AI Companion 🤖
Purpose
New mothers are often underserved after childbirth.
At 3 AM, when the baby won't sleep and anxiety feels overwhelming, this companion offers calm, empathetic guidance while encouraging appropriate medical care when needed.

It is:
Always available
Anonymous
Safety-first
Non-judgmental

# Features

💛 Empathetic Conversations	Validates emotions before providing information

🧠 Context Memory	Maintains conversation context

🚨 Crisis Detection	Detects severe distress and recommends professional help

⚡ Streaming Responses	Token-by-token generation for natural conversation

🌙 Available 24/7	Free with no signup required

# Knowledge Areas
Postpartum recovery,
C-section recovery,
Vaginal recovery,
Pelvic floor recovery,
Baby blues,
Postpartum depression (PPD),
Postpartum anxiety (PPA),
Postpartum psychosis (PPP),
Breastfeeding,
Mastitis,
Latching,
Milk supply,
Safe newborn care,
Partner & family support,

# Safety Principles 🛡️

The assistant always follows these rules.

❌ Never diagnoses medical conditions

❌ Never recommends stopping prescribed medication

✅ Always encourages professional medical consultation

🚨 Immediately recommends crisis resources when self-harm is detected

Every medical conversation ends with:
"Please consult your doctor to confirm what's right for you."

# System Architecture 🏗️

 ```
User
  │
  ▼
Portfolio Website (GitHub Pages)
  │
  ▼
Embedded Gradio Chat Interface
  │
  ▼
Python Backend
  │
  ▼
Safety Prompt Layer
  │
  ▼
Groq API (Llama 3.3 70B)
```

# Technology Stack ⚙️
Layer	Technology	Purpose

LLM	Llama 3.3 70B via Groq	Fast inference with high-quality responses

UI	Gradio 5.x	Chat interface

Backend	Python 3.11	AI application logic

Agent Deployment	Hugging Face Spaces	Public hosting

Website	GitHub Pages	Portfolio hosting

Version Control	Git & GitHub	Source control

# Project Structure 📁
General AI Fluency Impact Project
```
│
├── README.md
├── ai-stack.md
│
├── docs
│   └── capstone-report.pdf
│
├── agent
│   ├── app.py
│   ├── prompts.py
│   ├── requirements.txt
│   └── .env
│
└── website
    ├── index.html
    ├── style.css
    └── agent.html
```
# Running Locally 🚀

Prerequisites

Python 3.11+

Groq API Key

PowerShell, Terminal, or Bash

# Installation
# Clone repository
git clone https://github.com/JIYA-YDV/flyrank-internship-tracker.git

cd "flyrank-internship-tracker/Capstone/General AI Fluency Impact Project/agent"

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux / macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env
GROQ_API_KEY=gsk_your_key_here

# Run
python app.py

Open:
http://localhost:7860

# Example Prompts 🧪 
I had my baby two weeks ago and I'm feeling really sad.

Is it normal to feel overwhelmed with a newborn?

How can I tell if I have postpartum depression?

I'm having trouble breastfeeding. What should I do?

# What I Learned 📚
Technical: 
Rapid API migration (OpenAI → Groq),
Framework evaluation (Chainlit → Gradio),
Hugging Face deployment,
Docker debugging,
Git workflow,
Secret management,
Professional,
Systematic debugging,
Documentation improves thinking,
Human-centered AI design,
Shipping matters more than perfection,

# Future Improvements 🔮

RAG with WHO & ACOG medical guidelines

Regional language support

Voice interaction

Weekly symptom tracking

Partner support mode

Fine-tuned postpartum language model

# Disclaimer ⚠️

This project does not provide medical advice.

The chatbot provides educational information and emotional support only.

Always consult qualified healthcare professionals for medical decisions.

Emergency

Call your local emergency services immediately.

Maternal Mental Health Hotline:
1-833-943-5746

Privacy: 

No conversations are stored.

Sessions are temporary.

No personal information is collected.

# License 📜

This project is released under the MIT License.

# Acknowledgements 🙏
 · FlyRank AI Internship · Groq  · Hugging Face  · Every new mother who inspired this project
<p align="center">

Built with empathy, curiosity, and many Git commits 💛

Jiya Yadav

</p>
