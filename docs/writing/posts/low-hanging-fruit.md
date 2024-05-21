---
draft: False
date: 2024-05-11
slug: low-hanging-fruit-for-rag-search
comments: true
categories:
  - RAG
authors:
  - jxnl
---

# Low-Hanging Fruit for RAG Search

!!! note "RAG Course"
  
    I'm building a RAG Course right now, if you're interested in the course please fill out this [form](https://q7gjsgfstrp.typeform.com/ragcourse)

RAG (Retrieval-Augmented Generation), is a powerful technique that combines information retrieval with LLMs to provide relevant and accurate responses to user queries. By searching through a large corpus of text and retrieving the most relevant chunks, RAG systems can generate answers that are grounded in factual information.

In this post, we'll explore six key areas where you can focus your efforts to improve your RAG search system. These include using synthetic data for baseline metrics, adding date filters, improving user feedback copy, tracking average cosine distance and Cohere reranking score, incorporating full-text search, and efficiently generating synthetic data for testing.

<!-- more -->

!!! note "Consulting Services"

    I like to give the ideas for free but sell the implementation. If you're interested in getting some help on improving your rag application. Take a look at my [consulting services](../../services.md).

By addressing these low-hanging fruit, you can take your RAG search system to the next level, providing users with more relevant, accurate, and timely information. Let's dive in and explore each of these opportunities in more detail.

## 1. Synthetic Data for Baseline Metrics

Synthetic data can be used to establish baseline precision and recall metrics for your reverse search.
The simplest kind of synthetic data is to take existing text chunks, generate synthetic questions, and verify that when we query our synthetic questions, the sourced text chunk is retrieved correctly. 

**Benefits:**

1. Establishes a foundation for measuring system complexity and performance
2. Pinpoints areas for improvement and drives optimization efforts
3. Enables affordable, repeatable testing and evaluation
4. Provides a consistent reference point when introducing new models or features, allowing for meaningful comparisons. If the baseline remains unchanged, production data can be leveraged to enhance synthetic question generation or the system as a whole.

**Costs:**

This should really just be a matter of writing a simple prompt that generates questions, hopefully with a few shot examples, and iterating over existing text chunks. Once you have that, you can store pairs of query strings and chunk IDs. And a simple forloup can be used to verify that the query strings are retrieving the correct chunks. 


## 2. Adding Date Filters

Incorporating date filters into your search system can significantly improve the user experience by providing more relevant and up-to-date information. A big issue that I see oftentimes is people asking questions like, what is the latest, blah, blah, blah. This fundamentally does not embed anything and you need to end up using date filters and additional prompting to extract ranges out. 

**Benefits:**

1. Increased relevance and freshness of search results
2. Improved efficiency in narrowing down results
3. Enabling trend analysis and historical context


**Costs**

I talk about this in my [blog post](https://jxnl.github.io/instructor/blog/2023/09/17/rag-is-more-than-just-embedding-search/#case-study-1-metaphor-systems) about RAG. Is probably going to add, you know, for 500, 700 milliseconds to do some kind of query understanding.

## 3. Improving Thumbs Up/Down Copy

Using specific copy for your thumbs up/down buttons, such as "Did we answer your question?" instead of generic phrases, offers several benefits. This is particularly relevant when we care about question answer accuracy, but want to explicitly avoid getting negative feedback for being slow or verbose or having poor formatting. You might care about different things, but it's important to be explicit. Do not use generic copy like, did you like our response? 

**Benefits:**

1. Focused feedback on the relevance and quality of search results
2. Reduced ambiguity in user interpretation
3. Actionable insights for improving the search system

**Costs**

It might just be worth having a separate index or table that just stores question answer pairs and whether or not we're satisfied. This would be enough to drawing back onto our similarity data below and do some clustering and data analysis to figure out what the and priorities should be. 

## 4. Tracking Average Cosine Distance and Cohere Reranking Score

Monitoring the average cosine distance and Cohere reranking score for each question can help identify challenging queries and prioritize improvements. Once you have a table of query and scores, you will be able to do data analysis to figure out areas where you are underperforming, at least in the relevancy. 

**Benefits:**

1. Identifying strengths and weaknesses of the search system
2. Enabling targeted optimization for specific query types
3. Data-driven decision making for resource allocation and feature prioritization

**Costs**

Again, here we're just logging things. As long as we have a request ID, we can do something pretty simple like...

```json
{
    "request_id": "12345",
    "query": "What is the latest news?",
    "mean_cosine_distance": 0.3,
    "mean_cohere_reranking_score": 0.4
}
```

## 5. Using Full-Text Search

Incorporating both full-text search and semantic search (vector search) can improve the overall performance of your search system. This one is almost obvious for anyone who's building actual search systems. Include BM25 and you will likely see better results. 

**Benefits:**

1. Identifying relevant documents based on exact keyword matches
2. Uncovering conceptually similar documents
3. Improving the overall effectiveness of the search system

**Cost**

Here you gotta make sure your user system that uses full text search. Something like [LanceDB](https://lancedb.com/) really improves the UX.

## 6. Making Text Chunks Look Like Questions

When generating synthetic data for testing your search system, it's more efficient to make text chunks look like questions rather than the other way around. Generating Hyde introduces more latency at query time, but if you really care about results, you should be willing to incur ingestion costs to make search better at runtime. It's good for you to think that your text chunks and your queries should have similar embeddings, so it might be good to embed question-answer pairs if you know what kind of questions people are asking ahead of time. 

**Benefits:**

1. Reduced latency compared to generating hypothetical document embeddings
2. More effective testing of the search system's performance
3. Avoiding the overhead of generating embeddings for every possible question variant

## 7. Including File and Document Metadata

When chunking text for your search system, it's beneficial to include file and document metadata as additional text in each chunk. This metadata can provide valuable context and improve search relevance.

**Benefits:**

1. Improved search relevance by leveraging metadata information
2. Ability to filter and narrow down search results based on metadata fields
3. Enhanced understanding of the document structure and hierarchy

**Costs:**

Including metadata requires modifying the text chunking process to append the relevant information to each chunk. This may involve extracting metadata from file paths, document headers, or a separate metadata database. The additional text will slightly increase the storage requirements for the chunks.

Example metadata to include:

- File path
- Document title
- Author
- Creation date
- Tags or categories

By incorporating file and document metadata, you can enrich the search experience and provide users with more targeted and relevant results.


## Conclusion

By focusing on these low-hanging fruit opportunities, you can significantly enhance the performance and usability of your RAG search system, ultimately providing a better experience for your users.

If you have any questions about these details, please leave a comment below and let's get a conversation started. My goal really is to bring the unconscious conscious and being able to answer questions will really help me clarify my own thinking. 

!!! note "RAG Course"
  
    I'm building a RAG Course right now, if you're interested in the course please fill out this [form](https://q7gjsgfstrp.typeform.com/ragcourse)