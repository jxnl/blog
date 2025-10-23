---
title: The RAG Mistakes That Are Killing Your AI (Skylar Payne)
speaker: Skylar Payne
cohort: 3
description: Common RAG anti-patterns across different industries and practical advice for improving AI systems through better data handling, retrieval, and evaluation practices.
tags: [RAG, antipatterns, data quality, evaluation, best practices]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# The RAG Mistakes That Are Killing Your AI (Skylar Payne)

I hosted a Lightning Lesson with Skylar Payne, an experienced AI practitioner who's worked at companies like Google and LinkedIn over the past decade. Skylar shared valuable insights on common RAG (Retrieval-Augmented Generation) anti-patterns he's observed across multiple client engagements, providing practical advice for improving AI systems through better data handling, retrieval, and evaluation practices.

<!-- more -->

[▶️ Avoid These Critical RAG Mistakes](https://maven.com/p/35585d){: .md-button .md-button--primary}

## What are the most common RAG anti-patterns across different industries?

Skylar has worked with various use cases including customer support knowledge bases, medical advice chatbots, financial news summarization, academic research assistants, and e-commerce product comparison tools. Across these diverse applications, he's consistently observed similar problems that prevent RAG systems from performing optimally.

The fundamental issue that keeps appearing is insufficient attention to data quality and evaluation. As Skylar emphasized, "Look at your data. You really need to start from your user, understand what they want, work backwards. And then you need to look at your data at every step." This approach of continuous data inspection throughout the pipeline is critical for success.

When breaking down the RAG pipeline into its component parts, problems can emerge at each stage:

1. Data Collection and Curation
1. Extraction and Enrichment
1. Indexing and Storage
1. Retrieval
1. Re-ranking
1. Generation

Each of these stages presents unique challenges that can significantly impact the overall performance of your RAG system.

**_Key Takeaway:_** The teams who can iterate quickly through the cycle of examining data, getting ideas, and adapting their system are invariably the ones who succeed. This process of continuous improvement based on data insights is the foundation of effective RAG implementation.

## What problems occur during data collection and curation?

Two major issues frequently arise during the initial data collection phase:

Documents with varied encodings or formats often cause silent failures. In one medical chatbot project, 21% of the document corpus was silently dropped because the system assumed all documents were UTF-8 when many were actually Latin-1 encoded. This kind of silent failure is particularly dangerous because your index shrinks without your knowledge, leading to degraded answers and lost user trust.

Irrelevant document sets create "ticking time bombs" in your index. When documents that aren't relevant to any potential user query are included, they're just waiting to be incorrectly retrieved. In a financial news summarization project, including general macroeconomic trend articles when users only cared about specific industry updates led to strange, unhelpful summaries.

To address these issues, Skylar recommends:

- Understanding what formats and encodings your documents use
- Using robust parsers and off-the-shelf libraries when possible
- Monitoring failures rather than silently dropping documents
- Tracking document counts at each pipeline stage
- Curating document sets to include only relevant content
- Using metadata tagging to filter documents for specific query types
- Analyzing query logs to refine filters over time

**_Key Takeaway:_** Silent failures in data processing can dramatically reduce the quality of your RAG system without any obvious errors. Implement robust monitoring and be intentional about which documents you include in your index.

## What challenges exist in extraction and enrichment?

Information extraction from complex documents presents significant challenges, particularly with PDFs and tables. For an academic research assistant project, extracting tables from research papers was critical but difficult with standard tools.

Many off-the-shelf PDF extraction tools perform poorly on table extraction, leading to missing or malformed data. This affects the quality of information that can be retrieved and presented to users.

The solution approach includes:

- Using specialized tools designed specifically for the artifacts you need to extract
- Validating extracted chunks to ensure they make sense and meet accuracy requirements
- Looking at your data throughout the process to catch extraction errors

Another common issue is chunking documents into pieces that are too small. Many implementations default to tiny chunks (around 200 characters) because they're copying tutorials or using AI coding assistants that reference outdated approaches designed for models with limited context windows.

In an e-commerce product comparison project, spec sheets were split into such small snippets that no single chunk contained complete information, causing the model to hallucinate answers for about 13% of queries. Modern models can often handle much larger chunks, sometimes eliminating the need for chunking entirely.

Similarly, keeping low-value chunks like copyright footers or boilerplate text creates noise in your retrieval system. These chunks rarely contain useful information but can be retrieved if they happen to match a query, crowding out more relevant content.

**_Key Takeaway:_** Don't blindly follow chunking strategies from tutorials - examine your specific use case to determine the optimal chunk size, and be sure to filter out low-value content that adds noise to your retrieval system.

## What issues arise in indexing and storage?

Naive embedding usage is a common problem. Most embeddings are trained for semantic similarity (matching synonyms and similar meanings) but are often used to compare document chunks with questions, which typically have different forms and structures.

Several techniques can help bridge this gap:

- Query expansion (modifying queries to look more like documents)
- Late chunking or contextual retrieval (modifying documents at indexing time)
- Fine-tuning embeddings for your specific use case

Another critical issue is failing to check for index staleness. In the financial news summarization case, the index hadn't been refreshed for two weeks, causing the system to return outdated earnings data when users asked for the "latest" information. For time-sensitive applications, monitoring index freshness is essential, and you may want to filter out documents based on their age.

**_Key Takeaway:_** The mismatch between query form and document form is a fundamental challenge in RAG systems. Address this through query expansion, document modification techniques, or embedding fine-tuning, and always monitor index freshness for time-sensitive applications.

## What problems occur during retrieval?

Accepting vague queries like "health tips" forces RAG systems to retrieve broadly, making it difficult to provide focused, helpful answers. Similarly, accepting off-topic queries (like "write a poem about unicorns" in a product comparison tool) can lead to bizarre outputs that damage user trust.

To address these issues:

- Detect low-information queries through heuristics or classifiers
- Prompt users for clarification when queries are too vague
- Route off-topic queries to fallback responses
- Use intent classification to detect and handle queries outside your domain
- Implement relevance thresholds to avoid returning poor matches

Another common mistake is failing to break down complex tasks. For example, a customer support system was using the full RAG pipeline to answer "What is my billing date?" when a simple metadata lookup would be faster, cheaper, and more reliable. Identifying common query patterns and routing them to specialized handlers can significantly improve performance.

**_Key Takeaway:_** Not every query needs the full RAG treatment. Implement intent classification to route simple queries to specialized handlers and reject off-topic requests that your system isn't designed to handle.

## How should we approach evaluation of RAG systems?

Many teams evaluate only the documents they retrieve, missing critical insights about false negatives. This is like "looking for your keys under the lamppost because that's where the light is" - you're only examining a small portion of the potential solution space.

For comprehensive evaluation:

- Look beyond your retrieval window when logging and evaluating
- Log or reproduce scores for your ranking/retrieval to analyze performance
- Evaluate both relevance (are retrieved documents relevant?) and sufficiency (do they contain enough information to answer the query?)

Creating a quadrant analysis of correct/incorrect answers versus sufficient/insufficient retrieval provides powerful insights into where to focus improvement efforts. Each quadrant suggests different approaches to enhancing system performance.

Another common mistake is increasing system complexity without proper evaluation. Skylar has seen many clients implement sophisticated retrieval and re-ranking systems without first establishing whether they actually improve performance. In over 90% of these cases, the new system performed worse when properly evaluated.

**_Key Takeaway:_** Always implement evaluations before increasing system complexity. It's easy to fool yourself into thinking you know what the problem is, but data-driven evaluation provides essential guardrails.

## What re-ranking challenges do RAG systems face?

Overusing boosting rules can make systems difficult to understand and maintain. While boosting (adjusting ranking scores based on specific criteria) can be a useful hack to improve relevance, adding too many rules creates complexity. In the financial news example, boosting semiconductor-related content, recent articles, and earnings-related terms created a system that was hard to debug and understand.

Another issue is allowing "facepalm results" - outputs that are so obviously wrong that users lose trust in the system. These often occur because lower layers of retrieval optimize for high recall (getting anything potentially relevant), and the re-ranking layer fails to filter out inappropriate content.

To prevent these issues:

- Minimize manual boosting rules
- Consider training a custom cross-encoder re-ranker for better performance
- Apply metadata filters to exclude known irrelevant document types
- Blacklist domains or content patterns that typically produce poor results
- Remove low-value chunks from your index
- Monitor your system with test queries that have previously produced bad results

**_Key Takeaway:_** Re-ranking is your last line of defense against irrelevant content. Invest in robust filtering and monitoring to prevent embarrassing outputs that damage user trust.

## What generation-phase problems affect RAG systems?

Simple RAG systems often struggle with reasoning-based queries that require connecting information from multiple sources. For example, an academic research assistant needed to understand relationships between papers, which required multiple retrieval steps to connect the dots.

For these complex use cases, consider:

- Adopting agentic RAG workflows that interleave retrieval and reasoning
- Pre-computing synthesis documents that connect related information
- Constructing knowledge graphs to help traverse relationships between documents

Finally, hallucination remains a significant challenge, particularly in sensitive domains like healthcare. In the medical advice chatbot, the system hallucinated a drug side effect that wasn't present in the source material.

The most effective approach to reducing hallucination in RAG systems is:

- Force the LLM to provide inline citations
- Validate that each citation exists in the retrieved documents
- Semantically validate that each citation actually supports the claimed content

**_Key Takeaway:_** For complex reasoning tasks, simple RAG may not be sufficient. Consider more sophisticated approaches like agentic workflows or knowledge graphs, and always implement citation validation to prevent hallucination in sensitive domains.

## How important is metadata tagging in practice?

According to Skylar, about 40% of clients have indexes so small that metadata tagging doesn't provide significant benefits. Many B2B companies have segregated data by customer, further reducing the need for complex tagging within each customer's dataset.

The value of metadata tagging increases with:

1. The diversity of queries you're answering
1. The scale of data you're working with

For specific use cases like legal documents, metadata about authorship, ownership, and modification history can be crucial. By embedding these tags into the text chunks themselves (rather than just using them as filter properties), you can answer questions about document history and changes.

**_Key Takeaway:_** The value of metadata tagging depends on your data scale and query diversity. For smaller datasets or narrowly focused applications, extensive tagging may not be necessary, but for complex domains like legal documents, rich metadata can significantly enhance retrieval capabilities.

## What's the most important thing to remember when implementing RAG?

The most critical principle is to continuously examine your data at every stage of the pipeline. This means:

1. Starting with user needs and working backward
1. Looking at your data inputs, intermediate results, and outputs
1. Building robust evaluation systems before increasing complexity
1. Creating fast feedback loops to iterate on improvements

As Skylar emphasized throughout the session, "The teams who can make that loop go as fast as possible are the ones who win, and that is pretty invariable."

By focusing on data quality, implementing proper evaluation, and iterating quickly based on real insights rather than assumptions, you can avoid the common anti-patterns that plague RAG implementations and build systems that truly deliver value to users.

---

FAQs

## What are the most common mistakes in RAG implementations?

The most common mistake is increasing system complexity without proper evaluation. About 90% of the time, teams implement complex retrieval paths and re-ranking systems without evaluating if they actually improve performance. Always establish evaluation metrics before adding complexity to your RAG system to ensure you're making meaningful improvements rather than creating unnecessary maintenance burden.

## What's the single most important principle for successful RAG systems?

Look at your data at every step of the process. Start from understanding what your users want, work backwards, and examine your data throughout the entire pipeline. It's not enough to just check inputs and outputs when you have a complex system with multiple steps—problems might be occurring somewhere in the middle. Teams who can quickly iterate through the cycle of examining data, getting ideas, and adapting their systems are invariably the ones who succeed.

## What are the key stages of a RAG pipeline?

A typical RAG pipeline consists of five main stages:

1. Data collection and curation - Gathering the right documents to answer queries
1. Extraction and enrichment - Representing documents well with proper metadata
1. Indexing and storage - Setting up documents for easy retrieval
1. Retrieval and re-ranking - Finding relevant documents with high recall, then filtering for precision
1. Generation - Using an LLM to create answers based on retrieved information

## What problems commonly occur during data collection and curation?

Two major issues arise during this phase:

1. Documents with varied encodings or formats often silently fail to process. In one medical chatbot implementation, 21% of documents were silently dropped due to encoding issues. Always monitor document counts at each stage and implement robust error handling.
1. Irrelevant document sets create a "ticking time bomb" waiting to be retrieved for some query. Carefully curate your document index to include only content relevant to the types of queries you intend to serve. Consider using metadata tagging to filter documents for specific query types.

## What extraction and enrichment issues should I watch for?

Information extraction failures are particularly common with PDFs and tables. Many off-the-shelf PDF extraction tools struggle with complex layouts like tables, multi-column text, and specialized formats. Use tools specifically designed for the artifacts you need to extract and always validate the extracted content to ensure it meets your accuracy requirements.

## What are the common chunking mistakes in RAG systems?

Two primary chunking issues to avoid:

1. Chunking too small - Many implementations use tiny chunks (like 200 characters) because they follow outdated tutorials, but this dilutes context and meaning. In one e-commerce implementation, small chunks meant no single chunk contained complete information, leading to hallucinations in 13% of queries. Use longer context windows and chunk by semantic boundaries.
1. Keeping bad chunks - Retaining low-value content like footers, copyright notices, and duplicative content creates noise in your system. Inspect your shortest chunks manually and implement deduplication through content hashing.

## What indexing and storage problems should I be aware of?

Two critical issues in this phase:

1. Naive embedding usage - Most embeddings are trained for semantic similarity but questions often differ in form from document chunks. Consider techniques like query expansion, late chunking, contextual retrieval, or fine-tuning embeddings to bridge this gap.
1. Index staleness - Without monitoring index freshness, you risk providing outdated information. In one financial news system, the index hadn't been refreshed for two weeks, resulting in outdated earnings reports. Track staleness metrics and consider adding timestamp filters to exclude outdated content.

## What retrieval issues commonly impact RAG systems?

Several retrieval problems can undermine your system:

1. Accepting vague queries like "health tips" forces your system to retrieve anything remotely relevant. Detect low-information queries and prompt users for clarification.
1. Accepting off-topic queries (like "write a poem about unicorns" in a product comparison tool) can produce inappropriate responses. Implement intent classification to detect and handle off-topic requests.
1. Lack of task breakdown - Not recognizing patterns in user queries means missing opportunities to create more efficient workflows. For common, structured queries (like "What is my billing date?"), consider direct metadata lookups instead of using the full RAG pipeline.

## How should I approach evaluation in my RAG system?

Many teams evaluate only the relevance of retrieved documents but miss two critical evaluation dimensions:

1. False negatives - Examine documents that weren't retrieved but should have been. Look beyond your retrieval window to find relevant documents that were missed.
1. Retrieval sufficiency - Evaluate whether the retrieved documents contain enough information to fully answer the query, not just whether they're relevant. This helps identify whether problems stem from retrieval or from your document corpus itself.

## What re-ranking problems should I watch for?

Two common re-ranking issues:

1. Overusing boosting - Adding too many manual boosting rules (like boosting recent content or specific keywords) makes systems complex and unpredictable. Minimize manual boosting and consider training a custom re-ranker for better performance.
1. Allowing "facepalm results" - Obviously bad results that make users question your system's competence. Apply metadata filters to exclude irrelevant document types and monitor your system for these embarrassing failures.

## What generation phase issues should I address?

Two key generation concerns:

1. Using simple RAG for reasoning queries - Single-pass retrieval can't connect dots between concepts. For complex reasoning, consider agentic RAG workflows that interleave retrieval and reasoning, or pre-compute synthesis documents.
1. Lack of output guardrails for hallucination - Especially critical in sensitive domains like healthcare. Force your LLM to provide inline citations, validate that each citation exists, and semantically validate that citations support the content.

## How can I reduce hallucinations in my RAG system?

The most effective technique is implementing a three-step verification process:

1. Force your LLM to provide inline citations for claims
1. Validate that each citation actually exists in your retrieved documents
1. Semantically validate that each citation actually supports the content it's referencing

This approach is particularly important for sensitive domains like healthcare where hallucinated information could have serious consequences.

## What tools are recommended for RAG evaluation?

While tool preferences vary by situation, Lily Pad (from Microscope) is highlighted as particularly useful for teams without AI engineering backgrounds because it enforces best practices around versioning. However, the best approach is often to meet teams where they are and use their existing tools rather than introducing new ones that require vendor approval.

## How important is metadata tagging in RAG systems?

The value of metadata tagging depends on two factors:

1. The scale of your data - About 40% of implementations have indexes so small that extensive tagging provides little benefit
1. The diversity of queries you're answering

Metadata becomes more valuable when you have both high data volume and diverse query types. For B2B applications where customer data is segregated, the benefit may be limited since each customer's data volume is relatively small.

---

--8<--
"snippets/enrollment-button.md"
--8<--

---
