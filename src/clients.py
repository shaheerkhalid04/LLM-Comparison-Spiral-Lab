"""
Small wrapper that calls the OpenRouter API.

OpenRouter gives access to many different LLMs through one website, one
API key, and one request format (the same format as OpenAI's library).
Models whose ids end in ":free" cost nothing to use, which is perfect
for this assignment.

If the library is not installed, or the API key is missing, the function
raises a clear error that the main script catches and reports.
"""

import os


def call_openrouter(prompt, model):
    """Send the prompt to a model hosted on OpenRouter."""
    from openai import OpenAI

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. "
            "Copy .env.example to .env and paste in your key."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # Some free models "think" before answering, which also uses up
        # tokens. 2000 leaves plenty of room for a 200-word summary.
        max_tokens=2000,
    )
    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise RuntimeError("The model returned an empty reply. Try again.")
    return text


# A lookup table so the main script can pick the right function by name.
PROVIDERS = {
    "openrouter": call_openrouter,
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
