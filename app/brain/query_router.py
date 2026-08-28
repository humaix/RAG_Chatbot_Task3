import numpy as np
class QueryRouter:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.examples = {
            "general": [
                "hello",
                "hi",
                "hey",
                "how are you",
                "how are you doing",
                "how are things",
                "what's up",
                "hope you're doing well",
                "nice to meet you",
                "good morning",
                "good evening",
                "what can you do",
                "can you help me",
                "tell me about yourself",
                "who are you",
                "which model are you",
                "thanks",
                "thank you",
                "goodbye",
                "bye",
                "see you later",
                "that's great",
                "ok thanks",
                "appreciate it",
            ],
            "document": [
                "who is this person",
                "tell me about this employee",
                "how many leave days does this person have",
                "which department does this person work in",
                "what does the company policy say",
                "what is this paper about",
                "what information is in this document",
                "what is the title of this paper",
                "who are the authors",
                "summarize this document",
                "what are the key findings",
                "what data is in the spreadsheet",
                "list the employees",
                "what roles are mentioned",
                "what job opportunities are available",
            ]
        }
        self.example_embeddings = {}
        for intent, examples in self.examples.items():
            self.example_embeddings[intent] = (
                self.embedding_model.embed_documents(examples)
            )
    def detect_intent(self, question):
        question_embedding = np.array(self.embedding_model.embed_query(question))
        best_scores = {}
        for intent, embeddings in self.example_embeddings.items():
            best = -1
            for embedding in embeddings:
                embedding = np.array(embedding)
                score = np.dot(
                    question_embedding,
                    embedding
                ) / (
                    np.linalg.norm(question_embedding)
                    * np.linalg.norm(embedding)
                )
                if score > best:
                    best = score
            best_scores[intent] = best
        general_score = best_scores.get("general", -1)
        document_score = best_scores.get("document", -1)
        if general_score >= 0.45 and general_score > document_score + 0.05:
            return "general", general_score
        return "document", document_score