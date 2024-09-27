# pycuts/huggingface.py
import os

def is_spaces() -> bool:
    """
    Checks if the current script is running on a Hugging Face Space.
    
    Returns:
        bool: True if running on Hugging Face Space, False otherwise.
    """
    return os.getenv("SPACE_ID") == "true"

def is_zero_gpu_space() -> bool:
    """
    Checks if the Hugging Face Space runs on Zero GPU.
    
    Returns:
        bool: True if running Zero GPU, False otherwise.
    """
    return os.getenv("SPACES_ZERO_GPU") == "true"
