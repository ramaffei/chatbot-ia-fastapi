from typing import List, Dict, Any
import httpx
from pypdf import PdfReader
from io import BytesIO
import uuid


class DocumentService:
    def __init__(self, chroma_url: str):
        print(f"ChromaDB URL: {chroma_url}")
        self.chroma_url = f"http://{chroma_url}:8000"
        self.headers = {
            "Authorization": "Basic YWRtaW46YWRtaW4=",  # admin:admin in base64
            "Content-Type": "application/json",
        }

    async def process_pdf(self, file_content: bytes, conversation_id: str) -> str:
        """Process a PDF file and store its content in ChromaDB"""
        # Extract text from PDF
        pdf_text = self._extract_text_from_pdf(file_content)

        # Generate a unique document ID
        document_id = str(uuid.uuid4())

        # Create collection if it doesn't exist
        collection_name = f"conversation_{conversation_id}"
        await self._create_or_get_collection(collection_name)

        # Add document to ChromaDB
        await self._add_documents(
            collection_name=collection_name,
            documents=[pdf_text],
            metadatas=[
                {"document_id": document_id, "conversation_id": conversation_id}
            ],
            ids=[document_id],
        )

        return document_id

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text content from a PDF file"""
        pdf = PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text

    async def _create_or_get_collection(self, name: str) -> None:
        """Create a new collection in ChromaDB if it doesn't exist"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.chroma_url}/api/v1/collections",
                    headers=self.headers,
                    json={"name": name},
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code != 409:  # 409 means collection already exists
                    raise

    async def _add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str],
    ) -> None:
        """Add documents to a ChromaDB collection"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.chroma_url}/api/v1/collections/{collection_name}/add",
                headers=self.headers,
                json={"documents": documents, "metadatas": metadatas, "ids": ids},
            )
            response.raise_for_status()

    async def query_documents(
        self, conversation_id: str, query: str, n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Query documents in a conversation's collection"""
        collection_name = f"conversation_{conversation_id}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.chroma_url}/api/v1/collections/{collection_name}/query",
                headers=self.headers,
                json={"query_texts": [query], "n_results": n_results},
            )
            response.raise_for_status()
            results = response.json()

            # Format results
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            return [
                {
                    "content": doc,
                    "metadata": meta,
                    "relevance": 1 - dist,  # Convert distance to relevance score
                }
                for doc, meta, dist in zip(documents, metadatas, distances)
            ]
