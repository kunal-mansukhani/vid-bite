import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import PythonCodeTextSplitter
from langchain.schema import Document

class ExamplesDB:
    def __init__(self, embedding_model="sentence-transformers/all-MiniLM-L6-v2", persist_dir="examples_base") -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vectorstore = None
        self.persist_dir = persist_dir
        self.text_splitter = PythonCodeTextSplitter(chunk_size=1000, chunk_overlap=200)

    def add_python_files_from_folder(self, folder_path: str):
        documents = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.py'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    content = file.read()
                    chunks = self.text_splitter.split_text(content)
                    for chunk in chunks:
                        documents.append(Document(page_content=chunk, metadata={"source": filename}))
        
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(documents=documents, embedding=self.embeddings, persist_directory=self.persist_dir)
        else:
            self.vectorstore.add_documents(documents)

    def query(self, query: str, top_k=5):
        if self.vectorstore is None:
            raise ValueError("No vectorstore to query. Add documents first.")

        docs = self.vectorstore.similarity_search(query, k=top_k)
        return [{"content": doc.page_content, "source": doc.metadata["source"]} for doc in docs]

    def save_vectorstore(self):
        if self.vectorstore:
            self.vectorstore.persist()

    def load_vectorstore(self):
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )

if __name__ == "__main__":
    import time

    rag = ExamplesDB(persist_dir="python_examples_knowledge_base")
    