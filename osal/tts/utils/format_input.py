

def format_prompt(prompt, voice, available_voices, default_voice):
    """Format prompt for Orpheus model with voice prefix and special tokens."""
    if voice not in available_voices:
        print(f"Warning: Voice '{voice}' not recognized. Using '{default_voice}' instead.")
        voice = default_voice

    # Format similar to how engine_class.py does it with special tokens
    formatted_prompt = f"{voice}: {prompt}"
    
    # Add special token markers for the LM Studio API
    special_start = "<|audio|>"  # Using the additional_special_token from config
    special_end = "<|eot_id|>"   # Using the eos_token from config
    
    return f"{special_start}{formatted_prompt}{special_end}"
