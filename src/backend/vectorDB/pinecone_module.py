from pinecone import Pinecone, ServerlessSpec
from typing import List
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore

def initialize_pinecone(api_key: str, index_name: str, dimension: int = 768):
    pc = Pinecone(api_key=api_key)
    indexes = pc.list_indexes().names()

    if index_name not in indexes:
        print(f"Creating Pinecone index: {index_name}")
        pc.create_index(
            name="medical-chatbot",
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    else:
        print(f"Using existing index: {index_name}")

    index = pc.Index(index_name)
    return pc, index


def create_vector_store(documents: List[Document], embeddings, index_name: str, batch_size: int = 100):
    print(f"Uploading {len(documents)} chunks to Pinecone...")
    vector_store = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name,
        batch_size=batch_size
    )
    print("Vector store created successfully.")
    return vector_store


def load_existing_vector_store(index_name: str, embeddings):
    print(f"Loading vector store from index: {index_name}")
    vector_store = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )
    print("Vector store loaded.")
    return vector_store


def add_custom_documents(vector_store, documents: List[Document]):
    vector_store.add_documents(documents=documents)
    print(f"Added {len(documents)} custom documents to vector store.")
