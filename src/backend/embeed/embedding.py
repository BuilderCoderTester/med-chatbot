import torch
from langchain_community.embeddings import HuggingFaceEmbeddings

def initialize_embeddings(
        model_name: str = "NeuML/pubmedbert-base-embeddings",
        use_gpu: bool = True
    ):
    
    # Configure device
    device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
    
    # Model kwargs → loaded on CPU/GPU
    model_kwargs = {
        "device": device
    }
    
    # Encode kwargs → affects performance + accuracy
    encode_kwargs = {
        "batch_size": 16,                # safe for most GPUs
        "normalize_embeddings": True     # MUST match Pinecone metric cosine
    }
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    print(f"Embeddings model loaded: {model_name}  |  Device: {device.upper()}")
    return embeddings
