---
authors:
  - jxnl
categories:
  - RAG
comments: true
date: 2024-02-28
description: Explore levels of complexity in RAG applications, from basics to advanced
  methods for building effective systems.
draft: false
tags:
  - Retrieval-Augmented Generation
  - Data Processing
  - Asynchronous Programming
  - System Optimization
  - User Engagement
---

# Levels of Complexity: RAG Applications

This guide explores different levels of complexity in Retrieval-Augmented Generation (RAG) applications. We'll cover everything from basic ideas to advanced methods, making it useful for beginners and experienced developers alike.

We'll start with the basics, like breaking text into chunks, creating embeddings, and storing data. Then, we'll move on to more complex topics such as improved search methods, creating structured responses, and making systems work better. By the end, you'll know how to build strong RAG systems that can answer tricky questions accurately.

As we explore these topics, we'll use ideas from other resources, like our articles on [data flywheels](./data-flywheel.md) and [improving tool retrieval in RAG systems](./trade-off-tool-selection.md). These ideas will help you understand how to create systems that keep improving themselves, making your product better and keeping users more engaged.

Key topics we'll explore include:

1. Basic text processing and embedding techniques
2. Efficient data storage and retrieval methods
3. Advanced search and ranking algorithms
4. Asynchronous programming for improved performance
5. Observability and logging for system monitoring
6. Evaluation strategies using synthetic and real-world data
7. Query enhancement and summarization techniques

This guide aligns with the insights from our [RAG flywheel article](./rag-flywheel.md), which emphasizes the importance of continuous improvement in RAG systems through data-driven iterations and user feedback integration.

<!-- more -->

If you want to learn more about I systematically improve RAG applications check out my free 6 email improving rag crash course

[Check out the free email course here](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }

## Level 1: The Basics

Welcome to the foundational level of RAG applications! Here, we'll start with the basics, laying the groundwork for your journey into the realm of Retrieval-Augmented Generation. This level is designed to introduce you to the core concepts and techniques essential for working with RAG models. By the end of this section, you'll have a solid understanding of how to traverse file systems for text generation, chunk and batch text for processing, and interact with embedding APIs. Let's dive in and explore the exciting capabilities of RAG applications together!

1. Recursively traverse the file system to generate text.
2. Utilize a generator for text chunking.
3. Employ a generator to batch requests and asynchronously send them to an embedding API.
4. Store data in LanceDB.
5. Implement a CLI for querying, embedding questions, yielding text chunks, and generating responses.

### Processing Pipeline

```python
from dataclasses import dataclass
from typing import Iterable, List
import asyncio

sem = asyncio.Semaphore(10)

class TextChunk(BaseModel):
    id: int
    text: str
    embedding: np.array
    filename: str
    uuid: str = Field(default_factory=uuid.uuid4)

def flatmap(f, items):
    for item in items:
        for subitem in f(item):
            yield subitem

def get_texts():
    for file in files:
        yield TextChunk(
            text=file.read(),
            embedding=None,
            filename=file.name
        )

def chunk_text(items:Iterable[TextChunk], window_size: int, overlap: int=0):
    for i in range(0, len(items), window_size-overlap):
        yield TextChunk(
            text = items[i:i+window_size],
            embedding = None,
            filename = items[i].filename
        )

def batched(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def embed_batch(chunks: List[TextChunk]) -> List[TextChunk]:
    texts = [chunk.text for chunk in chunks]
    resp = embedding_api( # this is just the openai call
        texts=texts
    )
    for chunk, embedding in zip(chunks, resp):
        chunk.embedding = embedding
        yield chunks

def save_batch(chunks: List[TextChunk]):
    for chunk in chunks:
        db.insert(chunk)

if __name__ == "__main__":
    # This is the CLI
    texts = get_texts()
    chunks = flatmap(chunk_text, texts)
    batched_chunks = batched(chunks, 10)
    for chunks in tqdm(batched_chunks):
        chunk_with_embedding = embed_batch(chunks)
        save_batch(chunk_with_embedding)
```

