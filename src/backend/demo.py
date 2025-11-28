from tokenizer.tokenization_module import setup
from embeed.embedding import initialize_embeddings
from vectorDB.pinecone_module import initialize_pinecone, create_vector_store, load_existing_vector_store
from dotenv import load_dotenv
import os

load_dotenv()
pinecone_key = os.getenv("PINECONE_API_KEY")

# Step 1: Load documents
raw_documents, minimal_documents, chunked_documents = setup()

# Step 2: Initialize embeddings (SBERT-Healthcare)
embeddings = initialize_embeddings()

# Step 3: Initialize Pinecone
index_name = "medical-chatbot"
pc, index = initialize_pinecone(pinecone_key, index_name)

# Step 4: If index is empty → create & upload vectors. Otherwise load existing.
vector_count = index.describe_index_stats().get("total_vector_count", 0)

if vector_count == 0:
    print("\n🔷 No vectors found in Pinecone → Uploading new embeddings...")
    vector_store = create_vector_store(chunked_documents, embeddings, index_name)
    print("✔ Upload completed.")
else:
    print("\n🔷 Existing vectors detected → Loading vector store without re-upload...")
    vector_store = load_existing_vector_store(index_name, embeddings)

print("\n🌟 Vector store is ready to use!")
