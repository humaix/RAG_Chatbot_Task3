from pathlib import Path
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, jsonify
from app.core.config import Config
from app.brain.embedding import EmbeddingManager
from app.brain.vector_store import VectorStore
from app.brain.retriever import Retriever
from app.brain.prompt import create_prompt
from app.brain.llm import LLM
from app.brain.query_router import QueryRouter
from app.knowledge_base.chunker import DocumentChunker
from app.knowledge_base.loaders import DocumentLoader
from app.chat.conversation import Conversation

load_dotenv()
web = Blueprint("web", __name__)
config = Config()
# RAG COMPONENTS
embedding_name = config.get("embedding","model_name")
embedding_manager = EmbeddingManager(embedding_name)
embedding_model = embedding_manager.get_model()
router = QueryRouter(embedding_model)
directory = config.get("vector_store","directory")
collection = config.get("vector_store","collection_name")
vector_store = VectorStore(directory,collection,embedding_model)
top_k = config.get("retrieval","top_k")
retriever = Retriever(vector_store.get_store(),top_k)
llm_model = config.get("llm","model_name")
temperature = config.get("llm","temperature")
llm = LLM(llm_model,temperature)

conversation = Conversation()


# DOCUMENT UPLOAD
UPLOAD_FOLDER = Path("data/documents")
UPLOAD_FOLDER.mkdir(parents=True,exist_ok=True)
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".xlsx"
}
def allowed_file(filename):
    return (
        Path(filename)
        .suffix
        .lower()
        in ALLOWED_EXTENSIONS
    )
# HOME
@web.route("/")
def home():
    return render_template(
        "index.html"
    )
# CHAT
@web.route(
    "/chat",
    methods=["POST"]
)
def chat():
    data = request.get_json()
    question = data.get(
        "question",
        ""
    ).strip()
    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400
    # QUERY ROUTING
    intent, intent_score = router.detect_intent(question)
    # Casual/general questions
    # should not trigger retrieval.
    if (
        intent == "general"
        and intent_score >= 0.55
    ):
        answer = (
            "Hello! How can I help you "
            "with your documents?"
        )
        return jsonify({
            "answer": answer,
            "sources": []
        })
    # RETRIEVAL
    try:
        results = retriever.search(
            question
        )
        context = "\n\n".join(
            document.page_content
            for document in results
        )
        # CONVERSATION HISTORY
        history = conversation.get_history()
        history_text = "\n".join(
            f"{item['role']}: "
            f"{item['message']}"
            for item in history
        )
        # CREATE PROMPT
        prompt_template = create_prompt()
        prompt = prompt_template.invoke({
            "context": context,
            "question": question,
            "history": history_text
        })
        # GENERATE ANSWER
        answer = llm.generate(prompt)
        # SAVE CONVERSATION
        conversation.add_message("User",question)
        conversation.add_message("Assistant",answer)
        # SOURCES
        sources = []
        for document in results:
            source = document.metadata.get("source","Unknown source")
            row = document.metadata.get("row")
            if row is not None:
                source = (
                    f"{source} "
                    f"(Row {row})"
                )
            if source not in sources:
                sources.append(source)
        return jsonify({
            "answer": answer,
            "sources": sources
        })
    except Exception as error:
        print(f"Chat request failed: {error}")
        return jsonify({
            "answer": (
                "Sorry, I could not "
                "generate a response "
                "right now."
            ),
            "sources": []
        })
# FILE UPLOAD
@web.route(
    "/upload",
    methods=["POST"]
)
def upload():
    if "file" not in request.files:
        return jsonify({
            "error": "No file selected."
        }), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({
            "error": "No file selected."
        }), 400
    if not allowed_file(file.filename):
        return jsonify({
            "error": (
                "Only PDF, DOCX, TXT "
                "and XLSX files are supported."
            )
        }), 400
    try:
        file_path = UPLOAD_FOLDER / file.filename
        # Check for duplicate file
        if file_path.exists():
            return jsonify({
                "error": (
                    f"{file.filename} already exists. "
                    "Please use a different file name."
                )
            }), 409
        file.save(file_path)
        # Load only the uploaded file
        loader = DocumentLoader(str(UPLOAD_FOLDER))
        documents = loader.load_file(file_path)
        if not documents:
            file_path.unlink(missing_ok=True)
            return jsonify({
                "error": (
                    "The uploaded file "
                    "could not be read."
                )
            }), 400
        # Chunk uploaded document
        chunk_size = config.get("chunking","chunk_size")
        chunk_overlap = config.get("chunking","chunk_overlap")
        chunker = DocumentChunker(chunk_size,chunk_overlap)
        chunks = chunker.split_documents(documents)
        if not chunks:
            file_path.unlink(missing_ok=True)
            return jsonify({
                "error": (
                    "No usable content was found "
                    "in the uploaded file."
                )
            }), 400
        # Add only the new file to ChromaDB
        vector_store.add_documents(chunks)
        return jsonify({
            "message": (
                f"{file.filename} "
                "uploaded and indexed successfully."
            )
        })
    except Exception as error:
        print(f"Upload failed: {error}")
        return jsonify({
            "error": (
                "File upload or indexing failed."
            )
        }), 500
# CLEAR CHAT
@web.route(
    "/clear",
    methods=["POST"]
)
def clear_chat():
    conversation.clear()
    return jsonify({
        "message":
        "Conversation history cleared."
    })