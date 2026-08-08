import gradio as gr
from groq import Groq
from prompts import SYSTEM_PROMPT
import os
from dotenv import load_dotenv

# Load env (works locally + HF secrets on cloud)
load_dotenv()

# Init Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1000
TEMPERATURE = 0.7


def respond(message, history):
    """
    Handle chat messages with conversation memory.
    `history` is provided by Gradio in OpenAI message format.
    """
    # Build message list: system prompt + conversation history + new message
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add previous conversation
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Add current user message
    messages.append({"role": "user", "content": message})

    # Stream response from Groq
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        stream=True
    )

    # Yield tokens as they arrive (streaming effect)
    partial_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            partial_response += delta
            yield partial_response


# Build the Chat interface (Gradio 6.x compatible)
demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    title="?? Jiya — Postpartum AI Companion",
    description=(
        "A warm, empathetic AI health companion supporting new mothers through postpartum recovery. "
        "**Always consult your doctor for medical advice.** "
        "In emergencies call 911. Maternal Mental Health Hotline: 1-833-943-5746."
    ),
    examples=[
        "I had my baby 2 weeks ago and I'm feeling really sad and I don't know why",
        "Is it normal to feel overwhelmed with a newborn?",
        "How can I tell if I have postpartum depression?",
        "I'm having trouble breastfeeding — what should I do?",
    ],
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)