### Search Pipeline

```python
def search(question: str) -> List[TextChunk]:
    embeddings = embedding_api(texts=[question])
    results = db.search(question)
    return results

if __name__ == "__main__":
    question = input("Ask a question: ")
    results = search(question)
    for chunk in results:
        print(chunk.text)
```

### Answer Pipeline

```python
def answer(question: str, results: List[TextChunk]) -> str:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=False,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt(question, results)}
        ]
    )

if __name__ == "__main__":
    question = input("Ask a question: ")
    results = search(question)
    response = answer(question, results)
    for chunk in response:
        print(chunk.text, end="")
```

## Level 2: More Structured Processing

Here we delve deeper into the world of Retrieval-Augmented Generation (RAG) applications. This level is designed for those who have grasped the basics and are ready to explore more advanced techniques and optimizations. Here, we focus on enhancing the efficiency and effectiveness of our RAG applications through better asynchronous programming, improved chunking strategies, and robust retry mechanisms in processing pipelines.

In the search pipeline, we introduce sophisticated methods such as better ranking algorithms, query expansion and rewriting, and executing parallel queries to elevate the quality and relevance of search results.

Furthermore, the answering pipeline is refined to provide more structured and informative responses, including citing specific text chunks and employing a streaming response model for better interaction.

### Processing

1. Better Asyncio
2. Better Chunking
3. Better Retries

### Search

1. Better Ranking (Cohere)
2. Query Expansion / Rewriting
3. Parallel Queries

```python
class SearchQuery(BaseModel):
    semantic_search: str

def extract_query(question: str) -> Iterable[SearchQuery]:
    return client.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Extract a query"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        response_model=Iterable[SearchQuery]
    )

def search(search: Iterable[SearchQuery]) -> List[TextChunk]:
    with LanceDB() as db:
        results = db.search(search)
        return results


def rerank(question: str, results: List[TextChunk]) -> List[TextChunk]:
    return cohere_api(
        question=question,
        texts=[chunk.text for chunk in results]
    )

if __name__ == "__main__":
    question = input("Ask a question: ")
    search_query = extract_query(question)
    results = search(search_query)
    ranked_results = rerank(question, results)
    for chunk in ranked_results:
        print(chunk.text)
```

### Answering

1. Citating specific text chunks
2. Streaming Response Model for better structure.

```python
class MultiPartResponse(BaseModel):
    response: str
    followups: List[str]
    sources: List[int]

def answer(question: str, results: List[TextChunk]) -> Iterable[MultiPartResponse]:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=True,
        response_model=instructor.Partial[MultiPartResponse]
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt(question, results)}
        ]
    )

if __name__ == "__main__":
    from rich.console import Console

    question = input("Ask a question: ")

    search_query = extract_query(question)
    results = search(search_query)
    results = rerank(question, results)
    response = answer(question, results)

    console = Console()
    for chunk in response:
        console.clear()
        console.print(chunk.dump_model_json())
```

## Level 3: Observability

At Level 3, the focus shifts towards the critical practice of observability. This stage emphasizes the importance of implementing comprehensive logging mechanisms to monitor and measure the multifaceted performance of your application. Establishing robust observability allows you to swiftly pinpoint and address any bottlenecks or issues, ensuring optimal functionality. Below, we outline several key types of logs that are instrumental in achieving this goal.

### Expanding on Wide Event Tracking

Wide event tracking

- [Do it wide](https://isburmistrov.substack.com/p/all-you-need-is-wide-events-not-metrics?utm_source=tldrwebdev)

### Log how the queries are being rewritten

1. When addressing a complaint we should quickly understand if the query was written correctly

| Query | Rewritten Query | latency | ... |
| ----- | --------------- | ------- | --- |
| ...   | ...             | ...     | ... |

example: once we found that for queries with "latest" the dates it was selecting was literally the current date, we were able to quickly fix the issue by including few shot examples that consider latest to be 1 week or more.

1. Training a model

We can also use all the positive examples to figure out how to train a model that does query expansion better.

### Log the citations

By logging the citations, we can quickly understand if the model is citing the correct information, what text chunks are popular, review and understand if the model is citing the correct information. and also potentially build a model in the future that can understand what text chunks are more important.

| Query | Rewritten Query | ... | Citations |
| ----- | --------------- | --- | --------- |
| ...   | ...             | ... | [1,2,4]   |

There's a couple ways you can do this. For example, when you cite something, you can include not only what was shown to the language model, but also what was cited. If something was shown as a language model but was not cited, we can include this as part of the dataset.

| Query | Rewritten Query | ... | sources | cited |
| ----- | --------------- | --- | ------- | ----- |
| ...   | ...             | ... | [1,2,4] | [1,2] |

### Log mean cosine scores and reranker scores

By attaching this little metadata, we will be able to very cheaply identify queries that may be performing poorly.

| Query                          | Rewritten Query                | ... | Mean Cosine Score | Reranker Score |
| ------------------------------ | ------------------------------ | --- | ----------------- | -------------- |
| What is the capital of France? | What is the capital of France? | ... | 0.9               | 0.8            |
| Who modified the file last?    | Who was last in the race?      | ... | 0.2               | 0.1            |

Here you might see "oh clearly i can't answer questions about file modification" thats not even in my index.

### Log user level metadata for the search

By including other group information information, we can quickly identify if a certain group is having a bad experience

Examples could be

1. Organization ID
2. User ID
3. User Role
4. Signup Date
5. Device Type
6. Geo Location
7. Language

This could help you understand a lot of different things about how your application is being used. Maybe people on a different device are asking shorter queries and they are performing poorly. Or maybe when a new organization signed up, the types of questions they were asking were being served poorly by the language model. In the future we'll talk about other metrics, but just by implementing the mean cosine score and the free ranker score, you get these things for free without any additional work.

Just by building up some simple dashboards that are grouped by these attributes and look at the average scores, you can learn a lot. My recommendation is to review these things during stand-up once a week, look at some examples, and figure out what we could do to improve our system. When we see poor scores, we can look at the query and the rewritten query and try to understand what exactly is going on.

### Have Users

By this point you should definitely be having users. You've already set yourself for success by understanding queries, rewriting them, and monitoring how users are actually using your system. The next couple of steps will be around improving specific metrics and also different ways of doing that.

## Level 4: Evaluations

Evaluations at this stage are crucial for understanding the performance and effectiveness of our systems. Primarily, we are dealing with two distinct systems: the search system and the question answering (QA) system. It's common to see a lot of focus on evaluating the QA system, given its direct interaction with the end-user's queries. However, it's equally important to not overlook the search system. The search system acts as the backbone, fetching relevant information upon which the QA system builds its answers. A comprehensive evaluation strategy should include both systems, assessing them individually and how well they integrate and complement each other in providing accurate, relevant answers to the user's queries.

### Evaluating the Search System

The aim here is to enhance our focus on key metrics such as precision and recall at various levels (K). With the comprehensive logging of all citation data, we have a solid foundation to employ a language model for an in-depth evaluation of the search system's efficacy.

For instances where the dataset might be limited, turning to synthetic data is a practical approach. This method involves selecting random text chunks or documents and then prompting a language model to generate questions that these texts could answer. This process is crucial for verifying the search system's ability to accurately identify and retrieve the text chunks responsible for generating these questions.

```python
def test():
    text_chunk = sample_text_chunk()
    questions = ask_ai(f"generate questions that could be ansered by {text_chunk.text}")
    for question in questions:
        search_results = search(question)

    return {
        "recall@5": (1 if text_chunk in search_results[:5] else 0),
        ...
    }

average_recall = sum(test() for _ in range(n)) / n
```

Your code shouldn't actually look like this, but this generally captures the idea that we can synthetically generate questions and use them as part of our evaluation. You can try to be creative. But ultimately it will be a function of how well you can actually write a generation prompt.

### Evaluating the Answering System

This is a lot trickier, but often times people will use a framework like, I guess, to evaluate the questions. Here I recommend spending some more time building out a data set that actually has answers.

```python
def test():
    text_chunk = sample_text_chunks(n=...)
    question, answer = ask_ai(f"generate questions and answers for {text_chunk.text}")

    ai_answer = rag_app(question)
    return ask_ai(f"for the question {question} is the answer {ai_answer} correct given that {answer} is the correct answer?")
```

#### Evaluating the Answering System: Feedback

It's also good to build in feedback mechanisms in order to get better scores. I recommend building a thumbs up, thumbs down rating system rather than a five star rating system. I won't go into details right now, but this is something I strongly recommend.

### The purpose of synethic data

The purpose of synthetic data is to help you quickly get some metrics out. It will help you build out this evaluation pipeline in hopes that as you get more users and more real questions, you'll be able to understand where we're performing well and where we're performing poorly using the suite of tests that we have. Precision, recall, mean ranking scores, etc.

## Level 5: Understanding Short comings

At this point you should be able to have a data set that is extremely diverse using both the synthetic data and production data. We should also have a suite of scores that we can use to evaluate the quality of our answers.

| org_id | query | rewritten | answer | recall@k | precision@k | mean ranking score | reranker score | user feedback | citations | sources | ... |
| ------ | ----- | --------- | ------ | -------- | ----------- | ------------------ | -------------- | ------------- | --------- | ------- | --- |
| org123 | ...   | ...       | ...    | ...      | ...         | ...                | ...            | ...           | ...       | ...     | ... |

Now we can do a bunch of different things to understand how we're doing by doing exploratory data analysis. We can look at the mean ranking score and reranker score and see if there are any patterns. We can look at the citations and see if there are any patterns. We can look at the user feedback and see if there are any patterns. We can look at the sources and see if there are any patterns. We can look at the queries and see if there are any patterns.

### Clustering Queries

We can use clustering to understand if there are any patterns in the queries. We can use clustering to understand if there are any patterns in the citations. We can use clustering to understand if there are any patterns in the sources. We can use clustering to understand if there are any patterns in the user feedback.

We'll go into more depth later, but the general idea is we can also introduce cluster topics. I find that there's usually two different kinds of clutches that we detect.

1. Topics
2. Capabilities

Topics are captured by the nature of the text chunks and the queries. Capabilities are captured by the nature of the sources or additional metadata that we have.

Capabilites could be more like:

1. Questions that ask about document metadata "who modified the file last"
2. Quyestions that require summarzation of a document "what are the main points of this document"
3. Questions that required timeline information "what happened in the last 3 months"
4. Questions that compare and contrast "what are the differences between these two documents"

There are all things you'll likely find as you cluster and explore the datasets.

### Upcoming Topics

As we continue to explore the depths of RAG applications, the following areas will be addressed in subsequent levels, each designed to enhance the complexity and functionality of your RAG systems:

#### Level 6: Advanced Data Handling

- Finding Segments and Routing: Techniques for identifying and directing data segments efficiently.
- Processing Tables: Strategies for interpreting and manipulating tabular data.
- Processing Images: Methods for incorporating image data into RAG applications.

#### Level 7: Query Enhancement

- Building Up Timeline Queries: Crafting queries that span across different timeframes for dynamic data analysis.
- Adding Additional Metadata: Leveraging metadata to enrich query context and improve response accuracy.

#### Level 8: Summarization Techniques

- Summarization and Summary Indices: Developing concise summaries from extensive datasets to aid quick insights.

#### Level 9: Outcome Modeling

- Modeling Business Outcomes: Applying RAG techniques to predict and model business outcomes, facilitating strategic decision-making.

## Want to learn more?

Most teams jump straight to Level 4 complexity and wonder why everything breaks. The secret? Master each level before moving up. Want help navigating this progression? Here's how I work with teams:

[Consulting Services](../../services.md){ .md-button .md-button--primary }
[Maven RAG Playbook — 20% off with EBOOK](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button }
