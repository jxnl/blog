---
title: Systematically Improving RAG Applications Speaker Series
description: Collection of talks, lightning lessons, and presentations from the Systematically Improving RAG Applications series
date: 2024-12-01
---

# Systematically Improving RAG Applications Speaker Series

This section contains talks and presentations from [the Systematically Improving RAG Applications series](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK), featuring insights from industry experts and practitioners. Each talk provides specific learning outcomes, actionable techniques, and often surprising insights that challenge conventional RAG wisdom.

---

!!! success "📚 Get the Complete Course - 20% Off"
This content is from the [Systematically Improving RAG Applications](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK) course on Maven.

    **Readers can enroll for 20% off with code: `EBOOK`**

    Join 500+ engineers who've transformed their RAG systems from demos to production-ready applications.

    [Enroll in the RAG Playbook Course - 20% Off](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button .md-button--primary }

---

## Talks by Chapter

### Chapter 1: Foundation and Evaluation

Establishing evaluation frameworks and building feedback systems.

**[Building Feedback Systems for AI Products](zapier-vitor-evals.md)** - Vitor (Zapier)  
Simple UX changes increased feedback collection from 10 to 40+ submissions per day (4x improvement). Game-changing insight: specific feedback questions like "Did this run do what you expected?" dramatically outperform generic "How did we do?" prompts. The team discovered they were missing positive feedback entirely due to poor collection mechanisms.

**[Text Chunking Strategies](chromadb-anton-chunking.md)** - Anton (ChromaDB)  
Why chunking remains critical even with infinite context windows due to embedding model limitations and retrieval performance. Surprising discovery: default chunking strategies in popular libraries often produce terrible results for specific datasets. Essential practice: always manually examine your chunks.

**[Understanding Embedding Performance through Generative Evals](embedding-performance-generative-evals-kelly-hong.md)** - Kelly Hong  
Generative benchmarking for creating custom evaluation sets from your own data. Surprising finding: model rankings on custom benchmarks often contradict MTEB rankings, showing that public benchmark performance doesn't guarantee real-world success. Method: filter document chunks for relevance → generate realistic queries with context and examples → evaluate retrieval performance.

### Chapter 2: Training and Fine-Tuning

Creating custom embedding models and fine-tuning for specific domains.

**[Enterprise Search and Fine-tuning Embedding Models](glean-manav.md)** - Manav (Glean)  
Custom embedding models for each customer achieve 20% performance improvements over 6 months through continuous learning. Counter-intuitive insight: smaller, fine-tuned models often outperform larger general-purpose models for company-specific terminology. Each customer gets their own model that learns from user feedback.

**[Fine-tuning Re-rankers and Embedding Models for Better RAG Performance](fine-tuning-rerankers-embeddings-ayush-lancedb.md)** - Ayush (LanceDB)  
Re-rankers provide 12-20% retrieval improvement with minimal latency penalty, making them "low-hanging fruit" for RAG optimization. Even small 6M parameter models show significant improvements. ColBERT architecture offers effective middle ground between bi-encoders and cross-encoders.

### Chapter 3: Production and Monitoring

Deployment strategies and production monitoring for RAG systems.

**[Online Evals and Production Monitoring](online-evals-production-monitoring-ben-sidhant.md)** - Ben & Sidhant  
Trellis framework for managing AI systems with millions of users. Critical discovery: traditional error monitoring (like Sentry) doesn't work for AI since there's no exception when models produce bad outputs. Their approach: discretize infinite outputs → prioritize by impact → recursively refine. Key insight: "vibe checks" often beat complex automated evaluation.

**[RAG Anti-patterns in the Wild](rag-antipatterns-skylar-payne.md)** - Skylar Payne  
90% of teams adding complexity to RAG systems see worse performance when properly evaluated. Major discovery: silent failures in document processing can eliminate 20%+ of corpus without detection. Golden rule: teams who iterate fastest on data examination consistently outperform those focused on algorithmic sophistication.

**[Domain Experts: The Lever for Vertical AI](chris-lovejoy-domain-expert-vertical-ai.md)** - Chris Lovejoy (Anterior)  
How to make LLMs work in specialized industries: build domain‑expert review loops that generate failure‑mode datasets, prioritize fixes by impact, and dynamically augment prompts with expert knowledge. Trust requires transparent production metrics, secure data handling, and defenses against LLM‑specific threats.

