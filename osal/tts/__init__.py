import numpy as np
import scipy.io.wavfile as wavfile
from typing import Generator, Optional, List, Tuple
from numpy.typing import NDArray

from .orpheus_cpp import OrpheusCpp
from .utils import TTSOptions
from .models import MODELS_DICT

__all__ = [
    "OrpheusCpp",
    "get_supported_languages",
    "get_available_voices",
    "get_default_male_voice",
    "get_default_female_voice",
    "save_wav"
]


def get_supported_languages() -> List[str]:
    """
    Returns a list of supported language codes.
    This function can be called before creating a model instance.
    """
    return list(MODELS_DICT.keys())


def get_available_voices(lang: str) -> List[str]:
    """
    Returns a list of available voice IDs for a given language.
    This function can be called before creating a model instance.

    Args:
        lang (str): The language code (e.g., "en", "lug").

    Returns:
        List[str]: A list of voice IDs.

    Raises:
        ValueError: If the language is not supported.
    """
    if lang not in MODELS_DICT:
        raise ValueError(
            f"Language '{lang}' is not supported. "
            f"Supported languages are: {get_supported_languages()}"
        )
    return MODELS_DICT[lang]["voices"]


def get_default_male_voice(lang: str) -> str:
    """
    Returns the default male voice ID for a given language.
    This function can be called before creating a model instance.
    """
    if lang not in MODELS_DICT:
        raise ValueError(
            f"Language '{lang}' is not supported. "
            f"Supported languages are: {get_supported_languages()}"
        )
    return MODELS_DICT[lang]["default_male_voice"]


def get_default_female_voice(lang: str) -> str:
    """
    Returns the default female voice ID for a given language.
    This function can be called before creating a model instance.
    """
    if lang not in MODELS_DICT:
        raise ValueError(
            f"Language '{lang}' is not supported. "
            f"Supported languages are: {get_supported_languages()}"
        )
    return MODELS_DICT[lang]["default_female_voice"]


def save_wav(output_path: str, sample_rate: int, audio_data: NDArray[np.int16]):
    """
    A convenience function to save audio data to a .wav file.

    Args:
        output_path (str): The path to save the .wav file.
        sample_rate (int): The audio sample rate (e.g., 24000).
        audio_data (NDArray[np.int16]): The audio data numpy array.
    """
    wavfile.write(output_path, sample_rate, audio_data.flatten())
    print(f"Audio saved to {output_path}")