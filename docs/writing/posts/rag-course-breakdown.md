---
title: Systematically Improving RAG Applications
description: A Detailed, No-Nonsense Guide to Building Better Retrieval-Augmented Generation
authors:
  - jxnl
date: 2025-01-24
comments: true
---

# How to Systematically Improve RAG Applications

Retrieval-Augmented Generation (RAG) is a simple, powerful idea: attach a large language model (LLM) to external data, and harness better, domain-specific outputs. Yet behind that simplicity lurks a maze of hidden pitfalls: no metrics, no data instrumentation, not even clarity about _what exactly we’re trying to improve_.

In this mega-long post, I’ll lay out everything I know about **systematically improving RAG apps**—from fundamental retrieval metrics, to segmentation and classification, to structured extraction, multimodality, fine-tuned embeddings, query routing, and closing the loop with real user feedback. It’s the end-to-end blueprint for building and iterating a RAG system that actually works in production.

I’ve spent years consulting on applied AI—spanning recommendation systems, spam detection, generative search, and RAG. That includes building ML pipelines for large-scale recommendation frameworks, doing vision-based detection, curation of specialized datasets, and more. In short, I’ve seen many “AI fails” up close. Over time, I’ve realized that gluing an LLM to your data is just the first step. The real magic is how you measure, iterate, and keep your system from sliding backward.

We’ll break everything down in a systematic, user-centric way. If you’re tired of random prompt hacks and single-number “accuracy” illusions, you’re in the right place.

<!-- more -->

## 1. What Is RAG and Why Does Everyone Want It?

RAG stands for **Retrieval-Augmented Generation**. Think of it as your LLM plus an external knowledge source—documents, images, structured data, or anything else—so you’re not just relying on the model’s trained parameters. Instead, you fetch relevant data _on the fly_, embed it into prompts, and let the LLM do a specialized final answer.

Why does everyone get excited about RAG?

- **Domain Specificity**  
  You can keep a smaller (cheaper) LLM but still get highly relevant outputs—like enterprise policy documents or niche scientific knowledge—because you feed it external context.
- **Up-to-Date Info**  
  LLMs get stale. If your external data store is updated daily, you can deliver fresh results for user queries (e.g. news, real-time financial statements).
- **Interpretability**  
  You know _exactly_ which document chunk answered a query, which helps reduce hallucinations and fosters user trust.

### RAG in a Nutshell

1. **User Query** → 2. **Retrieve** relevant chunks from an external knowledge base → 3. **Fuse** them into a prompt → 4. **Generate** an answer with the LLM.

That’s it, conceptually. But the devil’s in the details. You can’t just throw stuff into the black box—**you have to measure** how well your retrieval pipeline is working.

---

## 2. Common Pitfalls: Absence Bias and Intervention Bias

I see two forms of bias kill most RAG systems:

### 2.1 Absence Bias

This is ignoring what you _can’t_ see.

- In RAG, that often means ignoring the retrieval step. Everyone sees the final “AI” output, so they keep fiddling with prompts or switching from GPT-3.5 to GPT-4. But if your retrieval is wrong—pulling the wrong chunk entirely—no model version will fix that.
- Folks might not measure retrieval success at all. They’ll say, “The answer is off, let’s tweak chain-of-thought.” But the root cause might be that the chunk or snippet is incomplete, or not even being retrieved in the first place.

### 2.2 Intervention Bias

This is the urge to do _anything_ so you feel in control.

- Maybe you see a new prompt-engineering trick on Twitter, and you jam it into your code.
- Or you discover some fancy re-ranking architecture, and you plug it in without measuring if your plain re-ranker was already fine.
- The result is a Franken-system, with 80 half-tested solutions layered on top of each other. Tech debt soars, you can’t debug which piece is failing, and your system is brittle.

**Solution**: Resist the hype. The best approach is to start from real data, measure carefully, do simple experiments, and only keep what actually helps.

---

