"""
Large Language Model (LLM) interface module.

This module provides functionality for:
- Loading and configuring the LLM model
- Generating text responses from prompts
- Managing model parameters and settings
"""

import os

from llama_cpp import Llama

MODEL_PATH = os.getenv('MODEL_PATH', '../models/Phi-3-mini-4k-instruct-q4.gguf')

llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=6, n_gpu_layers=35)


def generate(prompt: str, max_tokens: int = 512) -> str:
    """
    Generate text response from the language model.

    Uses the loaded LLM to generate a response based on the input prompt
    with specified parameters for token length and output formatting.

    Args:
        prompt (str): The input prompt to generate a response for.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 512.

    Returns:
        str: Generated text response from the model.
    """
    output = llm(
        prompt,
        max_tokens=max_tokens,
        stop=['</s>'],
        echo=False,
        stream=False,  # Disable streaming, the response will be returned all at once
    )
    return output['choices'][0]['text'].strip()  # type: ignore
