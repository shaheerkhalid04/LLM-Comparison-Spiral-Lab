"""
Small wrapper functions that call each LLM provider's API.

Each function takes a prompt string and returns the model's text reply.
They all look the same on the outside, so the main script does not need to
know the details of each provider.

If a provider's library is not installed, or the API key is missing, the
function raises a clear error that the main script catches and reports.
"""

import os


def call_openai(prompt, model):
    """Send the prompt to an OpenAI model (e.g. GPT)."""
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


def call_gemini(prompt, model):
    """Send the prompt to a Google Gemini model."""
    import google.generativeai as genai

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set.")

    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(prompt)
    return response.text.strip()


def call_anthropic(prompt, model):
    """Send the prompt to an Anthropic model (Claude)."""
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


# A lookup table so the main script can pick the right function by name.
PROVIDERS = {
    "openai": call_openai,
    "gemini": call_gemini,
    "anthropic": call_anthropic,
}


def get_summary(provider, model, prompt):
    """
    Pick the correct provider function and call it.

    Returns the summary text on success.
    Raises a RuntimeError with a readable message on failure.
    """
    if provider not in PROVIDERS:
        raise RuntimeError("Unknown provider: " + provider)
    return PROVIDERS[provider](prompt, model)
