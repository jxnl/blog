---
title: "Lexical Search in RAG Applications"
speaker: John Berryman
cohort: 3
description: "Guest lecture with John Berryman on traditional search techniques, their application in RAG systems, and how lexical search complements semantic search"
tags: [lexical search, traditional search, hybrid search, information retrieval, TF-IDF, filtering]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Lexical Search - John Berryman

I hosted a session featuring John Berryman, who shared his expertise on lexical search and its application in RAG systems. John, who previously worked at GitHub and co-authored books on prompt engineering and information retrieval, provided valuable insights on how traditional search techniques can complement modern vector-based approaches for more effective retrieval augmented generation.

<!-- more -->

## Why is lexical search still relevant in the age of semantic search?

While semantic search has become the default approach for RAG systems, John highlighted several limitations that make it problematic in certain scenarios. The primary issues include:

- Semantic search struggles with exact matches for product IDs, people's names, and specific phrases
- It performs poorly with niche jargon not present in the embedding training data
- Relevance is opaque, making debugging difficult when results aren't as expected
- Filtering is particularly clunky in vector-based systems

The filtering challenge is especially significant. With semantic search, you're forced into suboptimal approaches: either search first and then filter (risking empty results if filters are strict), or filter first and then semantically re-rank (which can be computationally expensive for large datasets).

**_Key Takeaway:_** Semantic search excels at understanding meaning but struggles with exact matching, specialized terminology, and efficient filtering - all areas where lexical search has established strengths.

## How does lexical search actually work?

John provided a concise explanation of lexical search fundamentals, breaking it down into three components:

1. Indexing: Documents are processed through analysis pipelines that include character filtering (like lowercasing), tokenization (splitting text into words), stopword removal (filtering common words), and stemming (normalizing word forms). This creates an inverted index where each token points to documents containing it.
2. Searching: The inverted index makes retrieval extremely efficient. For a search like "brown AND fox," the system simply retrieves the document IDs for each term and finds their intersection. This approach handles Boolean logic naturally and can incorporate relevance scoring through methods like TF-IDF (term frequency-inverse document frequency).
3. Results: Beyond just returning matching documents, lexical search can provide rich metadata like aggregations (facet counts showing distribution of values), snippets (relevant text excerpts), and highlights (showing where terms matched).

The key advantage is that lexical search can process filtering and relevance scoring simultaneously, unlike the sequential approach required in semantic search.

**_Key Takeaway:_** Lexical search's inverted index structure enables efficient simultaneous filtering and relevance scoring, with established relevance algorithms like TF-IDF and BM25 that have been refined over decades.

## How can lexical search be applied in RAG applications?

John demonstrated a practical application using the Wayfair Annotation Dataset (WANDs), containing about 43,000 e-commerce products. He showed how to:

1. Structure the index with appropriate field types (product name, description, class, rating count)
2. Build queries that combine must-match conditions with should-match boosting factors
3. Apply filters for availability, product class, and minimum ratings
4. Return not just results but also aggregations that provide insight into the matching set

When integrated into a RAG application, this approach allows the LLM to:

- Search with pre-applied filters (like showing only products available in the user's state)
- Explore results through multiple searches to narrow options
- Leverage aggregation data to understand the distribution of matching products
- Make more informed recommendations based on both the results and metadata

In the demonstration, a user complaint about back pain led the assistant to search for both ergonomic chairs and standing desks, then refine based on the facet data to focus on adjustable standing desks specifically.

**_Key Takeaway:_** Lexical search provides RAG systems with powerful filtering capabilities and metadata that allows LLMs to make more informed decisions about how to refine searches and present options to users.

## What are the limitations of lexical search?

Despite its strengths, John acknowledged several significant limitations:

- Lexical search struggles with word order and context (e.g., confusing "dress shoe" with a shoe that is a dress)
- It uses a bag-of-words approach that loses semantic meaning
- It can't recognize synonyms or different words with the same meaning
- It doesn't understand negation (searching for "not something" still matches "something")
- It misses contextual clues that embedding models naturally capture

These are precisely the areas where semantic search excels, suggesting that neither approach is sufficient on its own.

**_Key Takeaway:_** Lexical search's limitations around understanding meaning, context, and synonyms are the exact strengths of semantic search, pointing toward hybrid approaches as the optimal solution.

## What hybrid search approaches show promise?

John explored several approaches to combining the strengths of lexical and semantic search:

1. Lexical search plus re-ranking: Use lexical search to filter and provide an initial ranking, then apply semantic re-ranking to the top results. This is established but complex.
2. SPLADE (Sparse Lexical and Dense Expansion): Use language models to identify synthetic synonyms that should have been in the text but weren't, then add these to the lexical index. This expands recall but still has bag-of-words limitations.
3. Acorn: A promising approach that traverses vector structures while simultaneously checking filter matches.
4. Superlinked: Uses different embeddings for different data types, concatenating them into unified vectors that can be searched with nearest neighbor techniques while maintaining filtering capabilities.

John admitted that the ideal hybrid solution remains elusive, but the industry is actively working on approaches that combine the filtering power of lexical search with the semantic understanding of vector-based methods.

**_Key Takeaway:_** The future likely belongs to hybrid approaches that combine lexical search's filtering capabilities with semantic search's understanding of meaning, though the ideal implementation is still evolving.

## How do you optimize lexical search for specific domains?

During the Q&A, John shared insights on improving search for domain-specific applications:

1. Start by collecting data on what should match versus what actually matches
2. For e-commerce, analyze click logs to understand user behavior patterns
3. Focus on high-impact queries - often the top 10 queries account for 50% of traffic
4. Use human curators familiar with the domain to create judgment lists
5. Consider learn-to-rank algorithms that can automatically tune parameters based on this data

For hybrid approaches, he suggested getting the top 100-1000 results from lexical search, then using a feature store to retrieve additional information (including embeddings) for re-ranking with models like LambdaMart or XGBoost.

**_Key Takeaway:_** Optimizing search requires a combination of data analysis, human expertise, and appropriate algorithms. The most effective approach often involves using lexical search for initial filtering and retrieval, then applying more sophisticated ranking methods.

**Final thoughts on the lexical versus semantic debate**

While John humorously admitted his bias toward lexical search ("lexical search is my hammer and the world is my nail"), he clearly recognized that both approaches have complementary strengths. Lexical search excels at filtering, exact matching, and providing rich metadata, while semantic search better understands meaning, context, and synonyms.

The most promising direction appears to be hybrid approaches that leverage the strengths of both methods, though implementing these effectively remains challenging. As LLMs become more capable, they may also play a role in dynamically adjusting search parameters based on user needs, further blurring the line between lexical and semantic approaches.

## **_Key Takeaway:_** The debate isn't really about lexical versus semantic search, but rather how to effectively combine them to create retrieval systems that are both precise and understanding - offering both the filtering power of traditional search and the semantic comprehension of modern embedding-based approaches.

--8<--
"snippets/enrollment-button.md"
--8<--

---
