import re
from pathlib import Path
from langchain_core.documents import Document
class Retriever:
    def __init__(self, vector_store, top_k):
        self.vector_store = vector_store
        self.top_k = top_k
        self.retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": top_k,
                "fetch_k": top_k * 4,
            }
        )
    def _find_filename(self, question):
        match = re.search(r'([A-Za-z0-9_.-]+\.(pdf|docx|txt|xlsx))',question,re.IGNORECASE)
        if match:
            return match.group(1)
        doc_dir = Path("data/documents")
        if doc_dir.exists():
            q_lower = question.lower()
            for f in doc_dir.iterdir():
                if f.suffix.lower() in {'.pdf', '.docx', '.txt', '.xlsx'}:
                    if f.name.lower() in q_lower:
                        return f.name
        return None
    def _get_file_chunks(self, source_path, question):
        similar = self.vector_store.similarity_search(
            question,
            k=self.top_k * 2,
            filter={"source": source_path}
        )
        collection = self.vector_store._collection
        raw = collection.get(
            where={"source": source_path},
            include=["documents", "metadatas"]
        )
        all_docs = []
        for doc_text, meta in zip(raw["documents"], raw["metadatas"]):
            all_docs.append(Document(page_content=doc_text, metadata=meta))
        all_docs.sort(key=lambda d: (d.metadata.get("page", 0), d.metadata.get("row", 0)))
        first_chunks = all_docs[:5]
        seen_content = set()
        combined = []
        for doc in first_chunks + similar:
            key = doc.page_content[:200]
            if key not in seen_content:
                seen_content.add(key)
                combined.append(doc)
        return combined[:self.top_k * 3]
    def search(self, question):
        filename = self._find_filename(question)
        if filename:
            source_path = str(
                Path("data/documents") / filename
            ).replace("\\", "/")
            return self._get_file_chunks(source_path, question)

        return self.retriever.invoke(question)