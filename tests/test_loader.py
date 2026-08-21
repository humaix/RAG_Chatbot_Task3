from pathlib import Path
from app.knowledge_base.loaders import DocumentLoader
def test_supported_file_detection():
    loader = DocumentLoader("data/documents")
    assert Path("sample.pdf").suffix.lower() == ".pdf"
    assert Path("sample.docx").suffix.lower() == ".docx"
    assert Path("sample.txt").suffix.lower() == ".txt"
    assert Path("sample.xlsx").suffix.lower() == ".xlsx"