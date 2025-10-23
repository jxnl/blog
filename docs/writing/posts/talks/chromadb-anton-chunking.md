---
title: "Text Chunking Strategies for RAG Applications"
speaker: Anton
cohort: 3
description: "Technical session with Anton from ChromaDB on text chunking fundamentals, evaluation methods, and practical tips for improving retrieval performance"
tags:
  [
    text chunking,
    ChromaDB,
    retrieval performance,
    semantic chunking,
    heuristic chunking,
    evaluation,
  ]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Text Chunking - Anton (ChromaDB)

I hosted a special session with Anton from ChromaDB to discuss their latest technical research on text chunking for RAG applications. This session covers the fundamentals of chunking strategies, evaluation methods, and practical tips for improving retrieval performance in your AI systems.

<!-- more -->

## What is chunking and why is it important for RAG systems?

Chunking is the process of splitting documents into smaller components to enable effective retrieval of relevant information. Despite what many believe, chunking remains critical even as LLM context windows grow larger.

The fundamental purpose of chunking is to find the relevant text for a given query among all the divisions we've created from our documents. This becomes especially important when the information needed to answer a query spans multiple documents.

There are several compelling reasons why chunking matters regardless of context window size:

1. Embedding model limitations - While LLM context windows are growing, embedding models typically have fixed input sizes and will silently truncate oversized inputs
2. Inference efficiency - You're paying per token, so retrieving only relevant information reduces costs
3. Information accuracy - Effective chunking eliminates distractors that could confuse the model
4. Retrieval performance - Proper chunking significantly improves your system's ability to find all relevant information

**_Key Takeaway:_** Chunking will remain important regardless of how large context windows become because it addresses fundamental challenges in retrieval efficiency, accuracy, and cost management.

## What approaches exist for text chunking?

There are two broad categories of chunking approaches that are currently being used:

Heuristic approaches rely on separator characters (like newlines, question marks, periods) to divide documents based on their existing structure. The most widely used implementation is the recursive character text splitter, which uses a hierarchy of splitting characters to subdivide documents into pieces not exceeding a specified maximum length.

These methods generally produce good results with clean documents but become brittle when dealing with unusual formatting or special characters. They require significant preprocessing and cleaning.

Semantic approaches are more experimental but promising. These use embedding or language models to identify semantic boundaries in documents - points where the topic changes. This approach avoids the brittleness of heuristics by focusing on meaning rather than characters.

What's particularly interesting is that you can use the same embedding model for both chunking and retrieval, potentially finding an embedding-optimal chunking strategy. Since embeddings are relatively cheap, this approach is becoming more viable.

**_Key Takeaway:_** While heuristic approaches like recursive character text splitters are most common today, semantic chunking methods that identify natural topic boundaries show promise for more robust performance across diverse document types.

## Does chunking strategy actually matter for performance?

According to Anton's research, chunking strategy matters tremendously. Their technical report demonstrates significant performance variations based solely on chunking approach, even when using the same embedding model and retrieval system.

They discovered two fundamental rules of thumb that exist in tension with each other:

1. Fill the embedding model's context window as much as possible - Strategies that produce very short chunks tend to yield noisy retrieval results
2. Don't group unrelated information together - Embedding models struggle to summarize chunks containing contradictory or differing information

The most important insight, however, is that you must always examine your data. Many default chunking strategies produce chunks that are far too short because the delimiter characters are in the wrong order or are the wrong characters entirely.

By looking at your actual chunks, you can develop intuition about how your chunking strategy is working for your specific use case. This is critical because there's likely no universal "best" chunking strategy - the optimal approach depends on your data and task.

**_Key Takeaway:_** There's no one-size-fits-all chunking strategy. The best approach depends on your specific data and task, which is why examining your actual chunks is essential for diagnosing retrieval problems.

## How should we evaluate chunking strategies?

When evaluating chunking strategies, focus on the retriever itself rather than the generative output. This differs from traditional information retrieval benchmarks in several important ways:

Recall is the single most important metric. Modern models are increasingly good at ignoring irrelevant information, but they cannot complete a task if you haven't retrieved all the relevant information in the first place.

You should measure recall at the passage level rather than the document level. Traditional IR benchmarks focus on whole document retrieval, but in RAG applications, we care about retrieving specific relevant passages, not just any part of a relevant document.

Ranking metrics like NDCG (which consider the order of retrieved documents) are less relevant for RAG applications. As long as the information is available somewhere in the context window, the model can usually extract what it needs regardless of position.

The ChromaDB team has released code for their generative benchmark, which can help evaluate chunking strategies against your specific data.

**_Key Takeaway:_** Focus on passage-level recall rather than document-level metrics or ranking-sensitive measures. The model can handle irrelevant information, but it can't work with information that wasn't retrieved.

## What practical advice can improve our chunking implementation?

The most emphatic advice from Anton was: "Always, always, always look at your data." This point was stressed repeatedly throughout the presentation.

Many retrieval problems stem from poor chunking that isn't apparent until you actually examine the chunks being produced. Default settings in popular libraries often produce surprisingly poor results for specific datasets.

Retrieval is not a general system - it's dependent on your specific task and data. This means your evaluation needs to be based on the types of queries you expect to see in your application, not generic benchmarks.

While better tooling is being developed to help with this process, in the meantime, the best approach is to:

1. Generate chunks using your chosen strategy
2. Manually examine those chunks to ensure they make semantic sense
3. Test with queries representative of your actual use case
4. Measure passage-level recall to evaluate performance

This approach acknowledges that we're in an interesting era of software development where AI application builders are being forced to learn machine learning best practices that have evolved over decades.

**_Key Takeaway:_** No amount of sophisticated algorithms can compensate for not understanding your data. Examining your chunks and evaluating them against representative queries is the most reliable path to improving retrieval performance.

**Final thoughts on chunking for RAG applications**
The fundamental tension in chunking is between maximizing the use of the embedding model's context window and avoiding the grouping of unrelated information. Finding the right balance requires understanding your specific data and use case.

While semantic chunking approaches show promise, even the most basic heuristic methods can perform well if properly configured for your data. The defaults, however, are rarely optimal.

As Anton emphasized, retrieval is not a general system but a task-specific one. Your evaluation should reflect the queries your application will actually encounter rather than generic benchmarks.

The ChromaDB team is developing better tooling to help with this process, but in the meantime, the most reliable approach is to manually examine your chunks and measure passage-level recall against representative queries.

## By focusing on these fundamentals rather than blindly applying frameworks or following defaults, you can significantly improve the performance of your RAG applications and deliver better results to your users.

--8<--
"snippets/enrollment-button.md"
--8<--

---
