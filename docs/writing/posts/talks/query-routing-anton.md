---
title: "Data Organization and Query Routing for RAG Systems"
speaker: Anton
cohort: 3
description: "Guest lecture with Anton Troynikov from ChromaDB on organizing data for retrieval systems, query routing strategies, and optimizing vector search performance"
tags: [data organization, query routing, vector search, ChromaDB, retrieval optimization, filtering]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Query Routing - Anton (ChromaDB)

I recently hosted a session featuring Anton Troynikov from ChromaDB who shared critical insights about organizing data for retrieval systems. This often-overlooked aspect of RAG implementation can significantly impact retrieval accuracy and overall system performance. Here's a breakdown of the key concepts and best practices for structuring your data to optimize query routing.

<!-- more -->

## Why is data organization so critical for RAG systems?

Anton emphasized that before doing anything else with your retrieval system, you need to look at two critical elements: your data and your queries. This fundamental step is often skipped, leading to suboptimal performance.

"You need to look at your data. You need to look at what exactly is going into your vector database or your database. You need to actually see what's in there before you do literally anything else," Anton explained.

Beyond just examining your data, you should also analyze what your users are actually trying to access. There's often a misalignment between the data you've stored and what users are attempting to retrieve, which can lead to unexpected results.

This initial examination forms the foundation for how you'll organize your data for effective retrieval. Without this understanding, you're essentially building on unstable ground.

**_Key Takeaway:_** Always examine both your data and user queries before setting up your retrieval pipeline. This fundamental step will inform your data organization strategy and significantly impact your system's performance.

## What factors should you consider when organizing data for retrieval?

When organizing data for retrieval, Anton highlighted three main considerations: user access patterns, data source characteristics, and query scope.

For user access patterns, ask yourself:

- Do users have access to their own data or shared data?
- Is access limited by team, role, or other factors?
- Does access change over time (adding/removing users, changing permissions)?

For data sources, consider:

- Are you dealing with different types of data (financial reports, scientific papers, etc.)?
- Is your data multimodal (text, images, audio)?
- How frequently is each data source updated?
- Do all users have access to all data sources?

For query scope, think about:

- Do queries need to be filtered by date range, keywords, or other metadata?
- Are queries uniform across users, or do different users query the same data differently?

Understanding these factors will help you determine the most effective way to organize your data for retrieval. This isn't about finding a one-size-fits-all solution, but rather developing a conceptual framework for making informed decisions.

The "big pile of records" approach and its limitations
Anton described what he calls the "big pile of records" approach - using one giant index for all data in your application. This is the default assumption for many vector database vendors, primarily because they were originally built as large-scale search indexes rather than application databases.

"This is what most vendors try to push you into doing," Anton noted. "It's not strictly illegal. You're probably not going to get arrested for doing this yet."

However, this approach has several significant drawbacks:

1. Security and compliance issues: User data is commingled with no logical separation except through filters, which may not provide the same guarantees as proper access controls.
2. Reduced recall: This is a technical but crucial point. When you filter a large index, you're more likely to miss relevant results due to how vector search works under the hood.

Anton explained: "The way that vector search works under the hood for most implementations today is you have your vectors stored as a graph data structure, and you have a compute budget for how many edges of that graph you're going to traverse."

When filtering, you're essentially wasting part of your compute budget on irrelevant nodes, which reduces your ability to find all relevant results. The more specific your filter (like filtering to just one user out of many), the worse this problem becomes.

1. Performance issues: Writing to an already giant index is more expensive than writing to smaller, dedicated indexes.
2. Commingled data types: Different types of data (like code vs. documentation) may require different embedding models for optimal performance, but a single index forces you to use a general embedding model.

**_Key Takeaway:_** The "big pile of records" approach is simple but comes with significant drawbacks in security, performance, and recall. It's suitable for simple use cases like searching Wikipedia, but problematic for complex applications with multiple users and data sources.

The denormalized approach: One index per user per data source
As an alternative to the "big pile" approach, Anton proposed what he calls the "fully denormalized" approach: creating one index per user per data source.

While this sounds complicated and potentially expensive, it offers several significant advantages:

1. Complete separation of user data, eliminating commingling concerns
2. Improved recall because you're no longer filtering indexes
3. Independent indexing, allowing data sources to be updated individually
4. More efficient reads, as you're working with smaller indexes

"It basically overcomes all the problems that I discussed so far," Anton explained.

The main challenges with this approach include:

- Managing more indexes (though Anton noted that ChromaDB was designed to make this efficient)
- Determining where to route queries
- Handling duplicate updates and deletes

For mapping users to indexes, Anton suggested simple solutions like keeping a relational table of which data source goes to which user. This approach also moves access control out of the vector database itself, which may not have robust controls for compliance.

**_Key Takeaway:_** The denormalized approach of one index per user per data source offers better security, performance, and recall than the "big pile" approach, though it requires more sophisticated management of indexes and query routing.

## How do you route queries to the right data sources?

With multiple indexes, routing queries becomes a critical challenge. Anton outlined two main approaches:

1. Full multiplexing: Send the query to all applicable data sources and combine the results. This raises the question of how many results to return from each source. With longer context windows and lower per-token costs, you could simply send all results to the model and let it figure out what's relevant.

