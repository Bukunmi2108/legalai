# 🔬 CONTROLLED LEGAL RAG + FINE-TUNING EXPERIMENT

## ✅ Checklist

- [ ] 0.1 Choose ONE domain
- [ ] 0.2 Define tasks (freeze them)
- [ ] 1.1 Collect raw legal documents
- [ ] 1.2 Normalize documents
- [ ] 1.3 HARD SPLIT (critical)
- [ ] 2.1 Create gold questions from EVAL docs
- [ ] 2.2 Define evaluation rubric (freeze this)
- [ ] 3.1 Chunk corpus docs
- [ ] 3.2 Embed and index
- [ ] 3.3 Prompt (freeze it)
- [ ] 3.4 Run Baseline A
- [ ] 4.1 Build training pairs
- [ ] 4.2 LoRA fine-tuning
- [ ] 4.3 Run Baseline B
- [ ] 5.1 Reuse EVERYTHING
- [ ] 5.2 Run evaluation
- [ ] 6.1 Blind evaluation
- [ ] 6.2 Aggregate results
- [ ] 7.1 Interpretation
- [ ] 8.1 Write It Up

**Step-by-Step Execution Plan**

---

## PHASE 0 — Lock the Scope (Day 0)

**Do this once. Do not change it later.**

### 0.1 Choose ONE domain

Pick **one**:

* Contract law (recommended)
* Employment law
* Nigerian case law (Supreme Court only)

➡️ Smaller domain = cleaner signal.

### 0.2 Define tasks (freeze them)

Exactly 3 tasks:

1. Legal QA (doctrine)
2. Case-based reasoning
3. Citation fidelity

No more, no less.

---

## PHASE 1 — Data Preparation (Day 1–2)

### 1.1 Collect raw legal documents

Sources:

* Court judgments (PDF/HTML)
* Statutes
* Contracts

Target size:

* **300–1,000 documents**
* Quality > quantity

---

### 1.2 Normalize documents

Convert everything into:

```json
{
  "doc_id": "...",
  "title": "...",
  "jurisdiction": "...",
  "text": "clean legal text"
}
```

Rules:

* Remove headers/footers
* Preserve section numbers
* Preserve citations

---

### 1.3 HARD SPLIT (critical)

Split at **document level** (not chunks):

| Split  | %   | Used for        |
| ------ | --- | --------------- |
| Corpus | 70% | RAG retrieval   |
| Train  | 20% | Fine-tuning     |
| Eval   | 10% | Evaluation ONLY |

🚫 Eval docs must **never** appear in embeddings or training.

---

## PHASE 2 — Build Evaluation Set (Day 3)

### 2.1 Create gold questions from EVAL docs

For each eval document:

* 2–3 questions
* Answers must be **explicitly supported** by text

Example format:

```json
{
  "question": "...",
  "answer": "...",
  "citations": ["Doc X, Section 3"],
  "doc_id": "..."
}
```

Target:

* **100–150 total questions**

---

### 2.2 Define evaluation rubric (freeze this)

Each answer is scored on:

| Metric            | Scale               |
| ----------------- | ------------------- |
| Legal correctness | 0–2                 |
| Hallucination     | Yes / No            |
| Citation accuracy | Correct / Incorrect |
| Reasoning depth   | 0–2                 |

This is what makes it **research-grade**.

---

## PHASE 3 — RAG System (Baseline A) (Day 4)

### 3.1 Chunk corpus docs

* Chunk size: **500–700 tokens**
* Overlap: **10–15%**
* Preserve doc_id + section

---

### 3.2 Embed and index

* Embedding model: consistent across all experiments
* Vector store: FAISS / Chroma

Metadata to store:

* doc_id
* section
* jurisdiction

---

### 3.3 Prompt (freeze it)

Use the same prompt everywhere:

> “Answer the question using ONLY the provided legal context.
> Cite specific authorities.
> If the answer is not supported, say so.”

No changes later.

---

### 3.4 Run Baseline A

* Model: base model
* Retrieval: top-k = 5
* Temperature: 0.2

Save:

* Answer
* Retrieved chunks
* Token counts

---

## PHASE 4 — Fine-Tuning (Baseline B) (Day 5–6)

### 4.1 Build training pairs

From TRAIN split only:

```json
{
  "instruction": "Answer the legal question...",
  "input": "Legal context or question",
  "output": "Grounded legal answer with citation"
}
```

Target:

* **2k–5k samples** (enough for LoRA)

---

### 4.2 LoRA fine-tuning

* Base model same as RAG
* LoRA rank: 8–16
* Epochs: 2–3
* No retrieval

Save:

* Adapter weights
* Training config

---

### 4.3 Run Baseline B

* No RAG
* Same prompt
* Same eval questions

This tests **internalized knowledge only**.

---

## PHASE 5 — Fine-Tuned + RAG (Condition C) (Day 7)

### 5.1 Reuse EVERYTHING

* Same vector store
* Same prompt
* Same retrieval params

Only change:

* Model = fine-tuned model

---

### 5.2 Run evaluation

Log exactly same fields as A and B.

---

## PHASE 6 — Scoring & Analysis (Day 8)

### 6.1 Blind evaluation

You should **not know** which condition produced which answer while scoring.

Score:

* A vs B vs C
* Per-task breakdown

---

### 6.2 Aggregate results

Compute:

* Accuracy %
* Hallucination rate %
* Citation correctness %
* Avg reasoning score

---

## PHASE 7 — Interpretation (Day 9)

Answer explicitly:

* Where does RAG fail?
* Where does fine-tuning hallucinate?
* Does fine-tuning improve context usage?

This is where **research insight** comes in.

---

## PHASE 8 — Write It Up (Day 10)

Structure:

1. Problem
2. Methodology
3. Experimental controls
4. Results
5. Limitations
6. Future work

You now have:

* A legit experiment
* A writing sample
* A portfolio project
* Research credibility

---