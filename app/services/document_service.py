import tempfile

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class DocumentService:
    def pdf_to_documents(
        self,
        file_path: str | None = None,
        file_bytes: bytes | None = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
    ) -> list[Document]:
        if not file_path and not file_bytes:
            raise ValueError("Debe proporcionar un archivo PDF o bytes del archivo.")

        if file_path:
            documents = self._load_by_path(file_path)
        else:
            documents = self._load_by_bytes(file_bytes)
        return self._split_documents(documents, chunk_size, chunk_overlap)

    def _load_by_bytes(self, file_bytes: bytes | None) -> list[Document]:
        if not file_bytes:
            raise ValueError("Debe proporcionar bytes del archivo.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            pdf_path = tmp.name

        loader = PyPDFLoader(pdf_path)
        return loader.load()

    def _load_by_path(self, file_path: str) -> list[Document]:
        loader = PyPDFLoader(file_path)
        return loader.load()

    def _split_documents(
        self, documents: list[Document], chunk_size: int, chunk_overlap: int
    ) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
        )
        return splitter.split_documents(documents)
