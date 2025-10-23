---
title: "TurboPuffer: Object Storage-First Vector Database Architecture"
speaker: Simon, CEO of TurboPuffer
cohort: 3
description: "Deep dive into TurboPuffer's object storage-first vector database architecture, economics of different storage approaches, and real-world implementations from companies like Notion, Linear, and Cursor."
tags:
  [
    vector databases,
    object storage,
    TurboPuffer,
    RAG architecture,
    database economics,
    search performance,
  ]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# TurboPuffer: Object Storage-First Vector Database Architecture

I hosted a session with Simon, CEO of TurboPuffer, to explore how vector search works at scale for RAG applications. We discussed the economics and architecture of object storage-based vector databases, performance considerations, and real-world implementations from companies like Notion, Linear, and Cursor.

<!-- more -->

---

👉 If you want to learn more about RAG systems, check out our RAG Playbook course. Here is a 20% discount code for readers. 👈

[RAG Playbook - 20% off for readers](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button .md-button--primary }

---

## Why is TurboPuffer different from traditional vector databases?

TurboPuffer represents a fundamentally different approach to vector search by being the first completely object storage native database. This architecture emerged from two key ingredients needed for any successful new database:
**A new workload:** Connecting LLMs to enormous amounts of data through RAG creates unique storage challenges. When you vectorize text, you experience significant storage amplification - 1 kilobyte of text might expand to 16 kilobytes of vector data after chunking and embedding.

**A new storage architecture:** Traditional database architectures become prohibitively expensive at vector scale. Simon shared an example where a company's $3,000/month Postgres instance would have cost $30,000/month if they vectorized all their unstructured text in a traditional vector database.

The TurboPuffer architecture leverages three technological advances that weren't available a decade ago:

- **NVMe SSDs** that are only 4-5x slower than memory but 100x cheaper than DRAM
- **S3's strong consistency guarantees** (introduced in 2020)
- **S3's compare-and-swap functionality** (launched December 2023)

### The "Pufferfish" Storage Hierarchy

TurboPuffer implements a three-tier storage hierarchy that automatically moves data based on access patterns:

1. **Object Storage (S3/GCS/Azure)**: Cold storage at ~$0.02/GB, queries take 200-500ms
2. **NVMe SSD Cache**: Warm storage, queries take tens of milliseconds
3. **RAM Cache**: Hot storage, queries take <10ms

This creates a tiered storage system where data inflates from object storage to disk to RAM as needed - like a pufferfish inflating when threatened, hence the name. The system automatically manages this hierarchy without manual intervention.

**Key Takeaway:** Traditional vector databases store everything in RAM or across multiple SSDs, making them prohibitively expensive at scale. TurboPuffer's object storage-first approach can reduce costs by up to 95% while maintaining performance for active data through intelligent caching.

## How does the economics of different storage architectures compare?

Simon broke down the economics of different storage approaches:

- RAM: ~$5 per gigabyte
- 3 SSDs (traditional database redundancy): ~$0.60 per gigabyte
- S3 object storage: ~$0.02 per gigabyte

By storing data primarily in object storage and only caching what's actively being used, TurboPuffer creates a 10x cost advantage. The system is designed to be "round-trip sensitive" - optimized to maximize data retrieved in each storage access rather than making many small requests.

### TurboPuffer's Clustered Index Architecture

For vector search specifically, TurboPuffer uses clustered indexes rather than graph-based approaches (like HNSW) that require many round trips. This design is optimized for object storage access patterns:

**How Clustered Indexes Work:**

1. Vectors are grouped semantically into clusters
2. Cluster centroids are stored together for fast access
3. Query execution involves just two round trips:
   - First trip: Retrieve all centroids to identify relevant clusters
   - Second trip: Fetch only the most relevant cluster data

**Why This Beats Graph-Based Approaches:**

