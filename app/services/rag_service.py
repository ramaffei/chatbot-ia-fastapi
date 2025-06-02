import logging

from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from exceptions.rag import RAGException
from repositories.vector_store import FAISSVectorStore
from services.document_service import DocumentService
from langchain_core.embeddings import Embeddings

fake_embeddings = DeterministicFakeEmbedding(size=4096)

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(
        self,
    ) -> None:
        self.document_service = DocumentService()
        self.embedding: Embeddings = fake_embeddings
        self.vector_store = FAISSVectorStore(embeddings=self.embedding)

    def add_pdf_to_vector_store(
        self,
        file: bytes | None = None,
    ) -> list[Document]:
        split_documents = self.document_service.pdf_to_documents(
            file_bytes=file,
            chunk_size=1000,
            chunk_overlap=200,
        )
        logger.info(f"Adding {len(split_documents)} documents to vector store")
        if not split_documents:
            raise RAGException(RAGException.ErrorCode.Documents_Not_Found)
        self.vector_store.store.add_documents(split_documents)
        return split_documents

    def similarity_search_by_query(self, query: str) -> str:
        documents = self.vector_store.store.similarity_search(query)
        return self._documents_to_string(documents)

    def retrieve_str_documents(self, query: str) -> str:
        retriever = self.vector_store.store.as_retriever()
        documents = retriever.invoke(query)
        return self._documents_to_string(documents)

    def _documents_to_string(self, documents: list[Document]) -> str:
        return "".join(d.page_content for d in documents if d.page_content)
