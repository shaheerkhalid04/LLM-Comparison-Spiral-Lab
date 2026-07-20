# Project Notes

This project compares how different LLMs summarize the same document, for a
learning assignment. What still needs doing:

1. Confirm `requirements.txt` installs cleanly, and fix any model IDs in
   `src/config.py` that have been renamed or deprecated by the providers.
2. Run `python src/run_comparison.py` once API keys are set (keys go in a
   local `.env` file, which is gitignored; never commit real keys).
3. After the real summaries land in `outputs/`, fill in
   `results/comparison_table.md` and `results/report.md`.

Notes:
- The prompt in `config.py` must stay identical across all models; that is a
  hard requirement of the assignment (fair comparison).
- Do not invent summaries or scores. The scores must come from reading the
  models' actual outputs.
- Keep the code beginner-friendly and readable.

See README.md for full setup and the deliverables checklist.
