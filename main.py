import litellm

from chatbotui.config import load_settings


def main(role: str, content: str):
    settings = load_settings()

    litellm.ssl_certificate = settings.ssl_certificate

    response = litellm.completion(
        model=settings.llm_model,
        api_key=settings.llm_api_key,
        stream=True,
        messages=[{"role": role, content: "Say Hello."}],
    )

    for chunk in response:
        yield chunk.choices[0].delta.content or ""


if __name__ == "__main__":
    for token in main('user', 'Say hello.'):
        print(token, end="", flush=True)
