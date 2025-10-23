---
description: "There are only 6 fundamental ways to evaluate a RAG system. Here's how to do it."
comments: true
author:
  - jxnl
date: 2025-05-19
---

# There Are Only 6 RAG Evals

The world of RAG evaluation feels needlessly complex. Everyone's building frameworks, creating metrics, and generating dashboards that make you feel like you need a PhD just to know if your system is working.

<!-- more -->

But what if I told you there are only 6 fundamental ways to evaluate a RAG system?

Just math and symmetry.

## The Insight

RAG systems have three core components:

- A question (Q)
- Retrieved context (C)
- An answer (A)

That's it. Three variables.

!!! note "Exhaustive by Design"
The power of focusing on Question (Q), Context (C), and Answer (A) is that these three components, and their conditional relationships, cover _every_ possible aspect of RAG evaluation. There are no hidden variables.

If we look at this through the lens of conditional relationships — the quality of one component given another — we get exactly six possible relationships. No more, no less.

Think about it: when one thing breaks in your RAG system, it's always one of these relationships failing. This relates directly to what we've learned about the systematic approach to RAG improvement - identifying specific failure points rather than making vague statements about "making the AI better."

## The 6 Core Evaluation Metrics

Let's break down each relationship (I'll use the notation X|Y to mean "quality of X given Y"). Rather than treating all metrics equally, I'll organize them into three practical tiers based on implementation complexity and business impact - similar to how we think about the improvement flywheel for RAG products:

### Tier 1: Foundation Metrics (Before RAG Evaluation)

Before we even get to our six core metrics, we need to acknowledge the foundation of any retrieval system:

**Retrieval Precision & Recall**: These traditional information retrieval metrics measure how well your retriever finds relevant documents from the corpus. They're fast to compute, don't require LLMs, and provide quick feedback for retriever tuning.

This aligns perfectly with our approach to starting the flywheel with synthetic data - you need to establish baseline retrieval performance with clear, measurable metrics before moving to more complex evaluation techniques. These metrics serve as the leading indicators that predict future success, rather than lagging indicators that just tell you about past performance.

### Tier 2: Primary RAG Relationships

**1. Context Relevance (C|Q)**

- _Definition_: How well do the retrieved chunks address the question's information needs? This measures whether your retriever component is doing its job—finding passages that contain information relevant to answering the user's question.

- _Example (Good)_:

  - Question: "What are the health benefits of meditation?"
  - Context: "Regular meditation has been shown to reduce stress hormones like cortisol. A 2018 study in the Journal of Cognitive Enhancement found meditation improves attention and working memory."
  - _Reasoning_: Strong relevance. The context directly addresses multiple health benefits with specific details.

- _Example (Bad)_:
  - Question: "What are the health benefits of meditation?"
  - Context: "Meditation practices vary widely across different traditions. Mindfulness meditation, which originated in Buddhist practices, focuses on present-moment awareness, while transcendental meditation uses mantras to achieve deeper states of consciousness."
  - _Reasoning_: Low relevance. Despite being factually correct about meditation, this context discusses types and origins rather than any health benefits. The retriever has found topically related content but missed the specific information need.

!!! warning "Irrelevant Context Dooms Generation"
If your retriever pulls irrelevant context, your generator is doomed from the start. This is a common pitfall, reflecting "absence blindness" where teams obsess over generation quality while neglecting to ensure retrieval (C|Q) is even working correctly.

**2. Faithfulness/Groundedness (A|C)**

- _Definition_: To what extent does the answer restrict itself only to claims that can be verified from the retrieved context? This evaluates the generator's ability to avoid hallucinations.

- _Example (Good)_:

  - Context: "The Great Barrier Reef is the world's largest coral reef system."
  - Answer: "The Great Barrier Reef is the largest coral reef system in the world."
  - _Reasoning_: Perfect faithfulness. The answer only states what's in the context.

- _Example (Bad)_:

  - Context: "The Great Barrier Reef is the world's largest coral reef system. It stretches for over 2,300 kilometers along the coast of Queensland, Australia."
  - Answer: "The Great Barrier Reef, the world's largest coral reef system, stretches for over 2,300 kilometers along Australia's eastern coast and is home to about 10% of the world's fish species."
  - _Reasoning_: Mixed faithfulness. The first part is supported, but the claim about "10% of the world's fish species" isn't in the provided context. This subtle hallucination appears plausible and might be factually correct, but it's not grounded in the retrieved context.

- _Why It Matters_: Hallucination undermines trust. This is why we implement validation patterns, interactive citations, and chain-of-thought reasoning in our RAG applications - to catch errors before they reach users and build trust through transparency.

**3. Answer Relevance (A|Q)**

- _Definition_: How directly does the answer address the specific information need expressed in the question? This evaluates the end-to-end system performance.

- _Example (Good)_:

  - Question: "How does compound interest work in investing?"
  - Answer: "Compound interest works by adding the interest earned back to your principal investment, so that future interest is calculated on the new, larger amount."
  - _Reasoning_: High relevance. The answer directly explains the concept asked about.

- _Example (Bad)_:

  - Question: "How does compound interest work in investing?"
  - Answer: "Interest in investing can be simple or compound. Compound interest is more powerful than simple interest and is an important concept in finance. It's the reason why starting to invest early is so beneficial for long-term wealth building."
  - _Reasoning_: Low relevance. Despite being about compound interest, the answer doesn't actually explain the mechanism of how it works. It tells you it's important but fails to address the specific how question.

