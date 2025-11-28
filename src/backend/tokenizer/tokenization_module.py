from typing import List
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document   # << important

def load_pdf_files(data_path: str) -> List[Document]:
    loader = DirectoryLoader(
        data_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} PDF documents.")
    return documents


def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs = []
    for doc in docs:
        source = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": source}
            )
        )
    return minimal_docs


def split_documents(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 20
) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")
    return chunks


def setup():
    data_path = "/media/anurag/Windows/Projects/ML_PATH/medical_chatbot/data"
    raw_documents = load_pdf_files(data_path)
    minimal_documents = filter_to_minimal_docs(raw_documents)
    chunked_documents = split_documents(minimal_documents)
    return raw_documents, minimal_documents, chunked_documents
