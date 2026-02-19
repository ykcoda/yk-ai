import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


class DocLoader:
    def __init__(self, dir_path: str):
        self.dir_path: str = dir_path
        self.documents: list[str] = []

    @property
    def load_documents(self):
        for filename in os.listdir(self.dir_path):
            doc_path = os.path.join(self.dir_path, filename)
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(doc_path)
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(doc_path)
            else:
                print(f"Unsupported file format: {filename}")
                continue
            self.documents.extend(loader.load())
        return self.documents
