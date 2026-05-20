# legalai — Controlled RAG-vs-Fine-Tuning Experiment

A frozen-protocol experimental comparison of **retrieval-augmented generation** vs **LoRA fine-tuning** on a single legal-domain task (contract law).

The experiment is designed to produce an apples-to-apples comparison: same eval set, same prompt template, same generator, same judging rubric. The only thing that varies is whether the system retrieves over a corpus or uses a fine-tuned model.

## Experimental design (frozen)

| Dimension | Choice |
|---|---|
| **Domain** | Contract law |
| **Tasks** | Legal QA (doctrine), Case-based reasoning, Citation fidelity |
| **Corpus split** | 70% RAG corpus / 20% fine-tune train / 10% eval (document-level, never overlapping) |
| **Eval set** | 2–3 gold questions per eval doc, each answer explicitly supported by source text |
| **Baselines** | A: RAG over corpus · B: LoRA-fine-tuned model · (control: vanilla LLM) |
| **Evaluation** | Blind LLM-as-judge with a frozen rubric |

The full protocol lives in [`rag_vs_finetuning/plan.md`](rag_vs_finetuning/plan.md).

## Why frozen-protocol matters

When you change the eval set, prompt template, or generator between RAG and fine-tuning runs, you lose the ability to attribute performance differences to the technique. Most public RAG-vs-fine-tuning comparisons drift on at least one of these dimensions.

This experiment is structured so the only deliberate variable is the **retrieval-vs-parameters** mechanism for injecting knowledge.

## Status

- [x] Domain + task selection locked
- [x] Document collection, normalization, hard split
- [x] Chunking, embedding, indexing pipeline (Chroma / FAISS)
- [x] Retrieval baseline plumbing
- [ ] Gold question set construction
- [ ] Evaluation rubric freeze
- [ ] Baseline A (RAG) full eval
- [ ] LoRA training pair construction
- [ ] Baseline B (fine-tune) training + eval
- [ ] Blind LLM-as-judge run
- [ ] Aggregate results + write-up

WIP. Updates land on `main`.

## Stack

- Python 3.12
- LangChain (`langchain`, `langchain-community`, `langchain-google-genai`, `langchain-ollama`)
- FAISS (CPU) for vector indexing
- FlashRank for reranking
- pandas, openpyxl for data wrangling
- `uv` for environment management

## Repo layout

```
rag_vs_finetuning/
  plan.md              # frozen experimental protocol (read this first)
  …                    # data, scripts, eval harness (in progress)
pyproject.toml
.env.example
```

## Why I built it

I work on production legal-AI evaluation professionally. Most days the question isn't "does RAG work" — it's "for *this* task, does retrieval beat fine-tuning, and by how much, and with what failure modes." This repo is a clean, frozen-protocol attempt to answer that for contract law specifically.
