from tkinter.ttk import Separator
from zipfile import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import PdfReader
from qdrant_client.models import Distance, VectorParams

from core.config import get_embeddings, get_qdrant_client, get_settings

def load(path: Path) -> None:
    pass

def ingest(path: str | None = None) -> None:
    settings = get_settings()
    file = Path(path or get_settings().data_path)

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
    separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents=load(path=file))

    # 3. embed
    embed = get_embeddings(settings)

    # 4. store
    client = get_qdrant_client(settings)

    try:
        if client.collection_exists(collection_name=settings.collection_name):
            client.delete_collection(collection_name=settings.collection_name)
            client.create_collection(
                collection_name=settings.collection_name,
                vectors_config=VectorParams(size=settings.embedding_dim,distance=Distance.COSINE)
            )

    except:
        client.close()

    return len(chunks)



if __name__ == "__main__":
    ingest()  