Re-ranking models can be particularly effective here: "I think re-ranking models are actually underrated, mostly because people try to use them in the one giant index context instead of using them as an augmentation to query routing."

1. LLM routing: Have an LLM determine which sources are relevant for a given query. This works by telling the model which sources are available and having it decide where to route the query.

"This is a classification task that they're really good at," Anton noted. You don't need the latest and greatest model for this - even smaller, faster models can handle this type of classification effectively.

When using an LLM as a judge for routing, Anton emphasized the importance of calibration: "Go back and look at your data, go and see what the LLM is actually really doing and see what you as a human would do."

**_Key Takeaway:_** Query routing can be handled through full multiplexing (sending queries to all relevant sources) or LLM routing (having a model decide which sources are relevant). Both approaches have merit, with re-ranking models being particularly valuable for combining results from multiple sources.

## Why does filtering reduce recall in vector search?

One of the most technical but important points Anton made was explaining why filtering reduces recall in vector search. This isn't immediately obvious to many practitioners.

Vector search at scale uses approximate nearest neighbor (ANN) search rather than exact matching. As Anton explained:

"In order to make vector search efficient, we cannot use exact matching. Beyond a certain scale, it becomes infeasible to store all of your vectors in memory, and then to perform a nearest neighbor computation against all of those vectors."

Instead, vectors are stored in graph data structures that allow for logarithmic lookup times. This is a fundamental trade-off: "We trade recall for speed, and we trade recall for space."

When filtering is applied in this context, there are two approaches:

1. Pre-filtering: Traversing the graph and only considering nodes that match the filter. If your filter has low selectivity (matches a small percentage of data), most nodes you encounter won't contribute relevant results, wasting your compute budget.
2. Post-filtering: Grabbing many more results than needed (say 1,000 instead of 10) and then filtering that list. This reduces recall even further.

Anton provided a geometric intuition: "Imagine you have red and green points in space, and you're looking for green points. If there's roughly 50-50 red and green points and you draw a circle around them, you're going to have a good chance of getting the number of green points that you're looking for. However, if there are 10 times more red points than green points, and you're selecting 100 points, you're only going to get one-tenth of all the ones that you're looking for."

**_Key Takeaway:_** Filtering in vector search inherently reduces recall due to the approximate nature of vector search algorithms. The more specific your filter, the worse this problem becomes, which is why organizing data into separate indexes can significantly improve performance.

## Should you fine-tune embedding models for specific indexes?

On the topic of fine-tuning embedding models, Anton was enthusiastic: "It's cheap, and you should do it."

He noted that many people get intimidated by fine-tuning because it seems like "big brain AI PhD land," but the reality is that "the hardest part of fine-tuning is creating a dataset and then benchmarking the results."

With separate indexes for different users or data sources, fine-tuning becomes even more powerful. Anton gave the example of an engineering firm with a parts catalog: "The people who are creating the products have a different use for the data in that parts catalog to what the sales people have. So it's the same data, but two groups of users are accessing it completely differently."

Using techniques like embedding adapters, you can fine-tune for different user groups without even needing to re-embed your data, making it a very cost-effective approach.

**_Key Takeaway:_** Fine-tuning embedding models for specific indexes or user groups is more accessible than many realize and can significantly improve retrieval performance. With separate indexes, this becomes even more practical and powerful.

## How should you handle dynamic metadata filtering?

For implementing dynamic metadata filtering, Anton shared examples from financial research and legal domains:

In financial research, you might filter documents based on stock tickers. If a user asks about Uber, it's more effective to either filter against the Uber ticker or have a dedicated index for Uber-related documents.

In the legal domain, you might have different collections for court decisions, briefs, and evidence. When a user asks about a specific court's determination on a particular case, you can route the query specifically to the court decisions index rather than searching across all legal documents.

The key is understanding the natural categories in your domain and creating either separate indexes or robust metadata filtering based on those categories.

**_Key Takeaway:_** Dynamic metadata filtering should be based on natural categories in your domain and user query patterns. This can be implemented through dedicated indexes or metadata filters, with the choice depending on your specific requirements for recall, performance, and security.

**Final thoughts on data organization for RAG**
Anton emphasized that many of the best practices for organizing data in retrieval systems are still evolving. The field of AI application development is relatively young, and many current approaches still carry conceptual baggage from traditional search technologies.

"A lot of what we do in retrieval still has this conceptual overhang from when these were primarily search technologies," Anton noted. The difference is that search indexes rarely remove data, while application databases need to accurately represent a constantly changing world.

As we continue to develop best practices for RAG and retrieval systems, we need to carefully consider which concepts from search technology apply to retrieval and which need to be reconsidered.

The key message throughout Anton's presentation was that data organization isn't just a technical implementation detail - it's a fundamental design decision that impacts security, performance, and most importantly, the quality of results your system can deliver.

## **_Key Takeaway:_** Data organization for RAG systems requires thinking beyond traditional search paradigms. By carefully considering user access patterns, data source characteristics, and query requirements, you can design a system that delivers better results while maintaining security and performance.

--8<--
"snippets/enrollment-button.md"
--8<--

---