- _Why It Matters_: This is the ultimate user experience metric. It's also why we focus on building feedback mechanisms that specifically ask "Did we answer your question?" rather than vague "How did we do?" feedback prompts. Specific feedback aligned with this metric increases response rates dramatically.

### Tier 3: Advanced RAG Relationships

**4. Context Support Coverage (C|A)**

- _Definition_: Does the retrieved context contain all the information needed to fully support every claim in the answer? This measures whether the context is both sufficient and focused.

This metric connects directly to what we've learned about specialized retrievers and the query routing architecture. Different content types may require different retrieval approaches to ensure complete coverage. For instance, when answering questions about blueprints in construction projects, you might need both image retrieval and document retrieval working together.

**5. Question Answerability (Q|C)**

- _Definition_: Given the context provided, is it actually possible to formulate a satisfactory answer to the question? This evaluates whether the question is reasonable given the available information.

This relates to the strategic rejection pattern we've discussed. When a query can't be answered with the available context, the most honest response is to acknowledge this limitation. This builds trust through transparency rather than generating a hallucinated answer.

**6. Self-Containment (Q|A)**

- _Definition_: Can the original question be inferred from the answer alone? This measures whether the answer provides enough context to stand on its own.

This connects to our discussion of monologues and chain-of-thought approaches that make thinking visible. Answers that restate and address the core question directly create better user experiences, especially in asynchronous communication contexts.

## Implementing Tiered Evaluation in Practice

Based on recent academic research and practical experience, here's how to approach RAG evaluation with these metrics:

**Start with Tier 1**: Implement fast retrieval metrics for daily development

- Use precision, recall, MAP@K, and MRR@K to tune your retriever
- These don't require LLM evaluation and provide quick feedback cycles

This directly mirrors our approach of starting the improvement flywheel with synthetic data and focused evaluation metrics before moving to more complex approaches.

**Focus on Tier 2**: Implement the three primary RAG relationships

- These core metrics (C|Q, A|C, A|Q) directly assess how well your RAG system functions
- Most benchmarks prioritize these three metrics
- Use LLM-based evaluation for more nuanced assessment of these relationships

This aligns with our focus on building feedback mechanisms and quality-of-life improvements that enhance trust and transparency.

**Extend to Tier 3**: Add advanced metrics when you need deeper insights

- These metrics (C|A, Q|C, Q|A) connect technical performance to business outcomes
- Use them for monthly evaluations, major releases, and strategic decisions
- Different domains may require emphasis on different Tier 3 metrics (e.g., medical RAG needs stronger C|A)

This connects to our discussion of topic modeling and capability identification, recognizing that different query types may require different evaluation emphasis.

## LLM-as-Judge

Most modern RAG evaluations rely on LLMs as judges. This approach, while resource-intensive, provides the most nuanced assessment of our six core relationships.

!!! note "The Nuance of LLM Judges"
While resource-intensive, using LLMs as judges is currently the most effective method for capturing the subtle nuances in the six core RAG relationships. Traditional metrics often fall short in this complex assessment.

Several benchmarks, including RAGAs, ARES, and TruEra RAG Triad, now use LLM evaluation by default. While traditional metrics like BLEU, ROUGE, and BERTScore still have a place, only LLM-based evaluation can effectively capture the nuanced relationships in our framework.

This parallels our discussion about using LLMs to analyze feedback and identify patterns in user queries - leveraging AI to understand AI.

## Domain-Specific Evaluation

An interesting insight from the DomainRAG benchmark is that different domains may require different emphasis within our framework:

- Medical RAG systems need higher faithfulness scores (A|C)
- Customer service RAG demands better answer relevance (A|Q)
- Technical documentation RAG requires stronger question answerability (Q|C)

This reinforces what we've learned about topic modeling and segmentation - different query types need different capabilities, and our evaluation should reflect those priorities. It's why we segment questions not just by topic but by the capability required to answer them.

## Why This Framework Matters

When your RAG system fails, it fails along one of these dimensions. Every time.

- Answer seems wrong? Check faithfulness (A|C).
- Answer seems irrelevant? Check answer relevance (A|Q).
- Answer missing key info? Check context relevance (C|Q) or context support (C|A).

The beauty of this framework is that it's complete. There are no other relationships between Q, C, and A. We've covered every possible evaluation angle.

This systematic approach to diagnosing problems aligns perfectly with our product mindset for RAG - identifying specific failure points rather than making vague statements about "making the AI better."

## So What?

Next time you're debugging a RAG system, don't waste time on complexity theater. Focus on these six relationships organized in practical tiers. Fix the ones that are broken. Ignore the rest.

This framework complements our improvement flywheel perfectly - start with the basics, collect feedback on specific aspects, analyze that feedback to identify patterns, and make targeted improvements based on what you learn.

And if someone tries to sell you a RAG evaluation framework with 20 different metrics? Smile and ask which of the 6 core relationships they're actually measuring.

Because in RAG evaluation, as in RAG implementation, the systematic approach wins every time.

---

_What's your experience with RAG evaluation? Do you find yourself focusing on particular metrics more than others? Drop a comment below—I'd love to hear which of these 6 relationships causes you the most headaches._

## Want to learn more?

I also wrote a 6 week email course on RAG, where I cover everything in my consulting work. It's free and you can:

[Check out the free email course here](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }
