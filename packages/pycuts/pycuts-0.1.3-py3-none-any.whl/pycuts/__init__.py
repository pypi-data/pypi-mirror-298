# pycuts/__init__.py
from .torch import (
    device, gpu, empty_cache, synchronize, device_count, manual_seed
)
from .huggingface_hub import (
    is_spaces, is_zero_gpu_space
)