import gradio as gr
from groq import Groq
from prompts import SYSTEM_PROMPT
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Init Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Store conversation history per session
conversations = {}

def respond(message, history, session_id):
    """Handle chat messages with memory"""
    # Initialize session history if new
    if session_id not in conversations:
        conversations[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # Add user message
    conversations[session_id].append({"role": "user", "content": message})

    # Get response from Groq
    response = client.chat.completions.create(
        model=MODEL,
        messages=conversations[session_id],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )

    # Extract assistant response
    assistant_message = response.choices[0].message.content

    # Add to history
    conversations[session_id].append({"role": "assistant", "content": assistant_message})

    return assistant_message

# Create the chatbot interface
chatbot = gr.ChatInterface(
    fn=respond,
    chatbot=gr.Chatbot(height=500),
    textbox=gr.Textbox(
        placeholder="How are you feeling today?",
        label="Talk to Jiya"
    ),
    title="💛 Jiya - Postpartum AI Companion",
    description=(
        "A warm, empathetic AI health companion supporting new mothers through postpartum recovery. "
        "**Always consult your doctor for medical advice.**"
    ),
    examples=[
        ["I had my baby 2 weeks ago and I'm feeling really sad and I don't know why"],
        ["Is it normal to feel overwhelmed with a newborn?"],
        ["How can I tell if I have postpartum depression?"],
    ],
    theme="soft",
    cache_examples=True,
)

# Launch with custom CSS
chatbot.launch(server_name="0.0.0.0", server_port=7860)