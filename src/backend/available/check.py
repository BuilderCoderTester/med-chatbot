import torch
def check_gpu_availability():
    """Check and print GPU availability."""
    if torch.cuda.is_available():
        print(f"GPU is available: {torch.cuda.get_device_name(0)}")
        print(f"Number of GPUs: {torch.cuda.device_count()}")
        print(f"CUDA Version: {torch.version.cuda}")
        return True
    else:
        print("No GPU available, using CPU")
        return False

