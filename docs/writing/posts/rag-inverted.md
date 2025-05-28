---
authors:
  - jxnl
categories:
  - RAG
comments: true
date: 2024-01-07
description: Explore inverted thinking to build a terrible RAG system and learn pitfalls
  to avoid for better recommendations.
draft: false
slug: inverted-thinking-rag
tags:
  - RAG systems
  - inverted thinking
  - recommendation systems
  - machine learning
  - software engineering
---

# How to build a terrible RAG system

If you've followed my work on RAG systems, you'll know I emphasize treating them as recommendation systems at their core. In this post, we'll explore the concept of inverted thinking to tackle the challenge of building an exceptional RAG system.

!!! note "What is inverted thinking?"

    Inverted thinking is a problem-solving approach that flips the perspective. Instead of asking, "How can I build a great RAG system?", we ask, "How could I create the worst possible RAG system?" By identifying potential pitfalls, we can more effectively avoid them and build towards excellence.

This approach aligns with our broader discussion on RAG systems, which you can explore further in our [RAG flywheel article](./rag-flywheel.md) and our comprehensive guide on [Levels of Complexity in RAG Applications](./rag-levels-of-rag.md).

<!-- more -->

If you want to learn more about I systematically improve RAG applications check out my free 6 email improving rag crash course

[Check out the free email course here](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }

!!! tip "Inventory"

    You'll often see me use the term inventory. I use it to refer to the set of documents that we're searching over. It's a term that I picked up from the e-commerce world. It's a great term because it's a lot more general than the term corpus. It's also a lot more specific than the term collection. It's a term that can be used to refer to the set of documents that we're searching over, the set of products that we're selling, or the set of items that we're recommending.

## Don't worry about latency

There must be a reason that chat GPT tries to stream text out. Instead, we should only show the results once the entire response is completed. Many e-commerce websites have found that 100 ms improvement in latency can increase revenue by 1%. Check out [
How One Second Could Cost Amazon $1.6 Billion In Sales](https://www.fastcompany.com/1825005/how-one-second-could-cost-amazon-16-billion-sales).

## Don't show intermediate results

Users love love staring at a blank screen. It's a great way to build anticipation. If we communicated intermittent steps like the ones listed below, we'd just be giving away the secret sauce and users prefer to be left in the dark about what's going on.

1. Understanding your question
2. Searching with "..."
3. Finding the answer
4. Generating response

## Don't Show Them the Source Document

Never show the source documents, and never highlight the origin of the text used to generate the response. Users should never have to fact-check our sources or verify the accuracy of the response. We should assume that they trust us and that there is no risk of false statements.

## We Should Not Worry About Churn

We are not building a platform; we are just developing a machine learning system to gather metrics. Instead of focusing on churn, we should concentrate on the local metrics of our machine learning system like AUC and focus on benchmarks on HuggingFace.

## We Should Use a Generic Search Index

Rather than asking users or trying to understand the types of queries they make, we should stick with a generic search and not allow users to generate more specific queries. There is no reason for Amazon to enable filtering by stars, price, or brand. It would be a waste of time! Google should not separate queries into web, images, maps, shopping, news, videos, books, and flights. There should be a single search bar, and we should assume that users will find what they're looking for.

## We Should Not Develop Custom UI

It doesn't make sense to build a specific weather widget when the user asks for weather information. Instead, we should display the most relevant information. Semantic search is flawless and can effectively handle location or time-based queries. It can also re-rank the results to ensure relevance.

## We Should Not Fine-Tune Our Embeddings

A company like Netflix should have a generic movie embedding that can be used to recommend movies to people. There's no need to rely on individual preferences (likes or dislikes) to improve the user or movie embeddings. Generic embeddings that perform well on benchmarks are sufficient for building a product.

## We Should Train an LLM

Running inference on a large language model locally, which scales well, is cost-effective and efficient. There's no reason to depend on OpenAI for this task. Instead, we should consider hiring someone and paying them $250k a year to figure out scaling and running inference on a large language model. OpenAI does not offer any additional convenience or ease of use. By doing this, we can save money on labor costs.

## We Should Not Manually Curate Our Inventory

There's no need for manual curation of our inventory. Instead, we can use a generic search index and assume that the documents we have are relevant to the user's query. Netflix should not have to manually curate the movies they offer or add additional metadata like actors and actresses to determine which thumbnails to show for improving click rates. The content ingested on day one is sufficient to create a great recommendation system.

## We Should Not Analyze Inbound Queries

Analyzing the best and worst performing queries over time or understanding how different user cohorts ask questions will not provide any valuable insights. Looking at the data itself will not help us generate new ideas to improve specific segments of our recommendation system. Instead, we should focus on improving the recommendation system as a whole and avoid specialization.

Imagine if Netflix observed that people were searching for "movies with Will Smith" and decided to add a feature that allows users to search for movies with Will Smith. That would be a waste of time. There's no need to analyze the data and make system improvements based on such observations.

## Machine Learning Engineers Should Not Be Involved in Ingestion

Machine Learning Engineers (MLEs) do not gain valuable insights by examining the data source or consulting domain experts. Their role should be limited to working with the given features. Theres no way that MLEs who love music would do a better job at Spotify, or a MLE who loves movies would do a better job at Netflix. Their only job is to take in data and make predictions.

## We Should Use a Knowledge Graph

Our problem is so unique that it cannot be handled by a search index and a relational database. It is unnecessary to perform 1-2 left joins to answer a single question. Instead, considering the trending popularity of knowledge graphs on Twitter, it might be worth exploring the use of a knowledge graph for our specific case.

## We should treat all inbound inventory the same

There's no need to understand the different types of documents that we're ingesting. How different could marketing content, construction documents, and energy bills be? Just because some have images, some have tables, and some have text doesn't mean we should treat them differently. It's all text, and so an LLM should just be able to handle it.

## We should not have to build special ingestion pipelines

GPT-4 has solve all of data processing so if i handle a photo album, a pdf, and a word doc, it should be able to handle any type of document. There's no need to build special injestion pipelines for different types of documents. We should just assume that the LLM will be able to handle it. I shouldn't dont even have to think about what kinds of questions I need to answer. I should just be able to ask it anything and it should be able to answer it.

## We should never have to ask the data provider for clean data

If Universal studios gave Netflix a bunch of MOV files with no metadata, Netflix should not have to ask Universal studios to provide additional movie metadata. Universal might not know the runtime, or the cast list and its netflix's job to figure that out. Universal should not have to provide any additional information about the movies they're providing.

## We should never have to cluster our inventory

Theres only one kind of inventory and one kind of question. We should just assume that the LLM will be able to handle it. I shouldn't dont even have to think about what kinds of questions I need to answer. Topic clustering would only show us how uniform our inventory is and how little variation there is in the types of questions that users ask.

## We should focus on local evals and not A/B tests

Once we run our GPT-4 self critique evaluations we'll know how well our system is doing and it'll make us more money, We should spend most of our time writing evaluation prompts and measuring precision / recall and just launching the best one. A/B tests are a waste of time and we should just assume that the best performing prompt will be the best performing business outcome.

## Want to learn more?

I also wrote a 6 week email course on RAG, where I cover everything in my consulting work. It's free and you can:

[Check out the free email course here](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }
