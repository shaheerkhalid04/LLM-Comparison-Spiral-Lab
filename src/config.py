"""
Configuration for the LLM summarization comparison.

Keep all the "settings" of the project in one place so the rest of the code
stays simple. If you want to add or remove a model, this is the only file
you need to touch.
"""

# The prompt sent to every model. It MUST be identical for all models,
# otherwise the comparison would not be fair.
SHARED_PROMPT = (
    "Summarize the following document in a clear, well-structured way. "
    "Keep the summary concise (about 150-200 words). Only use information "
    "that is present in the document. Do not add outside facts.\n\n"
    "Document:\n"
    "{document_text}"
)

# The three (or more) models we compare.
# - "label"    : the friendly name shown in the report.
# - "provider" : which API client to use (see clients.py).
# - "model"    : the exact model id the provider expects.
#
# All three run through OpenRouter (openrouter.ai) on their free tier,
# so one free API key covers everything. Ids ending in ":free" cost
# nothing. Browse https://openrouter.ai/models?max_price=0 to swap in
# other free models.
MODELS = [
    {
        "label": "GPT-OSS",
        "provider": "openrouter",
        "model": "openai/gpt-oss-20b:free",
    },
    {
        "label": "Gemma",
        "provider": "openrouter",
        "model": "google/gemma-4-26b-a4b-it:free",
    },
    {
        "label": "Nemotron",
        "provider": "openrouter",
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
    },
    {
        "label": "Hunyuan",
        "provider": "openrouter",
        "model": "tencent/hy3:free",
    },
    {
        "label": "Cohere",
        "provider": "openrouter",
        "model": "cohere/north-mini-code:free",
    },
]

# The four metrics the assignment asks us to score each model on.
# Each is scored from 1 (poor) to 5 (excellent).
METRICS = [
    "Summary Quality",
    "Accuracy",
    "Conciseness",
    "Hallucinations",
]

# Where files live.
DOCUMENT_PATH = "documents/source_document.txt"
SUMMARIES_DIR = "outputs"
RESULTS_DIR = "results"
