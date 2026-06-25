from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class Settings:
    llm_api_key: str
    llm_model: str
    vlm_api_key: str
    vlm_model: str
    embedding_api_key: str
    embedding_model: str
    embedding_dim: int
    ssl_certificate: str


def load_settings() -> Settings:
    load_dotenv()

    return Settings(
        llm_api_key=os.getenv("LLM_API_KEY"),
        llm_model=os.getenv("LLM_MODEL"),

        vlm_api_key=os.getenv("VLM_API_KEY"),
        vlm_model=os.getenv("VLM_MODEL"),

        embedding_api_key=os.getenv("EMBEDDING_API_KEY"),
        embedding_model=os.getenv("EMBEDDING_MODEL"),
        embedding_dim=int(os.getenv("EMBEDDING_DIM")),

        ssl_certificate=os.getenv("SSL_CERTIFICATE"),
    )