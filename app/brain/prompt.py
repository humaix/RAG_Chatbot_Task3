from langchain_core.prompts import PromptTemplate


def create_prompt():

    template = """
You are a helpful document assistant.

Answer the user's question using ONLY the provided context and
conversation history.

IMPORTANT RULES:
1. If the context contains information about a person, employee,
   department, leave days, role, or other details, use that information
   directly in your answer.
2. Do not say that information is unavailable if the person's details
   are present anywhere in the provided context.
3. For employee-related questions, prioritize the employee's specific
   record over general company policies.
4. Use conversation history to understand follow-up questions.
5. Do not invent or assume information that is not present.
6. If the requested information truly does not exist in the context,
   say:
   "I could not find this information in the provided documents."

Conversation history:
{history}

Context:
{context}

Current question:
{question}

Answer:
"""

    return PromptTemplate(
        template=template,
        input_variables=[
            "history",
            "context",
            "question"
        ]
    )