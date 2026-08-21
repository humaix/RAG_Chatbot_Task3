from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
import pandas as pd
from langchain_core.documents import Document

class DocumentLoader:
    def __init__(self,folder_path):
        self.folder_path = Path(folder_path)

    def load_excel(self, file_path):
        dataframe = pd.read_excel(file_path)
        documents = []
        for index, row in dataframe.iterrows():
            text = " | ".join(f"{column}: {value}"
                for column, value in row.items())
            document = Document(page_content=text,metadata={
                    "source": str(file_path),
                    "row": index + 1
                })
            documents.append(document)
        return documents

    def load_documents(self):
        documents = []
        for file_path in self.folder_path.iterdir():
            if file_path.suffix.lower()==".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix.lower()==".docx":
                loader = Docx2txtLoader(str(file_path))
            elif file_path.suffix.lower() == ".txt":
                loader = TextLoader(str(file_path),encoding="utf-8")
            elif file_path.suffix.lower() == ".xlsx":
                documents.extend(self.load_excel(file_path))
                continue
            else:
                continue
            documents.extend(loader.load())

    def load_file(self, file_path):
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        if extension == ".pdf":
            loader = PyPDFLoader(str(file_path))
            return loader.load()
        elif extension == ".docx":
            loader = Docx2txtLoader(str(file_path))
            return loader.load()
        elif extension == ".txt":
            loader = TextLoader(str(file_path),encoding="utf-8")
            return loader.load()
        elif extension == ".xlsx":
            return self.load_excel(file_path)
        return []
        return documents

