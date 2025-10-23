---
title: "Why Glean Builds Custom Embedding Models for Every Customer"
speaker: Manav, Glean
cohort: 3
description: How Glean achieves 20% search performance improvements through customer-specific embedding models, unified data architecture, and smart feedback loops that most enterprise AI companies are missing.
tags: [enterprise search, embedding models, fine-tuning, RAG optimization, Glean, custom models]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Why Glean Builds Custom Embedding Models for Every Customer

I hosted Manav from Glean for a guest lecture on enterprise search and fine-tuning embedding models. This session revealed a surprisingly underutilized approach that can dramatically improve RAG system performance - building custom embedding models for each customer rather than using generic solutions.

<!-- more -->

[▶️ Learn Glean's Custom Model Strategy](https://maven.com/p/1ea9c9){: .md-button .md-button--primary}

## What is Glean and why does their approach to enterprise search matter?

Glean has built a comprehensive Work AI platform that unifies enterprise data across various applications (Google Drive, GitHub, Jira, Confluence) into a single system. Their flagship product, the Glean Assistant, leverages this unified data model to generate relevant answers to user questions and automate workflows.

The foundation of their system is semantic search capability, which Manav emphasized is absolutely critical for enterprise AI success:

> "Search quality matters - you can't have a good RAG system, you can't have a good overall enterprise AI product unless you have good search."

This makes intuitive sense - without retrieving the right context from your enterprise data, even the best LLMs will produce hallucinations and incorrect information.

**Key Takeaway:** Search quality is the foundation of enterprise AI success. Without effective retrieval from enterprise data, even the most advanced LLMs will generate hallucinations and provide incorrect information.

## What makes enterprise data uniquely challenging?

Unlike internet data, which has a significant "head problem" where most searches target popular websites or common information sources, enterprise data is far more heterogeneous and doesn't fit neatly into a single mold. Manav explained:

> "Enterprise data is very different than internet data... You have your basic document data sources like Google Drive, Google Docs, Confluence, Notion... But you're also working with a bunch of different types of applications, like Slack, which is a messaging platform. You have meetings, which doesn't really meet the standard concept of what a document is. You have GitHub and GitLab... They all behave in slightly different ways."

This diversity requires a robust, generalized unified data model that can handle the nuances of different data types while maintaining security and privacy. Additionally, company-specific language (project names, initiatives, internal terminology) creates another layer of complexity that generic models struggle with.

**Key Takeaway:** Enterprise search is fundamentally different from web search because of data heterogeneity and company-specific language. A unified data model that can handle diverse data types while preserving security is essential for effective enterprise AI.

## Why fine-tune embedding models for each customer?

One of the most fascinating aspects of Glean's approach is that they build custom embedding models for each customer. While many companies focus on using large, general-purpose embedding models, Glean has found that smaller, fine-tuned models often perform better for specific enterprise contexts.

### Glean's Custom Model Process:

1. **Start with a high-performance base model** (typically BERT-based)
2. **Perform continued pre-training** on company data using masked language modeling
3. **Convert the language model** into an embedding model through various training techniques
4. **Continuously update the model** as the company evolves

The results are impressive - after six months, they typically see a **20% improvement in search performance** just from learning from user feedback and adapting to company changes.

Manav emphasized the power of smaller, specialized models:

> "When you're thinking about building really performant enterprise AI... you want to also think about using smaller embedding models when you can, because small embedding models when fine-tuned to the domain and the specific task you have in hand can give you a lot better performance compared to just using large LLMs."

**Key Takeaway:** Smaller, fine-tuned embedding models often outperform large general-purpose models for enterprise contexts. Glean achieves 20% search performance improvements through continuous model adaptation to company-specific language and user feedback.

## How do they generate high-quality training data?

Creating effective training data for fine-tuning embedding models is challenging, especially with enterprise privacy constraints. Glean uses several creative approaches:

### Training Data Sources:

- **Title-body pairs:** Mapping document titles to passages from the document body
- **Anchor data:** Using documents that reference other documents to create relevance pairs
- **Co-access data:** Identifying documents accessed together by users in short time periods
- **Public datasets:** Incorporating high-quality public datasets like MS MARCO
- **Synthetic data:** Using LLMs to create question-answer pairs for documents

### Application-Specific Intelligence

What's most impressive is their attention to application-specific nuances. For example, with Slack data, they don't just treat each message as a document. Instead, they create "conversation documents" from threads or messages within a short timespan, then use the first message as a title and the rest as the body.

This understanding of how different applications work leads to much higher quality training data than generic approaches.

**Key Takeaway:** Generating high-quality training data requires understanding the nuances of different enterprise applications. Creative approaches like title-body pairs, anchor data, co-access signals, and synthetic data generation can provide valuable training signals even with privacy constraints.

## How do they learn from user feedback?

Once users start interacting with their products, Glean incorporates those signals to further improve their models:

### Search Product Feedback:

- **Query-click pairs:** Direct signals of relevance from user interactions

### RAG Assistant Feedback (More Challenging):

For RAG-only settings like their Assistant product, where users don't explicitly click on documents, they face a more challenging problem:

- **Upvote/downvote systems** (though these tend to get sparse usage)
- **Citation tracking** when users click on citations to read more about a topic
- **Interaction pattern monitoring** to infer relevance from various user behaviors

Manav candidly acknowledged the difficulty:

> "This is like a pretty hard open question"

Their approach of combining multiple weak signals seems pragmatic given the inherent challenge of getting explicit feedback signals for generative AI products.

**Key Takeaway:** Learning from user feedback in RAG systems is challenging, especially for generative interfaces. Combining multiple weak signals (upvotes, citation clicks, interaction patterns) provides a more robust approach than relying on any single feedback mechanism.

## How do they evaluate embedding model quality?

Evaluating embedding models in enterprise settings is particularly challenging because:

- **Privacy constraints:** You can't access customer data directly
- **Unique models:** Each customer has a different model
- **Complex systems:** End-to-end RAG evaluation involves many moving parts

### Glean's "Unit Test" Approach

Glean's solution is to build "unit tests" for their models - targeted evaluations for specific behaviors they want their models to exhibit. For example, they test how well models understand paraphrases of the same query.

This approach allows them to:

- **Set performance targets** for each customer's model
- **Identify underperforming models** before customers experience issues
- **Focus optimization efforts** on specific areas

Manav emphasized the importance of component-level optimization:

> "If you want to really make good tangible progress day by day, isolating and optimizing individual components is always going to be much more scalable than trying to improve everything all together all at once."

**Key Takeaway:** Evaluating embedding models in enterprise settings requires targeted "unit tests" that isolate specific behaviors. This component-level approach enables scalable optimization and prevents customer-facing issues.

## What role does traditional search play alongside embeddings?

Despite all the focus on embedding models, Manav emphasized that traditional search techniques remain crucial:

> "You don't want to over-index on semanticness or LLM-based scoring as the only thing that your search system should use... you can get a lot more bang for your buck by not using any semanticness at all to answer most questions."

### The 60-70% Rule

Manav estimated that for **60-70% of enterprise search queries**, basic lexical search with recency signals works perfectly well. Semantic search becomes more important for complex queries, particularly in agent-based systems.

This aligns with practical experience - getting 80% of the way there with full-text search and then adding semantic search as the cherry on top is often the most effective approach.

**Key Takeaway:** Don't abandon traditional search techniques in pursuit of embedding-based approaches. A hybrid system that leverages both lexical and semantic search, along with signals like recency and authority, will deliver the best results for enterprise search.

## How do they handle document relevance over time?

One interesting question addressed how Glean handles outdated documents that have been superseded by newer information. Their approach centers around a concept they call "authoritativeness," which incorporates:

### Authoritativeness Factors:

- **Recency:** Newer documents are generally more relevant
- **Reference patterns:** Documents that continue to be linked to or accessed remain authoritative
- **User satisfaction signals:** Documents that consistently satisfy user queries maintain relevance

### Real-World Example

A document containing WiFi password information might be old but still highly relevant if people continue to reference it when answering related questions.

This multi-faceted approach to document authority is more sophisticated than simply prioritizing recent content, which would miss important evergreen documents.

**Key Takeaway:** Document relevance over time requires a multi-faceted "authoritativeness" approach that balances recency with reference patterns and user satisfaction signals, rather than simply prioritizing the newest content.

## Final thoughts on building enterprise search systems

Manav concluded with several key insights for building effective enterprise search systems:

### Core Principles:

- **Unified data model** is critical for handling heterogeneous enterprise data
- **Company-specific language** matters tremendously for search quality
- **Fine-tuned smaller models** often outperform generic large models for specific tasks
- **User feedback learning**, though challenging, provides invaluable signals
- **Targeted "unit tests"** enable scalable model quality assessment
- **Traditional search techniques** remain powerful and shouldn't be discarded

### The Pragmatic Approach

Glean's approach is refreshingly pragmatic. They've learned that the path to high-quality enterprise search isn't just about using the latest, largest models, but about understanding the unique characteristics of enterprise data and building systems that address those specific challenges.

The emphasis on company-specific language models is particularly noteworthy - this is an area where many companies struggle when they try to apply generic embedding models to their unique terminology and document structures.

**Key Takeaway:** Successful enterprise search requires a pragmatic approach that combines custom embedding models, unified data architecture, hybrid search techniques, and continuous learning from user feedback rather than relying solely on off-the-shelf solutions.

## --8<--

"snippets/enrollment-button.md"
--8<--

---