- HNSW requires many small round trips (bad for object storage)
- Clustered indexes maximize data retrieved per round trip
- Better suited for high-throughput, batch-oriented workloads
- Enables the 10+ million vectors per second write performance

## What are the trade-offs of this architecture?

Simon was refreshingly transparent about the limitations:

- Cold queries can be slow (200-500ms) when data isn't in cache
- High write latency (100-200ms) since writes go directly to object storage
- Not suitable for high-transaction workloads like e-commerce checkout systems

However, these trade-offs are acceptable for search and RAG applications where:

- Warm queries can be as fast as in-memory databases
- Write throughput can scale to 10+ million vectors per second
- The architecture provides a "serverless" experience without managing node types

**Key Takeaway:** Object storage-first databases aren't suitable for every workload, but for search and RAG applications, the economic benefits far outweigh the occasional cold query penalty, especially when you can predict and pre-warm caches.

## How are companies using TurboPuffer in production?

Simon shared several case studies of companies using TurboPuffer at scale:

**Cursor:** Each codebase is a namespace in S3, with tens of millions of these at any time. When you open a codebase in Cursor, it starts hydrating the cache for that namespace, making subsequent semantic queries faster. This approach allowed Cursor to index much larger repositories than was economically feasible before, while cutting costs by 95%. The namespace-per-codebase architecture means inactive codebases cost almost nothing to store.

**Notion:** Saved "millions of dollars" by moving to TurboPuffer's architecture. With more than 10 billion vectors across millions of namespaces, Notion's workload is perfect for this approach since only a subset of workspaces are active at once. After migrating, Notion removed all per-user AI charges. Their usage pattern shows clear power-law distribution - most data is rarely accessed, making object storage ideal.

**Linear:** Moved from Elasticsearch and PGVector to TurboPuffer for a more hands-free experience. They view it as a foundational search layer that enables them to connect more data to LLMs without operational overhead. The migration eliminated their need to manage vector database infrastructure while improving search quality.

**Superhuman:** Uses TurboPuffer for intelligent email search and organization features, leveraging the cost-effective storage to index years of email history that would be prohibitively expensive with traditional vector databases.

## How should developers think about caching and performance?

TurboPuffer aims to make caching decisions automatic rather than requiring manual configuration. The main control available is a "hint cache warm" request that starts hydrating the cache for a namespace without charging for a query if it's already cached.

For applications like Notion, when a user opens the Q&A dialog, they send a request to start warming the cache for that particular namespace, ensuring subsequent queries are fast.

Simon emphasized that while cold queries can take 500-600ms, warm queries can be as fast as 8-10ms. The system is designed to automatically inflate the "pufferfish" for frequently accessed data.

## What should developers consider when building vector search systems?

### Embedding Model Latency is Often the Bottleneck

One overlooked consideration is embedding model latency. Simon pointed out that it doesn't matter if your vector database query takes 8ms when your embedding model has a 300ms P50 latency.

**Key Recommendations:**

- Test embedding provider latency from your specific geographic region
- Consider model switching costs (requires re-embedding everything)
- Models from Cohere, Gemini, and Voyage typically offer good latency characteristics
- Factor in both P50 and P95 latencies for production planning

### Storage Amplification Effects

When planning vector search systems, account for significant storage amplification:

- 1KB of text → ~16KB of vector data (after chunking + embeddings)
- Multiple embedding models multiply storage requirements
- Metadata and indexing structures add overhead
- Plan for 10-20x storage expansion from raw text to searchable vectors

### Query Pattern Analysis

Understand your access patterns before choosing a database architecture:

- **Uniform access**: Traditional in-memory databases might be better
- **Power-law distribution**: Object storage-first architectures excel
- **Write-heavy workloads**: Consider TurboPuffer's clustered indexes
- **Multi-tenant applications**: Namespace-based storage can dramatically reduce costs

## How does TurboPuffer handle updates to indexed content?

