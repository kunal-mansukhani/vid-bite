from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from scraper.scraper import scrape_docs
from scraper.utils import save_documents, load_documents
import time

class RAG:
    def __init__(self, embedding_model="sentence-transformers/all-MiniLM-L6-v2", persist_dir="knowledge_base") -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

        self.documents = []
        self.vectorstore = None
        self.persist_dir = persist_dir


    def add_documents_from_url(self, url: str, name: str="Knowledge"):
        documents = scrape_docs(url)
        self.add_document(documents)
        save_documents(documents, f"{name}.pkl")

    def load_documents(self, path: str):
        self.documents = load_documents(path)
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(documents=self.documents, embedding=self.embeddings, persist_directory=self.persist_dir)
        else:
            self.vectorstore.add_documents(self.documents)

    def add_document(self, documents: list):
        self.documents.extend(documents)
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(documents=self.documents, embedding=self.embeddings, persist_directory=self.persist_dir)
        else:
            self.vectorstore.add_documents(documents)

    def query(self, query: str, top_k=5):
        if self.vectorstore is None:
            raise ValueError("No vectorstore to save. Add documents first.")

        docs = self.vectorstore.similarity_search(query, k=top_k)

        contents = [doc.page_content for doc in docs]
        return contents
    
    def save_vectorstore(self,):
        self.vectorstore.persist()

    def load_vectorstore(self, path: str):
        self.persist_dir = path
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )

    
if __name__== "__main__":
    # # Option 1: Add documents from URL (It will scrape the web first)
    # rag = RAG()
    # rag.add_documents_from_url("https://docs.manim.community/en/stable/", "manim_docs.pkl")
    # rag.save_vectorstore()
    # rag.query("How to create a scene in Manim")

    # Option 2: Load documents and create vectorstore
    # rag = RAG(persist_dir="knowledge_base")  # Persist_dir refers to the directory where the vectorstore will be saved
    # rag.load_documents("manim_docs.pkl")
    # rag.save_vectorstore()
    # print(rag.query("Draw a square"))
    
    # Option 3: Load vectorstore and query
    rag = RAG(persist_dir="knowledge_base")
    rag.load_vectorstore("knowledge_base")
    print(rag.query("Draw a square"))


    
        