### Chapter 4: Query Analysis and Data Organization

Understanding user queries and routing them effectively.

**[Query Routing for RAG Systems](query-routing-anton.md)** - Anton (ChromaDB)  
Why the "big pile of records" approach reduces recall due to approximate nearest neighbor algorithms. When filtering large indexes, compute budget is wasted on irrelevant nodes. Solution: separate indexes per user/data source often outperform filtered large indexes because filtering inherently reduces recall.

### Chapter 5: Specialized Retrieval Systems

Building specialized capabilities for different content types and use cases.

#### Coding Agents

**[Autonomous Coding Agents w/ Nik Pash @ Cline](rag-is-dead-cline-nik.md)** - Nik Pash (Cline)  
Why leading coding agent companies are abandoning embedding-based RAG in favor of direct code exploration. Surprising insight: even massive enterprise codebases work better with agentic exploration than vector search. Key finding: "narrative integrity" - agents need coherent thought processes, not disconnected code snippets from similarity search.

**[Agentic RAG](colin-rag-agents.md)** - Colin Flaherty  
Surprising findings from top SWE-Bench performance: simple tools like grep and find outperformed sophisticated embedding models due to agent persistence and course-correction capabilities. Key recommendation: expose existing retrieval systems as tools to agents rather than replacing them.

#### Document Processing and Multi-Modal

**[Better RAG Through Better Data](reducto-docs-adit.md)** - Adit (Reducto)  
Hybrid computer vision + VLM pipelines outperform pure approaches for document parsing. Critical finding: even 1-2 degree document skews can dramatically impact extraction quality. Essential insight: invest heavily in domain-specific evaluation rather than generic benchmarks.

**[Encoder Stacking and Multi-Modal Retrieval](superlinked-encoder-stacking.md)** - Daniel (Superlinked)  
LLMs as "pilots that see the world as strings" fundamentally can't understand numerical relationships. Solution: mixture of specialized encoders for different data types (text, numerical, location, graph) rather than forcing everything through text embeddings. This approach eliminates over-reliance on re-ranking.

#### Search Technologies

**[Lexical Search in RAG Applications](john-lexical-search.md)** - John Berryman  
Why semantic search struggles with exact matching, product IDs, and specialized terminology. Lexical search provides efficient simultaneous filtering and rich metadata that helps LLMs make better decisions. Recommended approach: use lexical search for filtering, semantic search for understanding meaning.

### Chapter 6: Advanced Topics and Innovation

Cutting-edge approaches and innovative techniques.

**[RAG is Dead - Long Live Agentic Code Exploration](rag-is-dead-cline-nik.md)** - Nik Pash (Cline)

Why leading coding agent companies are abandoning embedding-based RAG in favor of direct code exploration. Surprising insight: even massive enterprise codebases work better with agentic exploration than vector search. Key finding: "narrative integrity" - agents need coherent thought processes, not disconnected code snippets from similarity search.

**[Semantic Search Over the Web with Exa](semantic-search-exa-will-bryk.md)** - Will Bryk (Exa)  
Why AI systems need fundamentally different search engines than humans. Vision for "perfect search" includes test-time compute where complex queries may take hours or days. Prediction: search market will fragment into specialized providers rather than one-size-fits-all solutions.

**[RAG Without APIs: Browser-Based Retrieval](rag-without-apis-browser-michael-struwig.md)** - Michael (OpenBB)  
Browser-as-data-layer for secure financial data access without traditional API redistribution. Innovation: stateless agent protocol enables remote function execution in browser, solving compliance and security issues. Philosophy: anything humans can do, AI must be able to do.

## Overarching Themes

**Most Critical Learning:** Data quality examination beats algorithmic sophistication - teams that iterate fastest on understanding their data consistently build better RAG systems

**Most Underutilized Technique:** Fine-tuning embeddings and re-rankers - both are more accessible and impactful than most teams realize

**Biggest Gap:** Most teams focus on model selection and prompting but underinvest in document processing, evaluation frameworks, and understanding their specific data distribution

The series reveals that successful RAG systems require a portfolio of techniques rather than silver bullets, with data understanding and systematic evaluation being the foundational capabilities that enable everything else.

---

For more information about the broader curriculum, see the [main index](../index.md).

## Stay Updated

Get access to exclusive discounts and our free 6-day email course on RAG improvement:

[Subscribe for Free 6-Day Email Course](https://improvingrag.com/){ .md-button }