For applications like Cursor where files change frequently, there's an interesting observation: the semantic meaning of content doesn't change with every keystroke the way full-text search results might.

Many customers find a compromise between immediate updates and efficiency:

- Debounce changes by time or character count
- Consider the economics of re-embedding (which is often more expensive than storing in TurboPuffer)
- Evaluate how much semantic drift occurs with small edits

TurboPuffer itself is optimized for writes, with all reads being strongly consistent by default - once you write to the database, it's immediately available on the next query.

## How can facets and aggregations enhance RAG applications?

I'm particularly excited about how facets and aggregations can improve context engineering for agents. While traditional RAG just returns text chunks, facets provide metadata about the results that can guide future queries.

For example, if an agent searches code with `search_chunks()` and discovers that 45% of relevant chunks come from a specific file, it might decide to `read_file()` the entire file rather than making more semantic searches. This gives agents the context they need to make better tool selections.

In e-commerce, facets help users discover they can filter by brand, price range, or ratings. Similarly, for agents, facets reveal the structure of the data and available filtering dimensions that weren't apparent from the initial query.

For legal applications, facets might show that 90% of relevant clauses come from three specific documents, prompting the agent to load those entire documents rather than continuing with chunk-based searches.

**Key Takeaway:** The future of RAG isn't just about retrieving text chunks - it's about providing agents with context about the data landscape so they can make better decisions about how to explore it further. Facets and aggregations are powerful tools for this context engineering approach.

## What minimum requirements does TurboPuffer have?

TurboPuffer currently has minimum spend requirements, which Simon explained are not about infrastructure limitations but about ensuring a high-quality support experience. The team takes uptime seriously and maintains an on-call pager system to be responsive to any issues.

While they plan to lower these requirements over time and eventually offer a free tier, their current focus is on providing excellent support to customers with production workloads.

For smaller use cases, Simon suggested that PGVector might be sufficient if you already have a Postgres database, though TurboPuffer offers significant advantages for larger-scale applications.

## Final thoughts on building search systems for LLMs

Simon emphasized that successful databases eventually implement every query type their users need. The goal for TurboPuffer is to allow both humans and agents to converse naturally with data, which requires a range of query capabilities beyond simple vector similarity.

As we build systems for agents to interact with data, we need to think about providing rich context rather than just raw results. The computational requirements of loading billions of records into a context window aren't feasible, so databases need to provide ways to summarize, aggregate, and pivot data to make it explorable.

The most successful RAG implementations will combine vector search, full-text search, filtering, and aggregations to give agents the tools they need to efficiently navigate large datasets and extract meaningful insights.

---

## FAQs

## What is TurboPuffer and what makes it unique?

TurboPuffer is a search engine built on object storage that offers semantic search, full-text search, and aggregations. What makes it unique is its storage architecture—all data is stored by default on S3, GCS, or Azure Blob Storage with caching in front of it. This architecture works like a JIT compiler, where the more you query it, the faster it becomes as data moves up into cache hierarchies. TurboPuffer is the first completely object storage native database, designed specifically for modern search needs.

## Who uses TurboPuffer?

TurboPuffer is used by companies like Cursor, Notion, Linear, and Superhuman. These companies have chosen TurboPuffer for production-level search capabilities, often migrating from more expensive and slower solutions. Many of these companies use TurboPuffer to power their semantic search features, particularly for connecting large language models to enormous amounts of data.

## How does TurboPuffer's storage architecture work?

TurboPuffer uses a tiered storage approach. Data is primarily stored in object storage (S3, GCS, or Azure Blob) at about 2 cents per gigabyte. When data is accessed, it's cached in SSDs and RAM based on usage patterns. This creates a "pufferfish effect" where data inflates from object storage (where queries take around 500ms) to disk (tens of milliseconds) and finally to RAM (less than 10ms). This architecture is significantly more cost-effective than traditional database architectures that store multiple copies on SSDs.

