# import logging
# import os
# from dotenv import load_dotenv
# # from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
# load_dotenv()
#
#
#
# # class LLM:
# #     def __init__(self, model_name, temperature):
# #         self.logger = logging.getLogger(__name__)
# #         self.model = ChatGoogleGenerativeAI(model=model_name,temperature=temperature)
# #     def generate(self, prompt):
# #         try:
# #             response = self.model.invoke(prompt)
# #             if isinstance(response.content, list):
# #                 for item in response.content:
# #                     if item.get("type") == "text":
# #                         return item.get("text", "")
# #                 return ""
# #             return response.content
# #         except Exception as error:
# #             self.logger.error(f"LLM generation failed: {error}")
# #             return ("Sorry, I could not generate a response right now. "
# #                     "Please try again."
# #             )
#
#
# class LLM:
#     def __init__(self, model_name: str, temperature: float = 0.2):
#         self.logger = logging.getLogger(__name__)
#         # API key
#         api_key = os.getenv("GROQ_API_KEY")
#         if not api_key:
#             self.logger.error("GROQ_API_KEY environment variable not found.")
#             raise ValueError("GROQ_API_KEY is missing in .env file.")
#
#         self.model = ChatGroq(model=model_name,temperature=temperature,groq_api_key=api_key)
#     def generate(self, prompt: str) -> str:
#         try:
#             response = self.model.invoke(prompt)
#             if isinstance(response.content, list):
#                 for item in response.content:
#                     if isinstance(item, dict) and item.get("type") == "text":
#                         return item.get("text", "")
#                     elif isinstance(item, str):
#                         return item
#                 return ""
#             return str(response.content)
#         except Exception as error:
#             self.logger.error(f"LLM generation failed: {error}")
#             return (
#                 "Sorry, I could not generate a response right now. "
#                 "Please try again."
#             )




import logging
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
class LLM:
    def __init__(self,model_name: str,temperature: float = 0.2):
        self.logger = logging.getLogger(__name__)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            self.logger.error("GROQ_API_KEY environment variable not found.")
            raise ValueError("GROQ_API_KEY is missing in .env file.")
        self.model = ChatGroq(
            model=model_name,
            temperature=temperature,
            groq_api_key=api_key,
            timeout=60,
            max_retries=3
        )
    def generate(self, prompt: str) -> str:
        try:
            response = self.model.invoke(prompt)
            if isinstance(response.content, list):
                for item in response.content:
                    if isinstance(item, dict):
                        if item.get("type") == "text":
                            return item.get("text", "")
                    elif isinstance(item, str):
                        return item
                return ""
            return str(response.content)
        except Exception as error:
            self.logger.error(f"LLM generation failed: {error}")
            return (
                "Sorry, I could not generate a response right now. "
                "Please try again."
            )