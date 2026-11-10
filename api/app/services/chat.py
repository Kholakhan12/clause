from langchain.chat_models import init_chat_model
from langchain_qdrant import QdrantVectorStore
from core.config import get_settings, get_qdrant_client, get_embeddings
from pydantic import BaseModel

NO_ANSWER = "I don't know."


class Source(BaseModel):
    source: str
    page: int | None = None
    score: float | None = None


class Answer(BaseModel):
    answer: str
    sources: list[Source]


class RAGService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = get_qdrant_client(settings=self.settings)

        if not self.client.collection_exists(self.settings.collection_name):
            raise RuntimeError(
                f"Collection {self.settings.collection_name} not found. "
                "Please run the ingestion script first."
            )

        self.store = QdrantVectorStore(
            client=self.client,
            collection_name=self.settings.collection_name,
            embedding=get_embeddings(settings=self.settings),
        )

        self.llm = init_chat_model(
            model=self.settings.chat_model,
            model_provider=self.settings.chat_provider,
            temperature=self.settings.chat_temperature,
        )

    def ask(self, question: str) -> Answer:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty")

        results = self.store.similarity_search_with_score(
            query=question,
            k=self.settings.top_k,
        )

        if not results:
            return Answer(answer=NO_ANSWER, sources=[])

        context = "\n\n".join(
            doc.page_content for doc, _ in results
        )

        messages = [
            {"role": "system", "content": self.settings.system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ]

        return Answer(
            answer=self.llm.invoke(messages).text,
            sources=[
                Source(
                    source=doc.metadata.get("source", "unknown"),
                    page=doc.metadata.get("page"),
                    score=round(float(score), 4),
                )
                for doc, score in results
            ],
        )

    def close(self) -> None:
        self.client.close()


rag_service = RAGService()

try:
    query = input("Ask a question: ")
    result = rag_service.ask(query)
    print(result.model_dump_json(indent=2))
finally:
    rag_service.close() 
from services.chat_service import RAGService


def main():
    rag_service = RAGService()
    try:
        query = input("Ask a question: ").strip()
        result = rag_service.ask(query)
        print(f"AI: {result.answer}")
    except:
        pass
    finally:
        rag_service.close()


if __name__ == "__main__":
    main()