## 3. The Baseline: Retrieval Metrics & Synthetic Data

### 3.1 Why Evaluate Retrieval First?

If your system can’t _find_ the relevant snippet in the first place, everything else collapses. LLM outputs become hallucinations. So we always measure retrieval with classical **precision** and **recall**—particularly recall, because missing the key snippet is lethal.

- **Precision**: Of all returned snippets, how many are actually relevant?
- **Recall**: Of all relevant snippets, how many did we return?

In most RAG contexts, recall is the bigger headache. You usually can’t answer a question if you never retrieve the right chunk.

### 3.2 Synthetic Data to Jumpstart

**What if you have no user data yet?**

- You can’t measure recall if you don’t know which chunk is correct.
- That’s where _synthetic data_ helps. You take your knowledge base—maybe a document, a PDF, or table—and you ask an LLM: “Generate 5 questions that can be answered by each chunk.”
- You now have question→chunk pairs. Evaluate whether your system returns that chunk for each question. That’s your recall.

> _Tip_: This dataset can be simplistic (the LLM often paraphrases text), but it’s enough for a first pass. Then, as you get real user traffic or real user questions, you blend them in for a more robust dataset.

### 3.3 Evaluate, Inspect, Iterate

Armed with synthetic data, you do:

1. **Index** your documents (maybe in a vector DB).
2. **Generate** queries that map to known chunks.
3. **Check** how many times you actually retrieve the correct chunk.
4. **Log** the result in a spreadsheet or your favorite logging tool.

If your recall is 50%, that means half the time you’re missing the relevant chunk entirely. No advanced prompt can fix that. You must investigate chunk sizing, embeddings, or re-ranking next.

---

## 4. Segmentation & Classification: Finding Your Failure Modes

### 4.1 Overall Metrics Can Lie

You see a recall of 70% and think, “Not bad.” But that might average across many easy queries. The truly important queries (like multi-hop or date-filter questions) might have 5% recall. You won’t see that if you never break your dataset into categories.

Hence, **segmentation**. We group queries by topic, user type, complexity, or whatever matters for your business. Then we measure retrieval metrics _per segment_.

### 4.2 How to Segment

- **Topic**: “sales questions,” “technical questions,” “pricing questions,” etc.
- **Complexity**: “simple single-hop” vs. “multi-hop or comparison-based.”
- **User role**: “new users vs. experienced users,” “executives vs. engineers.”
- Or do a quick LLM-based clustering: feed your queries to a clustering algorithm (like k-means or an LLM-based topic labeling) to see emergent groups.

### 4.3 Inventory vs. Capability

Once you see a segment is failing, ask: “Is the problem **inventory** or **capability**?”

- **Inventory** means the data simply isn’t there. Maybe you’re missing the entire subfolder of docs, or you haven’t ingested the relevant column in your DB.
- **Capability** means the data is there, but you can’t surface it. You might need better searching, advanced filtering, or new metadata.

_Example:_ Searching “which user last edited file X”—that’s a capability question. If that metadata isn’t in your system, your LLM can’t just guess.

---

## 5. Structured Extraction & Multimodality

### 5.1 From Plain Text to Structured Data

So you suspect that some queries fail because it’s not enough to treat everything as lumps of text. For instance:

- **Dates, authors, or statuses** might be crucial filters.
- The user might say, “Show me the 2022 budget vs. 2023 budget,” but your text chunk is a giant PDF with no date-labeled metadata.

**Structured extraction** means you parse the doc, figure out relevant fields or metadata, and store them in a more query-friendly way. This might be a separate DB column or a sidecar index. Then your search can do a straightforward filter like `(doc_year=2023)`.

### 5.2 Handling Tables

PDFs, Excel sheets, or CSV files can be disasters if you just chunk them as text:

- You lose row/column context.
- In RAG, a user may ask: “What’s the year-over-year growth in column F?”

