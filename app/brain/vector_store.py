import logging
from langchain_chroma import Chroma
class VectorStore:
    def __init__(self, directory, collection_name, embedding_model):
        self.logger = logging.getLogger(__name__)
        self.store = Chroma(collection_name=collection_name,persist_directory=directory,embedding_function=embedding_model)
    def add_documents(self, documents):
        if not documents:
            self.logger.warning("No documents to add.")
            return
        self.store.add_documents(documents)
        self.logger.info(f"{len(documents)} documents added to ChromaDB")
    def get_store(self):
        return self.store