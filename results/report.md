# LLM Comparison - Document Summarization

## Document Used
"The Rise of Renewable Energy" — the sample article included with the
project (documents/source_document.txt). It is a short explainer of about
230 words / 3 paragraphs covering what renewable energy is, how solar,
wind, and hydropower work, and the policy drivers and challenges of the
transition.

## Models Compared
All five models were called through OpenRouter's free tier with the
exact same prompt on 2026-07-20:

- **GPT-OSS** — openai/gpt-oss-20b:free
- **Gemma** — google/gemma-4-26b-a4b-it:free
- **Nemotron** — nvidia/nemotron-3-super-120b-a12b:free
- **Hunyuan** — tencent/hy3:free
- **Cohere** — cohere/north-mini-code:free

## Prompt Used
```
Summarize the following document in a clear, well-structured way. Keep the summary concise (about 150-200 words). Only use information that is present in the document. Do not add outside facts.

Document:
{document_text}
```

## Summaries
Each model's summary is saved in the `outputs/` folder.

## Evaluation
See `comparison_table.md` for the scores.

### Notes per metric
- Summary Quality: Gemma produced the cleanest result: a title, three
  short paragraphs, easy to read. Cohere was similarly well structured
  but one sentence is awkwardly garbled (see Accuracy). Hunyuan was
  clear and compact, though it appended a "(147 words)" word count the
  prompt never asked for and has no title. Nemotron was well written
  but delivered one dense paragraph with no structure, so it is harder
  to scan. GPT-OSS had good structure (headings and bullet points) but
  its text contained corrupted words ("sunमुlight", "upgrate
  electricity", "governmentsimus"), which badly hurts readability.
- Accuracy: Gemma, Nemotron, and Hunyuan represented the source
  faithfully; every claim in their summaries can be traced back to a
  sentence in the document. Cohere distorted one claim: "fossil fuels,
  which emit carbon dioxide after millions of years of formation"
  merges two separate facts from the source (they take millions of
  years to form; they release CO2 when burned) into a confusing
  statement. GPT-OSS slightly reworded some claims (e.g. attributing
  falling costs to "technological advances", which the document does
  not say).
- Conciseness: All five stayed within or near the requested 150-200
  words and dropped no key information. Hunyuan was the tightest (147
  words), Gemma (~170) and Cohere (~180) comfortably in range, Nemotron
  (~190) at the upper end; GPT-OSS spent a few words on its added
  hydropower remark.
- Hallucinations: Gemma, Nemotron, Hunyuan, and Cohere added nothing
  that is not in the document. GPT-OSS invented a claim: "Hydropower
  relies on sufficient water flow but is limited by suitable sites" —
  plausible, but the source never discusses hydropower's limitations,
  so this violates the "do not add outside facts" instruction.

## Conclusion
Gemma performed best overall. It was the only model that combined
faithful content, clean structure, and the requested length with zero
added facts, making it the most trustworthy summarizer in this test.
Nemotron and Hunyuan tied for second: both were completely faithful,
but Nemotron lacks structure (one dense paragraph) and Hunyuan added a
needless word count and no title. Cohere was well organized but garbled
one factual sentence. GPT-OSS finished last: despite good formatting
instincts, it produced corrupted words and one invented claim about
hydropower — exactly the failure modes this evaluation is designed to
catch.
