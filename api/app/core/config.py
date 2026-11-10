from functools import lru_cache

from langchain.embeddings import init_embeddings
from langchain_core.embeddings import Embeddings
from pydantic_settings import BaseSettings, SettingsConfigDict
from qdrant_client import QdrantClient


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RAG_", env_file=".env", extra="ignore"
        )

    data_path: str = "shop_handbook.pdf"

    chat_provider: str = "ollama"
    chat_model: str = "gemma3:4b"
    embed_provider: str = "ollama"
    embed_model: str = "nomic-embed-text:latest"
    embed_dim: int = 768
    temperature: float = 0.5


    top_k: int = 5
    chunk_size: int = 600
    chunk_overlap: int = 100

    collection_name: str = "shop_handbook"
    qdrant_path: str = "./qdrant_data"
    qdrant_url: str = "http://localhost:6333"



    system_prompt= (
        "You are a helpful assistant that answers questions about the shop handbook."
         "Answers should be based on the content of the handbook, and if the answer is not found in the handbook, respond with 'I don't know.'" \
         "if answer is not found in the handbook, respond with 'I don't know.'"
          )

@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_embeddings() -> None:
    return init_embeddings(
        provider=get_settings().embed_provider,
        model=get_settings().embed_model,
        embed_dim=get_settings().embed_dim,
    )

def get_qdrant_client(settings: Settings) -> QdrantClient:
    return QdrantClient(
        path=settings.qdrant_path,
        url=settings.qdrant_url
    )