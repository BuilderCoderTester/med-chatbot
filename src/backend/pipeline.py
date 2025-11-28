from dotenv import load_dotenv
import os
from embeed.embedding import initialize_embeddings
from vectorDB.pinecone_module import initialize_pinecone, load_existing_vector_store
from rag.rag_module import query_rag_chain

load_dotenv()
pinecone_key = os.getenv("PINECONE_API_KEY")

# 1) Embedding model
embeddings = initialize_embeddings(
    "NeuML/pubmedbert-base-embeddings",
    use_gpu=False
)

# 2) Pinecone
index_name = "medical-chatbot"
pc, index = initialize_pinecone(pinecone_key, index_name, dimension=384)

# 3) Load vector DB
vector_store = load_existing_vector_store(index_name, embeddings)

# 4) Create RAG chain (Gemini 2.5 Flash)
# rag_chain = create_rag_chain(vector_store)

def ask_question(question):
    return query_rag_chain(vector_store,question)