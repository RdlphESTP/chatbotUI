import litellm
from pydantic import BaseModel

from chatbotui.config import load_settings


def main(
    messages: list[dict],
    response_format=None,
    effort: str=None,
    verbosity: str=None,
    temperature : str=None
):
    settings = load_settings()

    litellm.ssl_certificate = settings.ssl_certificate

    response = litellm.completion(
        model=settings.llm_model,
        api_key=settings.llm_api_key,
        timeout=30,
        stream=True,
        drop_params=True,   # Drops unsupported parameters depending on the model

        messages=messages,
        response_format=response_format,
        reasoning_effort=effort,
        verbosity=verbosity,
        temperature=temperature,
    )

    for chunk in response:
        yield chunk.choices[0].delta.content or ""


if __name__ == "__main__":
    messages=[
        {"role": "system", "content": "If no sources are available, say that you don’t know."},
        {"role": "user", "content": "What does the green LED on the central processing unit mean?"},
    ]


    class RAGAnswer(BaseModel):
        answer: str
        sources: list[str]


    for token in main(messages, RAGAnswer):
        print(token, end="", flush=True)
