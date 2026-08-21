from dotenv import load_dotenv
from app.core.config import Config
from app.core.logger import get_logger
from app.knowledge_base.loaders import DocumentLoader
from app.knowledge_base.chunker import DocumentChunker
from app.brain.embedding import EmbeddingManager
from app.brain.vector_store import VectorStore

load_dotenv()

def main():
    logger = get_logger("ingestion")
    config = Config()
    logger.info("Document ingestion started")
    # Load documents
    folder = config.get("data","document_directory")
    loader = DocumentLoader(folder)
    documents = loader.load_documents()
    logger.info(f"Documents loaded: {len(documents)}")

    # Split documents into chunks
    chunk_size = config.get("chunking","chunk_size")
    chunk_overlap = config.get("chunking","chunk_overlap")
    chunker = DocumentChunker(chunk_size,chunk_overlap)
    chunks = chunker.split_documents(documents)
    logger.info(f"Chunks created: {len(chunks)}")
    # Create embedding model
    model_name = config.get("embedding","model_name")
    embedding_manager = EmbeddingManager(model_name)
    embedding_model = embedding_manager.get_model()
    logger.info("Embedding model loaded")
    # Create vector store
    directory = config.get("vector_store","directory")
    collection = config.get("vector_store","collection_name")
    vector_store = VectorStore(directory,collection,embedding_model)
    vector_store.add_documents(chunks)
    logger.info("Documents indexed successfully")


if __name__ == "__main__":
    main()