If you can store that table as an actual table, the retrieval process becomes more direct. Even a “text-to-SQL” approach might help, so the system queries an actual database. Don’t hack your LLM to parse it if you can keep it structured in the first place.

### 5.3 Images and Blueprints

Many real-world RAG apps face blueprint or diagram queries. For example, in construction or engineering: “Show me the blueprint for floor 3 and label the exit doors.” _Pure text search can’t help._

- One approach: run an image captioner or bounding-box model to generate text descriptions of an image, then index that text.
- Another approach: create specialized indexes that store bounding boxes or object detection results.

**Lesson**: Don’t rely on the LLM alone to interpret an image on the fly. Pre-extract the data you need, verify it, measure recall again.

---

## 6. Query Routing & Specialized Indices

### 6.1 The Problem: We Now Have Multiple “Searchers”

We have:

- A standard text index (vector DB).
- A specialized table query system (SQL).
- An image-based approach.
- Possibly a lexical index for exact code references or short numeric IDs.

So how do we pick which one to call? If a user says, “Compare the 2021 and 2022 product shipments,” do we hit the text index or the table search?

**Query routing** is the answer.

### 6.2 Defining Tools

Think of each index or search method as a “tool.” Then you have a simple classification step:

> “Which tool or set of tools do we need for this query?”

For large language models, you can define something like a function call with a name, arguments, and usage examples. The LLM picks which function to call. We measure “tool recall”: the fraction of queries that _should_ call a certain tool but do.

### 6.3 Precision vs. Recall in Tool Selection

Too many calls can slow your pipeline. So you’ll want to watch:

- **Precision**: how often the system calls a tool it _shouldn’t_ call.
- **Recall**: how often it calls the right tool for the right query.

It’s almost the same retrieval logic, but at the “index selection” level. Having a confusion matrix for tool calls is super helpful. If you see that 90% of blueprint queries end up going to the text index incorrectly, you know you need better training examples or a short docstring clarifying: “Use the blueprint search if you see mention of diagrams, floors, or building references.”

---

## 7. Fine-Tuning Embeddings & Re-Rankers

### 7.1 Off-the-Shelf vs. Custom

Out-of-the-box embeddings (OpenAI, Cohere, etc.) might be generic. They’re trained to cluster text in a broad sense, but your domain might be specialized. For example, if you do legal or medical, generic embeddings might group terms incorrectly or miss nuance.

**Fine-tuning** means you gather a dataset of query→relevant chunk pairs (plus negative chunks that are not relevant) and train an embedding model or re-ranker to separate positives from negatives in vector space.

### 7.2 Collecting Training Data

- **Synthetic**: The “question→chunk” pairs you generated early on can become training data.
- **User Feedback**: If you show the user which chunk your system used, and they either confirm or reject it, that’s gold.
- **Triplets**: In contrastive learning, you typically have (query, positive chunk, negative chunk). The model learns to push the positive chunk closer and the negative chunk farther.

### 7.3 Gains from Fine-Tuning

You can see a 10-30% recall boost just by ensuring your embedding space aligns with how _you_ define “relevance.” This drastically reduces “time wasted” on advanced prompt engineering that tries to fix a retrieval mismatch.

### 7.4 Re-Rankers

Instead of (or in addition to) fine-tuning a bi-encoder (embedding model), you might fine-tune a cross-encoder or re-ranker that scores each candidate chunk directly. Re-rankers can be slower but often yield higher precision. Typically, you do a quick vector search, then run re-ranking on the top K results.

---

## 8. Closing the Loop: Feedback, Streaming & UX

### 8.1 Collecting User Feedback

None of these improvements happen if you have no feedback. If your UI just spits out an answer with no user engagement, you’re blind. Make it easy for users to:

- **Thumbs Up/Down** the answer.
- **Highlight** which snippet is wrong or missing.
- **Edit** or correct the final text if you’re drafting an email or doc.

Even subtle changes—like bigger thumbs-up/down buttons—multiply the feedback you get, which you feed back into your training sets for embeddings or re-rankers.

