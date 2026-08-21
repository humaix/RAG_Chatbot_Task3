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
                "what can you do",
                "can you help me",
                "thanks",
                "thank you",
                "which model are you"
            ],
            "document": [
                "who is Sara",
                "who is Ali",
                "who is Ahmed",
                "how many leave days does Sara have",
                "which department does Ali work in",
                "what does the company policy say",
                "what is this paper about",
                "what information is in this document"
            ]
        }

        self.example_embeddings = {}

        for intent, examples in self.examples.items():
            self.example_embeddings[intent] = (
                self.embedding_model.embed_documents(examples)
            )

    def detect_intent(self, question):

        question_embedding = np.array(
            self.embedding_model.embed_query(question)
        )

        best_intent = "document"
        best_score = -1

        for intent, embeddings in self.example_embeddings.items():

            for embedding in embeddings:

                embedding = np.array(embedding)

                score = np.dot(
                    question_embedding,
                    embedding
                ) / (
                    np.linalg.norm(question_embedding)
                    * np.linalg.norm(embedding)
                )

                if score > best_score:
                    best_score = score
                    best_intent = intent

        return best_intent, best_score