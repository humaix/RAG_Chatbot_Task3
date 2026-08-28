
from dotenv import load_dotenv
from app.core.config import Config
from app.core.logger import get_logger
from app.brain.embedding import EmbeddingManager
from app.brain.vector_store import VectorStore
from app.brain.retriever import Retriever
from app.brain.prompt import create_prompt, create_general_prompt, create_rewrite_prompt
from app.brain.llm import LLM
from app.brain.query_router import QueryRouter
from app.chat.conversation import Conversation

load_dotenv()

def main():
    logger = get_logger("rag_chatbot")
    config = Config()
    logger.info("Chatbot started")
    # Load embedding model
    model_name = config.get("embedding","model_name")
    embedding_manager = EmbeddingManager(model_name)
    embedding_model = embedding_manager.get_model()
    # Connect to existing ChromaDB
    directory = config.get("vector_store","directory")
    collection = config.get("vector_store","collection_name")
    vector_store = VectorStore(directory,collection,embedding_model)
    # Create retriever
    top_k = config.get("retrieval","top_k")
    retriever = Retriever(vector_store.get_store(),top_k)
    # Create LLM
    llm_model = config.get("llm","model_name")
    temperature = config.get("llm","temperature")
    llm = LLM(llm_model,temperature)
    # Query router
    router = QueryRouter(embedding_model)
    # Conversation memory
    conversation = Conversation()
    while True:
        question = input("\nYou: ").strip()
        if not question:
            continue
        if question.lower() in ["exit", "quit"]:
            print("Chat ended.")
            break
        if question.lower() == "clear":
            conversation.clear()
            print("Conversation history cleared.")
            continue

        history = conversation.get_history()
        history_text = "\n".join(f"{item['role']}: {item['message']}" for item in history)

        # Query routing
        intent, intent_score = router.detect_intent(question)

        if intent == "general":
            general_template = create_general_prompt()
            general_prompt = general_template.invoke({
                "history": history_text,
                "question": question
            })
            answer = llm.generate(general_prompt)
            conversation.add_message("User", question)
            conversation.add_message("Assistant", answer)
            print(f"\nBot: {answer}")
            continue

        # Rewrite follow-up questions
        if history_text.strip():
            rewrite_template = create_rewrite_prompt()
            rewrite_prompt = rewrite_template.invoke({
                "history": history_text,
                "question": question
            })
            search_query = llm.generate(rewrite_prompt).strip() or question
        else:
            search_query = question

        # Retrieve relevant documents
        results = retriever.search(search_query)
        logger.info(f"Retrieved documents: {len(results)}")
        context = "\n\n".join(document.page_content for document in results)
        # Build prompt
        prompt_template = create_prompt()
        prompt = prompt_template.invoke(
            {
                "context": context,
                "history": history_text,
                "question": question
            }
        )
        answer = llm.generate(prompt)
        conversation.add_message("User",question)
        conversation.add_message("Assistant",answer)
        print(f"\nBot: {answer}")
        # Display sources used for the answer
        sources = []
        for document in results:
            source = document.metadata.get("source","Unknown source")
            row = document.metadata.get("row")
            if row:
                source = f"{source} (Row {row})"
            if source not in sources:
                sources.append(source)
        if sources:
            print("\nSources:")
            for source in sources:
                print(f"- {source}")

if __name__ == "__main__":
    main()
