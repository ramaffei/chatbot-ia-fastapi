import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings


class FAISSVectorStore:
    def __init__(
        self,
        embeddings: Embeddings,
    ) -> None:
        self.embeddings: Embeddings = embeddings
        self.index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
        self.docstore = InMemoryDocstore()

        self._store = None

    @property
    def store(self) -> FAISS:
        if not self._store:
            self._store = FAISS(
                embedding_function=self.embeddings,
                index=self.index,
                docstore=self.docstore,
                index_to_docstore_id={},
            )
        return self._store


# from langchain_chroma import Chroma


# class ChromaVectorStore:
#     """
#     Clase para manejar un vector store utilizando Chroma.
#     Permite crear o cargar un vector store desde documentos.
#     """

#     def __init__(
#         self,
#         embeddings: str,
#         collection_name: str = "docs_collection",
#         persist_directory: str = "./chroma_langchain_db",
#     ):
#         self.collection_name = collection_name
#         self.persist_directory = persist_directory
#         self.embeddings = embeddings

#         self._store = None

#     @property
#     def store(self) -> Chroma:
#         if not self._store:
#             self._store = Chroma(
#                 collection_name=self.collection_name,
#                 persist_directory=self.persist_directory,
#                 embedding_function=self.embeddings,
#             )
#         return self._store
