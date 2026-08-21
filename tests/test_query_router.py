from app.brain.embedding import EmbeddingManager
from app.brain.query_router import QueryRouter

def test_general_query():
    embedding_manager = EmbeddingManager(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    embedding_model = embedding_manager.get_model()
    router = QueryRouter(embedding_model)
    intent, score = router.detect_intent(
        "hello, how are you?"
    )
    assert intent == "general"
    assert score > 0