import logging
from langchain_huggingface import HuggingFaceEmbeddings
class EmbeddingManager:
    def __init__(self, model_name):
        self.logger = logging.getLogger(__name__)
        self.model = HuggingFaceEmbeddings(model_name=model_name)
        self.logger.info(f"Embedding model loaded: {model_name}")

    def get_model(self):
        return self.model