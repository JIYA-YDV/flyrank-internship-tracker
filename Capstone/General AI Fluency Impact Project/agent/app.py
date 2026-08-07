import chainlit as cl
from groq import AsyncGroq
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
import os

# Load environment variables
load_dotenv()

# Init Groq client (free, fast)
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# Model config — Llama 3.3 70B is excellent for empathetic conversation
MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1000
TEMPERATURE = 0.7


@cl.on_chat_start
async def start():
    """Initialize conversation with message history."""

    # Store conversation history in session
    cl.user_session.set("history", [
        {"role": "system", "content": SYSTEM_PROMPT}
    ])

    # Welcome message
    await cl.Message(
        content=(
            "Hi there 💛 I'm Jiya — your postpartum support companion.\n\n"
            "Whether you're a new mom, a partner, or just someone looking "
            "for information about postpartum health — I'm here for you.\n\n"
            "**How are you doing today?** What's on your mind?"
        )
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""

    # Get conversation history
    history = cl.user_session.get("history")

    # Add user message to history
    history.append({
        "role": "user",
        "content": message.content
    })

    # Create streaming response placeholder
    response_message = cl.Message(content="")
    await response_message.send()

    full_response = ""

    # Stream response from Groq
    stream = await client.chat.completions.create(
        model=MODEL,
        messages=history,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        stream=True
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_response += delta
            await response_message.stream_token(delta)

    await response_message.update()

    # Add assistant response to history
    history.append({
        "role": "assistant",
        "content": full_response
    })

    # Save updated history
    cl.user_session.set("history", history)