import litellm
import chainlit as cl
# from pydantic import BaseModel

from chatbotui.config import load_settings

# ================== SETUP ==================
settings = load_settings()
litellm.ssl_certificate = settings.ssl_certificate

LLM_CONFIG = {
    "model": settings.llm_model,
    "api_key": settings.llm_api_key,
    "timeout":30,
    "stream":True,
    "drop_params":True,
}

LLM_SYSTEM = "You are a helpful bot, you always reply in French."

# ================ MENU CARDS ===============
@cl.set_starters
async def starters():
    return [
        cl.Starter(
            label="Consulter une procédure",
            message="Montre-moi la procédure de consignation."
        ),
        cl.Starter(
            label="Question technique",
            message="Explique le fonctionnement d'un TGBT."
        )
    ]

# ================= SESSION =================

@cl.on_chat_start
async def start_chat():     # setup history on chat start
    cl.user_session.set(
        "history",
        [
            {
                "role": "system",
                "content": LLM_SYSTEM
            }
        ]
    )


# ================== LOOP ===================
@cl.on_message
async def on_message(prompt: cl.Message):   # get user prompt
    history = cl.user_session.get("history")    # init history

    history.append(     # update history
        {
            "role": "user",
            "content": prompt.content
        }
    )

    llm_msg = cl.Message(   # load a new response
        content=""
    )
    await llm_msg.send()

    assistant_response = ""

    try:
        response = await litellm.acompletion(
            messages=history,
            **LLM_CONFIG
        )

        async for chunk in response:
            token = chunk.choices[0].delta.content
            if token:       # in case output is empty
                assistant_response += token
                await llm_msg.stream_token(token)

        await llm_msg.update()

        history.append(     # update history
            {
                "role": "assistant",
                "content": assistant_response
            }
        )

        cl.user_session.set("history", history)

    except Exception as e:  # in case LLM fails
        llm_msg.content = f"Erreur : {str(e)}"
        await llm_msg.update()