## What cost savings can I expect with TurboPuffer?

Many customers have reduced their costs by up to 95% when switching to TurboPuffer from traditional vector database solutions. This is because object storage costs about 2 cents per gigabyte, compared to approximately 60 cents per gigabyte for traditional database storage (using 3 SSDs for redundancy). The economics are particularly favorable for vector search workloads, which typically involve large amounts of data.

## What are the limitations of TurboPuffer?

TurboPuffer has two main limitations due to its object storage architecture:

- Cold queries can be slow (around 500ms) when data isn't in cache and needs to be fetched from object storage
- Write latency is high (100-200ms) because writes go directly to object storage

These limitations make TurboPuffer less suitable for high-transaction workloads like checkout systems, but ideal for search and RAG (Retrieval Augmented Generation) applications.

## How does TurboPuffer handle vector search?

TurboPuffer uses clustered indexes for vector search, which are optimized for object storage and disk access. This approach groups similar vectors together and stores them adjacently. When searching, TurboPuffer first retrieves centroids (cluster centers), identifies the closest clusters, and then only downloads those specific clusters. This minimizes round trips to storage while maximizing data throughput, making it efficient for object storage, disk, and memory.

## How does TurboPuffer compare to other vector databases?

Unlike traditional in-memory vector databases, TurboPuffer doesn't require all data to be in memory, making it more cost-effective for large datasets where only a portion is actively used. Compared to AWS's vector search on object storage, TurboPuffer offers significantly lower latency for warm queries. Unlike graph-based vector indexes (HNSW), TurboPuffer's clustered approach is better suited for object storage and high write throughput workloads.

## What kind of performance can I expect from TurboPuffer?

Cold query performance (when data isn't cached) is around 200-500ms, depending on the workload. Once data is cached, performance is comparable to in-memory databases, with latencies as low as 8-10ms. TurboPuffer can handle extremely high write throughput (10+ million vectors per second) and scales horizontally with object storage.

## How does caching work in TurboPuffer?

TurboPuffer automatically manages caching without requiring manual configuration. The system is designed to inflate the "pufferfish" (cache data) based on usage patterns. You can send a "cache warm" request to TurboPuffer to proactively hydrate the cache for specific data, which many customers do when they anticipate user interactions. For example, Notion sends cache warming requests when users open the Q&A dialog.

## How does TurboPuffer handle consistency?

By default, TurboPuffer provides strong consistency for reads. Once you write data to TurboPuffer, it's immediately available for the next query with strong consistency guarantees. This makes systems more predictable and easier to reason about. You can turn this off for better performance if eventual consistency is acceptable for your use case.

## How should I choose embedding models when using TurboPuffer?

When selecting embedding models to use with TurboPuffer, consider the latency of the embedding model itself. Some popular embedding models have high latency (300ms+), which can become the bottleneck in your search system regardless of how fast TurboPuffer is. Models from providers like Cohere, Gemini, and Voyage typically offer better latency. It's important to test the latency from your specific region to avoid performance issues later.

## Does TurboPuffer support facets and aggregations?

Yes, TurboPuffer supports facets and aggregations, which are useful for both traditional search applications and newer AI-powered use cases. In e-commerce, facets help users filter by attributes like color, size, or price. In AI applications, facets can provide additional context to language models, helping them make more informed search queries and better understand the data structure.

## Is TurboPuffer suitable for small use cases?

TurboPuffer currently has minimum spend requirements, making it more suitable for production-level applications rather than small experiments. The company maintains these requirements to ensure they can provide high-quality support and reliability. For very small use cases, alternatives like PGVector might be more appropriate. The TurboPuffer team plans to lower these requirements over time as they scale their support capabilities.

---

👉 If you want to learn more about RAG systems, check out our RAG Playbook course. Here is a 20% discount code for readers. 👈

[RAG Playbook - 20% off for readers](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button .md-button--primary }

---
