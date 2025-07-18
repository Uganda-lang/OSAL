
from typing import TypedDict, NotRequired

class TTSOptions(TypedDict):
    max_tokens: NotRequired[int]
    """Maximum number of tokens to generate. Default: 2048"""
    temperature: NotRequired[float]
    """Temperature for top-p sampling. Default: 0.8"""
    top_p: NotRequired[float]
    """Top-p sampling. Default: 0.95"""
    top_k: NotRequired[int]
    """Top-k sampling. Default: 40"""
    min_p: NotRequired[float]
    """Minimum probability for top-p sampling. Default: 0.05"""
    pre_buffer_size: NotRequired[float]
    """Seconds of audio to generate before yielding the first chunk. Smoother audio streaming at the cost of higher time to wait for the first chunk."""
    voiqce_id: NotRequired[str]
    """Voice ID to use for TTS."""