### 8.2 Streaming & Interstitials

Long queries or multi-step calls might mean you have 2-10 seconds of latency. That’s an eternity in user experience.

- **Streaming partial tokens** gives the user something to look at. It feels faster.
- **Show your steps** or an interstitial message, e.g. “Searching for relevant documents… Reading them… Summarizing…”
- Even a skeleton screen or a progress bar lowers user impatience significantly.

### 8.3 Chain-of-Thought

People talk about chain-of-thought prompting—a fancy term for letting the LLM reason step by step. Don’t just do it blindly. _Measure_ if it helps your correctness. Often, writing down intermediate reasoning in the prompt can boost accuracy, but can also hamper performance if used incorrectly. For complex queries, chain-of-thought is a powerful approach, especially if you:

1. Summarize relevant instructions from your doc.
2. Summarize relevant passages.
3. Then produce the final answer.

This ensures you don’t skip vital details and provides a natural “monologue” approach. You can even show or hide this from the user—some let you expand the chain-of-thought if curious.

### 8.4 Post-Validation

You can run a final validation step that checks your output for errors or certain constraints:

- If you need to ensure a link is valid, do a quick GET request to confirm it returns `200 OK`.
- If you require the LLM to never reveal personal data, parse the output with a quick script that looks for email addresses or phone numbers.

When it fails these validations, you automatically do a second pass or show a disclaimer. That keeps your system from shipping nonsense, bridging the gap to near-zero hallucinations for critical fields.

---

## 9. Conclusion: The Continuous Flywheel

### 9.1 Recap

We covered:

1. **RAG Basics**—LLM + external data.
2. **Absence & Intervention Bias**—the twin plagues of ignoring retrieval or chasing every new method.
3. **Evaluation**—synthetic data and recall metrics to measure if you’re retrieving the right chunk.
4. **Segmentation**—detect where you fail specifically, not just in broad averages.
5. **Structured Extraction & Multimodality**—extract table columns, handle images with captioning, etc.
6. **Routing**—call the right specialized index or function.
7. **Fine-Tuning**—collect user feedback to refine your embeddings or re-rankers for domain-specific performance.
8. **Product Feedback & UX**—deploy user feedback loops, streaming, chain-of-thought, plus final validations.

### 9.2 From Here to Infinity

A RAG system isn’t “done” after these steps. It’s an ongoing cycle:

1. **Ship** a minimal version with basic retrieval.
2. **Log** user interactions, watch recall.
3. **Discover** a failing segment—maybe new data types, new user queries, or a brand-new domain.
4. **Add** structured extraction or specialized routing.
5. **Train** an embedding or re-ranker to handle that segment better.
6. **Collect** more user feedback.
7. **Repeat** indefinitely, with the system continuously improving.

This flywheel turns your RAG setup from a static prototype into a living product. The more data you gather, the better your retrieval, routing, and generation get—assuming you measure systematically and don’t chase random solutions.

### 9.3 Final Thought

People see RAG as “LLM plus chunk text.” That’s the superficial part. The real advantage is that it’s **measurable**—and measurability kills guesswork. Instead of random hype or endless prompt tinkering, you systematically track your retrieval, refine your segmentation, handle specialized data, pick the best index, and incorporate user feedback. That’s how you turn a quick POC into a robust, lasting solution.

---

## Thanks for Reading

I hope this has clarified the methodical, data-driven path to building a world-class RAG system. Stay sharp—**absence bias** and **intervention bias** are always around the corner. Measure everything, refine your pipeline step by step, and you’ll watch your system’s performance rise.

If you enjoyed this post, you can also check out [improvingrag.com](https://improvingrag.com) a free guide that tries to capture much of what we teach in my [maven course](https://maven.com/applied-llms/rag-playbook).

## Want to learn more?

I also wrote a 6 week email course on RAG, where I cover everything in my consulting work. It's free and you can:

[Check out the free email course here](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }
