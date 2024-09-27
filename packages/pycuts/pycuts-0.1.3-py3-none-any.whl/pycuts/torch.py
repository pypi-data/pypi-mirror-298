# https://raw.githubusercontent.com/dwancin/pycuts/main/pycuts/torch.py
import torch
from typing import Optional

def device() -> torch.device:
    """
    Returns the appropriate device (cuda, mps, or cpu).
    
    Returns:
        torch.device: The best available device.
    """
    return torch.device(
        "cuda" if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available()
        else "cpu"
    )

def gpu() -> bool:
    """
    Checks whether a GPU is available or not.
    
    Returns:
        bool: `True` if a GPU is available, `False` if only CPU is available.
    """
    current_device = device()
    return current_device.type in ["mps", "cuda"]

def empty_cache(device: Optional[torch.device] = None) -> None:
    """
    Clears the GPU memory to prevent out-of-memory errors.
    Args:
        device (torch.device, optional): The device to empty cache for. Defaults to current device.
    """
    device = device or device()
    if device.type == "cuda":
        torch.cuda.empty_cache()
    elif device.type == "mps":
        torch.mps.empty_cache()

def synchronize(device: Optional[torch.device] = None) -> None:
    """
    Waits for all kernels in all streams on the given device to complete.
    Args:
        device (torch.device, optional): The device to synchronize. Defaults to current device.
    """
    device = device or device()
    if device.type == "cuda":
        torch.cuda.synchronize()
    elif device.type == "mps":
        torch.mps.synchronize()

def device_count() -> int:
    """
    Returns the number of available devices.
    Returns:
        int: The number of devices available.
    """
    current_device = device()
    if current_device.type == "cuda":
        return torch.cuda.device_count()
    elif current_device.type == "mps":
        return 1  # Only one MPS device available on macOS
    else:
        return 1

def manual_seed(seed: int) -> None:
    """
    Sets the seed for generating random numbers for reproducible behavior.
    
    Args:
        seed (int): The desired seed value.
    
    Raises:
        ImportError: If random or numpy cannot be imported.
    """
    try:
        import random
        import numpy as np
    except ImportError as e:
        raise ImportError(f"Required module not found: {e.name}. Please ensure it is installed.") from e
    
    current_device = device()
    
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if current_device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
    elif current_device.type == "mps":
        torch.mps.manual_seed(seed)
