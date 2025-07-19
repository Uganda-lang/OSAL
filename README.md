**OSAL** This is an extension api for the ease access of the models we've developed. All the models can be accessed on the [huggingface hub](https://huggingface.co/USOAL)

## Features

-   **High-Quality Synthesis**: Generates natural-sounding speech.
-   **Multi-Lingual Support**: Create and manage multiple TTS models for different languages simultaneously in the same application.
-   **High-Performance**: Fast C++ backend with multi-threading support.
-   **GPU Acceleration**: Offload model layers to the GPU for even faster performance.
-   **Offline Inference**: After the initial model download, no internet connection is required.

## Prerequisites

To download the required TTS models, you need a **Hugging Face Hub API Token**.

1.  If you don't have one, create a Hugging Face account [here](https://huggingface.co/join).
2.  Navigate to your account settings and find the "Access Tokens" page, or go directly to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
3.  Create a new token with at least `read` permissions.

## Installation

You can install Orpheus TTS via pip:

```bash
git clone https://github.com/Uganda-lang/OSAL.git

cd OSAL
```

## Quick Start: Multiple Language Instances

We recommend storing your token as an environment variable for security.

```bash
export HUGGING_FACE_TOKEN="hf_YourTokenGoesHere"
```

Now, you can run the following Python code to create both English and Luganda synthesizers:

```python
import os
from osal import tts

# 1. Get Hugging Face Token ---
hf_token = os.environ.get("HUGGING_FACE_TOKEN")
if not hf_token:
    raise ValueError("Hugging Face token not found. Please set the HUGGING_FACE_TOKEN environment variable.")

# 2. Create TTS Instances for Different Languages ---
# This will download the models on the first run.
print("Initializing English TTS model...")
tts_en = tts.OrpheusCpp(huggingface_token=hf_token, lang="en")

# Other languages 
print("\nInitializing Luganda TTS model with GPU acceleration...")
tts_lug = tts.OrpheusCpp(
    huggingface_token=hf_token,
    lang="lug",
    n_gpu_layers=99 # Offload all possible layers to GPU
)



# 3. Synthesize Speech with the Correct Instance ---
# Synthesize English text
text_en = "Hello from the English model."
print(f"Synthesizing English: '{text_en}'")
sample_rate_en, audio_data_en = tts_en.tts(text=text_en)
tts.save_wav("output_en.wav", sample_rate_en, audio_data_en)


# Synthesize Luganda text using the default female voice for that language
text_lug = "Mukulike okuva mu katambi ka Luganda." # "Welcome from the Luganda model."
female_voice_lug = tts.get_default_female_voice("lug")
print(f"Synthesizing Luganda: '{text_lug}'")
sample_rate_lug, audio_data_lug = tts_lug.tts(
    text=text_lug,
    options={"voice_id": female_voice_lug, "temperature": 0.7}
)
tts.save_wav("output_lug.wav", sample_rate_lug, audio_data_lug)

print("\nSynthesis complete for both languages.")
```

## API Reference

### The `OrpheusCpp` Class

This is the main class for text-to-speech synthesis. You create an instance of this class for each language model you want to use.

#### `tts.OrpheusCpp()`
The constructor initializes and loads a specific language model.

```python
tts_instance = tts.OrpheusCpp(
    huggingface_token: str,
    lang: str = "en",
    n_gpu_layers: int = 0,
    n_threads: int = 0,
    verbose: bool = True
)
```

-   **`huggingface_token`**: Your Hugging Face API token.
-   **`lang`**: The language model to load. See `get_supported_languages()`. Defaults to `"en"`.
-   **`n_gpu_layers`**: Number of model layers to offload to the GPU. Set to a high number (e.g., `99`) to offload all possible layers. Requires a compatible GPU and drivers.
-   **`n_threads`**: Number of CPU threads to use for inference. `0` uses the default.

#### `tts_instance.tts()`
Generates audio from text using the loaded model.

```python
tts_instance.tts(
    text: str,
    options: Optional[Dict] = None
) -> Tuple[int, NDArray[np.int16]]
```

-   **`text`**: The input text to synthesize.
-   **`options`**: A dictionary containing sampling parameters:
    -   `voice_id` (str): The voice to use. If not provided, uses the model's default male voice. See `get_available_voices()`.
    -   `temperature` (float): Sampling temperature (e.g., `0.8`).
    -   `top_p` (float): Top-p sampling nucleus (e.g., `0.95`).
    -   `top_k` (int): Top-k sampling (e.g., `40`).
    -   And other advanced parameters.

**Returns:** A tuple `(sample_rate, audio_data)`. `sample_rate` is 24000. `audio_data` is a 1D NumPy array of 16-bit integers.

**Example:**
```python
# Create an English model instance
tts_en = tts.OrpheusCpp(huggingface_token=hf_token, lang="en")

# Synthesize with custom options
custom_options = {
    "voice_id": tts.get_default_female_voice("en"),
    "temperature": 0.75,
    "top_p": 0.9,
}
sample_rate, audio_data = tts_en.tts(
    text="This is a test with a female voice and custom sampling parameters.",
    options=custom_options
)

# Use the convenience function to save the output
tts.save_wav("custom_output.wav", sample_rate, audio_data)
```

---

### Utility Functions

These stateless helper functions can be called at any time, even before creating a model instance.

#### `tts.get_supported_languages()`
Returns a list of supported language codes.
```python
print(tts.get_supported_languages())
# Output: ['en', 'lug', ..]
```

#### `tts.get_available_voices()`
Returns a list of available voice IDs for a given language.
```python
print(tts.get_available_voices("en"))
```

#### `tts.get_default_male_voice()`
Returns the default male voice ID for a given language.

#### `tts.get_default_female_voice()`
Returns the default female voice ID for a given language.

#### `tts.save_wav()`
A convenience function to save audio data to a `.wav` file.
```python
tts.save_wav("output.wav", sample_rate, audio_data)
```
