"""
Main script for the LLM summarization comparison.

What it does, step by step:
  1. Reads the source document.
  2. Builds one shared prompt.
  3. Sends that same prompt to each model.
  4. Saves every model's summary to its own file.
  5. Writes a comparison table (with the scores left blank for you to fill in
     after reading the summaries) plus a starter report.

Run it from the project root with:
    python src/run_comparison.py
"""

import os

from dotenv import load_dotenv

import config
import clients

# Read the API key from the .env file in the project root, so you don't
# have to set environment variables by hand.
load_dotenv()


def read_document(path):
    """Read the source document text from a file."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            "Could not find the document at '" + path + "'. "
            "Put your article/paper text there first."
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def build_prompt(document_text):
    """Insert the document into the shared prompt template."""
    return config.SHARED_PROMPT.format(document_text=document_text)


def save_summary(label, summary_text):
    """Save one model's summary to outputs/<label>_summary.txt."""
    os.makedirs(config.SUMMARIES_DIR, exist_ok=True)
    filename = os.path.join(config.SUMMARIES_DIR, label + "_summary.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary_text)
    return filename


def run_all_models(prompt):
    """
    Send the prompt to every model in the config.

    Returns a dictionary: { model_label: summary_or_error_message }.
    """
    summaries = {}
    for entry in config.MODELS:
        label = entry["label"]
        print("Running " + label + " ...")
        try:
            summary = clients.get_summary(
                entry["provider"], entry["model"], prompt
            )
            summaries[label] = summary
            path = save_summary(label, summary)
            print("  saved -> " + path)
        except Exception as error:
            # We keep going even if one model fails, so a missing key for
            # one provider does not stop the whole run.
            message = "ERROR: " + str(error)
            summaries[label] = message
            print("  " + message)
    return summaries


def write_comparison_table():
    """
    Write an empty comparison table (Markdown) for the four metrics.

    Scores are left blank on purpose: you fill them in yourself after
    reading each summary. That keeps the evaluation honest.
    """
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    path = os.path.join(config.RESULTS_DIR, "comparison_table.md")

    # Don't overwrite a table you already filled in. Delete the file if
    # you want a fresh blank one.
    if os.path.exists(path):
        print("  (keeping existing " + path + ")")
        return path

    header = "| Model | " + " | ".join(config.METRICS) + " | Overall Score |"
    divider = "| --- " * (len(config.METRICS) + 2) + "|"

    rows = []
    for entry in config.MODELS:
        blanks = " | ".join([" "] * (len(config.METRICS) + 1))
        rows.append("| " + entry["label"] + " | " + blanks + " |")

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Comparison Table\n\n")
        f.write("Score each metric from 1 (poor) to 5 (excellent).\n")
        f.write("For 'Hallucinations', a higher score means fewer made-up "
                "facts.\n\n")
        f.write(header + "\n")
        f.write(divider + "\n")
        f.write("\n".join(rows) + "\n")
    return path


def write_report_scaffold():
    """Write a starter report file for observations and the conclusion."""
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    path = os.path.join(config.RESULTS_DIR, "report.md")

    # Don't overwrite a report you already wrote. Delete the file if you
    # want a fresh scaffold.
    if os.path.exists(path):
        print("  (keeping existing " + path + ")")
        return path

    lines = [
        "# LLM Comparison - Document Summarization",
        "",
        "## Document Used",
        "Describe the document you summarized (title, source, length).",
        "",
        "## Prompt Used",
        "```",
        config.SHARED_PROMPT,
        "```",
        "",
        "## Summaries",
        "Each model's summary is saved in the `outputs/` folder.",
        "",
        "## Evaluation",
        "See `comparison_table.md` for the scores.",
        "",
        "### Notes per metric",
        "- Summary Quality: ",
        "- Accuracy: ",
        "- Conciseness: ",
        "- Hallucinations: ",
        "",
        "## Conclusion",
        "Which model performed best, and why? Write 3-4 sentences here.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def main():
    """Tie all the steps together."""
    document_text = read_document(config.DOCUMENT_PATH)
    prompt = build_prompt(document_text)

    # Save the exact prompt used, so it is part of the deliverables.
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    with open(os.path.join(config.RESULTS_DIR, "prompt_used.txt"),
              "w", encoding="utf-8") as f:
        f.write(prompt)

    run_all_models(prompt)
    table_path = write_comparison_table()
    report_path = write_report_scaffold()

    print("")
    print("Done.")
    print("Comparison table: " + table_path)
    print("Report scaffold:  " + report_path)
    print("Now read the summaries in 'outputs/' and fill in the scores.")


if __name__ == "__main__":
    main()
