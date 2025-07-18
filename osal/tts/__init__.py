import numpy as np
import scipy.io.wavfile as wavfile
from typing import Generator, Optional, List, Tuple
from numpy.typing import NDArray

# Import the main class and helper types
from .orpheus_cpp import OrpheusCpp
from .utils import TTSOptions
# Import the static model data directly
from .models import MODELS_DICT

# This global variable will hold the initialized model instance.
_model_instance: Optional[OrpheusCpp] = None

__all__ = [
    "init",
    "speak",
    "stream_speak",
    "get_supported_languages",
    "get_available_voices",
    "get_default_male_voice",
    "get_default_female_voice",
    "OrpheusCpp",
]



def get_supported_languages() -> List[str]:
    """
    Returns a list of supported language codes.
    This function can be called before init().
    """
    return list(MODELS_DICT.keys())


def get_available_voices(lang: str) -> List[str]:
    """
    Returns a list of available voice IDs for a given language.
    This function can be called before init().

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
    This function can be called before init().

    Args:
        lang (str): The language code.
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
    This function can be called before init().

    Args:
        lang (str): The language code.
    """
    if lang not in MODELS_DICT:
        raise ValueError(
            f"Language '{lang}' is not supported. "
            f"Supported languages are: {get_supported_languages()}"
        )
    return MODELS_DICT[lang]["default_female_voice"]


def init(
    huggingface_token: str,
    lang: str = "en",
    n_gpu_layers: int = 0,
    n_threads: int = 0,
    verbose: bool = True,
):
    """
    Initializes the Orpheus TTS model and loads it into memory.
    This must be called once before using the speak() or stream_speak() functions.

    Args:
        huggingface_token (str): Your Hugging Face API token to download the model.
        lang (str, optional): The language model to load. Use get_supported_languages()
                              to see options. Defaults to "en".
        n_gpu_layers (int, optional): Number of model layers to offload to GPU. Defaults to 0.
        n_threads (int, optional): Number of CPU threads to use. Defaults to 0.
        verbose (bool, optional): Whether to enable verbose logging from llama.cpp. Defaults to True.
    """
    global _model_instance
    if _model_instance is not None:
        print("Warning: TTS model is already initialized. Re-initializing.")

    if lang not in get_supported_languages():
        raise ValueError(
            f"Language '{lang}' is not supported. "
            f"Please choose from: {get_supported_languages()}"
        )

    _model_instance = OrpheusCpp(
        huggingface_token=huggingface_token,
        lang=lang,
        n_gpu_layers=n_gpu_layers,
        n_threads=n_threads,
        verbose=verbose,
    )
    print(f"Orpheus TTS initialized successfully for language: '{lang}'.")


def _check_initialized():
    """Internal function to ensure the model is initialized."""
    if _model_instance is None:
        raise RuntimeError(
            "TTS model not initialized. Please call orpheus.init() before using this function."
        )


def speak(
    text: str,
    output_path: Optional[str] = None,
    voice_id: Optional[str] = None,
    temperature: float = 0.8,
    top_p: float = 0.95,
    top_k: int = 40,
    min_p: float = 0.05,
    max_tokens: int = 2048,
    pre_buffer_size: float = 1.5,
) -> Tuple[int, NDArray[np.int16]]:
    """
    Generates audio from text and returns it as a NumPy array.
    Requires model to be initialized with init().

    Args:
        text (str): The text to synthesize.
        output_path (Optional[str], optional): If provided, saves the audio to this .wav file path.
        voice_id (Optional[str], optional): The voice to use. If None, uses the default male voice
                                           for the initialized language.
        temperature (float, optional): Temperature for sampling. Defaults to 0.8.
        top_p (float, optional): Top-p sampling parameter. Defaults to 0.95
        top_k (int, optional): Top-k sampling parameter. Defaults to 40.
        min_p (float, optional): Minimum probability for top-p sampling. Defaults to 0
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 2048.
        pre_buffer_size (float, optional): Seconds of audio to generate before yielding the first chunk
    Returns:
        Tuple[int, NDArray[np.int16]]: A tuple containing the sample rate (24000) and the audio data.
    """
    _check_initialized()

    # If no voice is specified, use the default from the *initialized instance*. This is correct.
    effective_voice_id = voice_id or _model_instance.default_male_voice

    options: TTSOptions = {
        "voice_id": effective_voice_id,
        "temperature": temperature, "top_p": top_p, "top_k": top_k,
        "min_p": min_p, "max_tokens": max_tokens, "pre_buffer_size": pre_buffer_size,
    }

    sample_rate, audio_data = _model_instance.tts(text, options)

    if output_path:
        wavfile.write(output_path, sample_rate, audio_data.flatten())
        print(f"Audio saved to {output_path}")

    return sample_rate, audio_data

