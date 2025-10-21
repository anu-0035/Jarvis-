# rag_pipeline.py
import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv


# LangChain imports
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")


if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment (see .env.example)")


# === Helper: load documents from a folder (txt and pdf) ===


def load_documents(data_dir: str) -> List[object]:
    """Load .txt and .pdf files from a directory and return LangChain Document objects."""
    docs = []
    p = Path(data_dir)
    if not p.exists():
        return docs


    for f in p.iterdir():
        if f.suffix.lower() == ".txt":
            loader = TextLoader(str(f))
            docs.extend(loader.load())
        elif f.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(f))
            docs.extend(loader.load())
    return docs




# === Build or load vectorstore ===


def build_or_load_vectorstore(data_dir: str = "../data", persist_directory: str = CHROMA_PERSIST_DIR):
    """
    Loads documents from `data_dir`, splits them into chunks, creates embeddings and stores them in Chroma.
    If a persisted Chroma directory already exists, it will load it instead of rebuilding.
    """


    # Embeddings and other LLM config
    embeddings = OpenAIEmbeddings()


    # If Chroma persistence exists, load it
    if Path(persist_directory).exists() and any(Path(persist_directory).iterdir()):
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        return vectordb


    # Load documents
    docs = load_documents(data_dir)
    if not docs:
        # no docs found, return empty vectordb (in-memory)
        return Chroma.from_texts([], embedding=embeddings)


    # Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)


    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()
    return vectordb


# === Create QA chain ===


class RAGEngine:
    def __init__(self, data_dir: str = "../data", persist_directory: str = CHROMA_PERSIST_DIR, model_name: str = "gpt-4o-mini"):
        self.vectordb = build_or_load_vectorstore(data_dir=data_dir, persist_directory=persist_directory)
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": 4})
        # LLM for final answer generation
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.0)
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.retriever)


    def answer(self, query: str) -> str:
        if not query:
            return ""
        return self.qa_chain.run(query)




    # Create a global engine instance (lazy creation is fine for small demos)
    _engine: RAGEngine | None = None


    def get_engine() -> RAGEngine:
        global _engine
        if _engine is None:
            # data directory relative to backend/ folder
            _engine = RAGEngine(data_dir="../data")
        return _engine




    def rag_answer(query: str) -> str:
        engine = get_engine()
        return engine.answer(query)