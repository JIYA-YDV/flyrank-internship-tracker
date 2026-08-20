import gradio as gr
from groq import Groq
from prompts import SYSTEM_PROMPT
import os
from dotenv import load_dotenv
import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    # Your logic here
    response_message = f"You said: {message.content}"
    await cl.Message(content=response_message).send()
    
# Optional import for HF Spaces GPU decorator
try:
    import spaces
    HAS_SPACES = True
except ImportError:
    HAS_SPACES = False
    # Create a dummy decorator for local use
    class spaces:
        @staticmethod
        def GPU(func):
            return func

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "groq/compound-mini"
MAX_TOKENS = 1000
TEMPERATURE = 0.7


@spaces.GPU
def respond(message, history):
    """Handle chat messages with conversation memory."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for item in history:
        if isinstance(item, dict):
            messages.append({"role": item["role"], "content": item["content"]})
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, bot_msg = item
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        stream=True
    )

    partial_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            partial_response += delta
            yield partial_response


custom_theme = gr.themes.Base(
    primary_hue="pink",
    secondary_hue="pink",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
)

# CLEAN dark theme with pink accents - no overlays
custom_css = """
.gradio-container, body {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%) !important;
    color: #f8fafc !important;
    max-width: 1000px !important;
    margin: 0 auto !important;
    padding: 20px !important;
    font-family: 'Inter', sans-serif !important;
}

/* Header */
.header-card {
    background: rgba(26, 26, 46, 0.6);
    border: 1px solid rgba(244, 114, 182, 0.2);
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 30px rgba(244, 114, 182, 0.08);
}
.header-card h1 {
    font-size: 30px;
    margin: 12px 0 8px;
    font-weight: 700;
    background: linear-gradient(135deg, #f472b6 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.header-card p {
    color: #94a3b8;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
}
.disclaimer-box {
    background: rgba(146, 64, 14, 0.12);
    border-left: 4px solid #f472b6;
    padding: 14px 18px;
    margin: 20px auto 0;
    border-radius: 10px;
    text-align: left;
    font-size: 13px;
    color: #fbcfe8;
    max-width: 620px;
    line-height: 1.6;
}
.disclaimer-box strong {
    color: #f472b6;
}

/* Chatbot container */
[class*="chatbot"] {
    background: rgba(15, 15, 26, 0.4) !important;
    border: 1px solid rgba(244, 114, 182, 0.15) !important;
    border-radius: 16px !important;
}

/* Reset all message backgrounds first */
.message, .message-wrap, .message-row, .message-bubble {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
}

/* USER messages - solid pink bubble */
.message-row.user .message-bubble,
.user .message,
div[class*="user"] > div[class*="message"] {
    background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%) !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 12px rgba(244, 114, 182, 0.25) !important;
    border: none !important;
}

/* BOT messages - dark card */
.message-row.bot .message-bubble,
.bot .message,
div[class*="bot"] > div[class*="message"],
div[class*="assistant"] > div[class*="message"] {
    background: rgba(30, 30, 45, 0.9) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(244, 114, 182, 0.15) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
}

/* Text inside messages */
.message p, .message span, .message-bubble p, .message-bubble span {
    background: transparent !important;
    color: inherit !important;
    margin: 0 !important;
    line-height: 1.7 !important;
    font-size: 15px !important;
}

/* Input textbox */
textarea, input[type="text"] {
    background: rgba(15, 15, 26, 0.8) !important;
    color: #f8fafc !important;
    border: 2px solid rgba(244, 114, 182, 0.3) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
}
textarea:focus, input:focus {
    border-color: #f472b6 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(244, 114, 182, 0.15) !important;
}
textarea::placeholder, input::placeholder {
    color: #64748b !important;
}

/* Primary buttons */
button.primary, .primary {
    background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%) !important;
    color: white !important;
    border: none !important;
    padding: 12px 28px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 4px 15px rgba(244, 114, 182, 0.3) !important;
}
button.primary:hover, .primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(244, 114, 182, 0.5) !important;
}

/* Example chips */
.examples button {
    background: rgba(244, 114, 182, 0.08) !important;
    color: #fbcfe8 !important;
    border: 1.5px solid rgba(244, 114, 182, 0.3) !important;
    border-radius: 100px !important;
    padding: 10px 20px !important;
    font-size: 13px !important;
    margin: 4px !important;
}
.examples button:hover {
    background: rgba(244, 114, 182, 0.15) !important;
    border-color: #f472b6 !important;
}

/* Hide gradio footer */
footer, .footer, .built-with { display: none !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(15, 15, 26, 0.5); }
::-webkit-scrollbar-thumb {
    background: rgba(244, 114, 182, 0.3);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(244, 114, 182, 0.5); }

/* Action icons */
button.icon-button, .icon-button {
    color: #94a3b8 !important;
    background: transparent !important;
}
button.icon-button:hover {
    color: #f472b6 !important;
}
"""

with gr.Blocks(title="Jiya - Postpartum AI Companion") as demo:
    gr.HTML("""
        <div class="header-card">
            <div style="font-size: 56px; margin-bottom: 8px;">💛</div>
            <h1>Jiya — Postpartum AI Companion</h1>
            <p>A warm, empathetic AI companion for postpartum recovery.<br/>
            Available 24/7 with judgment-free support.</p>
            <div class="disclaimer-box">
                <strong>⚠️ Medical Disclaimer:</strong> This AI provides information and support only —
                not medical advice. Always consult your doctor. Emergencies: <strong>911</strong>.
                Maternal Mental Health Hotline: <strong>1-833-943-5746</strong>
            </div>
        </div>
    """)

    chatbot = gr.ChatInterface(
        fn=respond,
        examples=[
            "I had my baby 2 weeks ago and I am feeling really sad",
            "Is it normal to feel overwhelmed?",
            "How can I tell if I have postpartum depression?",
            "I am having trouble breastfeeding, what should I do?",
        ],
        cache_examples=False,
    )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        theme=custom_theme,
        css=custom_css,
        ssr_mode=False
    )
