---
title: Stop Trusting MTEB Rankings (Kelly Hong, Chroma)
speaker: Kelly Hong
cohort: 3
description: A deep dive into generative benchmarking - creating custom evaluation sets from your own data to better assess embedding model performance.
tags: [embeddings, evaluation, benchmarking, generative evals, Chroma]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Stop Trusting MTEB Rankings (Kelly Hong, Chroma)

I hosted a session with Kelly Hong from Chroma, who presented her research on generative benchmarking for retrieval systems. She explained how to create custom evaluation sets from your own data to better test embedding models and retrieval pipelines, addressing the limitations of standard benchmarks like MTEB.

<!-- more -->

[▶️ See Chroma's Testing Framework in Action](https://maven.com/p/30886a){: .md-button .md-button--primary}

**Why public benchmarks like MTEB don't reflect real-world performance**

When evaluating embedding models for retrieval applications, many teams rely on public benchmarks like MTEB (Massive Text Embedding Benchmark). While convenient for comparing models, these benchmarks have significant limitations:

The data is too generic and doesn't match specific domain needs. Even domain-specific MTEB datasets like legal documents aren't as specific as your actual production data.

The query-document pairs are artificially clean - questions are perfectly formulated and documents are perfect matches. In real applications, user queries are ambiguous, incomplete, and often phrased as statements rather than questions.

There's significant risk of data contamination since embedding models may have seen these public datasets during training, making it unclear if you're testing retrieval capability or just memorization.

As Kelly put it: "If you have really good performance on a public benchmark for a given embedding model, that doesn't necessarily guarantee that you'll also get that good performance for your specific production pipeline."

**_Key Takeaway:_** Good performance on public benchmarks doesn't translate to good performance in your specific application. You need to evaluate embedding models on your own data to get meaningful results.

**The generative benchmarking approach**

Generative benchmarking creates custom evaluation sets directly from your data through a two-step process:

1. Chunk filtering: Using an LLM judge to identify document chunks that users would realistically query about

1. Query generation: Creating realistic queries from those filtered chunks

This approach addresses the limitations of public benchmarks because:

- It's specific to your data
- It generates more realistic queries that reflect actual user behavior
- It tests retrieval on private data that embedding models haven't seen during training

Kelly shared a case study with Weights & Biases where they started with 13,000 document chunks and about 2,000 real user queries from production. After filtering, they generated queries that matched the style and content of real user questions.

The results were revealing - the embedding model Weights & Biases had been using (text-embedding-3-small) actually performed worse than alternatives they tested. Even more interesting, the rankings of embedding models on their custom benchmark contradicted the MTEB rankings.

**Creating realistic queries that match user behavior**

One of the most important aspects of generative benchmarking is generating queries that actually reflect how users search. Kelly demonstrated that naively generated queries (without context or examples) tend to be perfectly formed questions that make retrieval too easy.

For example, a naive query generation might produce "What is the purpose of artifact versioning in Weights & Biases?" But real users are more likely to search with something like "artifact versioning not working."

To generate realistic queries, Kelly recommended providing:

1. Context about your application (e.g., "This is a technical support bot for Weights & Biases")

1. Example queries from real users (5-7 examples is usually sufficient)

When I work with companies building vertical AI applications, I approach this by:

- Interviewing subject matter experts about what they actually search for
- Having LLMs generate candidate queries through role-playing exercises
- Getting experts to review and validate the generated queries

I've recently been experimenting with using OpenAI's Deep Research for this - I'll have it research a domain like "search systems for lawyers dealing with employment claims" and use that research as part of my prompt. This approach has been surprisingly effective for generating realistic queries.

**The importance of human involvement in the evaluation process**

Kelly emphasized that generative benchmarking isn't a fully automated "press one button and everything's done" approach. Human involvement remains critical:

"Human involvement is very critical. If you want really good evals, I think it applies to basically any case where you're working with AI as well. I think it's very rare that your system is going to work well with absolutely no human in the loop."

For the chunk filtering step, the Chroma team:

1. Started with a small set of about 300 document chunks

1. Manually labeled them as relevant or irrelevant

1. Iterated on their LLM judge criteria 4-5 times to align with human judgment

1. Only then scaled to the full document corpus

I've seen too many teams try to fully automate their evaluation process without ever looking at the actual data. I often tell clients, "You can't delegate all the thinking to these LLMs." The reluctance to actually look at examples is a common problem.

I find that many teams lean on LLM evals which give you this feeling of control because you're always twiddling with the generation prompt. But if your recall is very low - if you just can't find the document because of some phrasing in the text - then everything downstream is really bad. People feel empowered to adjust prompts but don't focus enough on making search better.

**Practical applications of generative benchmarking**

Kelly outlined several practical applications of generative benchmarking beyond just selecting the best embedding model:

- Identifying irrelevant content in your document corpus
- Iterating on specific components of your retrieval pipeline (reranking, chunk rewriting)
- Aligning your evaluation set with production query distributions
- Identifying knowledge gaps in your document corpus

"I think it becomes even more powerful once you actually have production traffic to work with," Kelly noted. "You can cluster your production queries by topic, and you can see the distribution of topics that your users are asking about, and then you can use that distribution and align your eval set to that."

**Balancing cost and performance in retrieval optimizations**

When discussing contextual chunk rewriting (where you provide document context for each chunk), Kelly acknowledged its benefits but cautioned about the costs:

"Contextual rewriting is useful, but also very expensive. So I would be more intentional about how you use it."

She suggested being selective about which chunks need context rather than rewriting everything, potentially using the chunk filtering process to identify which documents would benefit most from context.

I emphasized the value of having quantifiable metrics for these decisions: "This is the benefit of having an actual eval harness. The real conversation isn't 'should we use retrieval, or should we use contextual retrieval,' it is 'if we use contextual retrieval, our metrics go up 2%. Is that worth it? Probably not. But if you did contextual retrieval, and it went up 20%, then the question is, okay, well, is spending 20 cents per document worth the 20% improvement in retrieval?' That is a quantified decision that you can make."

I've seen similar patterns with hybrid search. In one case, I worked with companies processing transcripts where lexical search performed nearly as well as semantic search but was 10 times faster. I told them, "If I want to find meeting notes, I want that to be as fast as possible."

**Setting up efficient evaluation infrastructure**

When asked about hyperparameter tuning and experimentation time, Kelly shared that their process was relatively quick because they worked with small data samples first:

"We did around 4 or 5 iterations, but we did it across a small subset of data. So we were only working with about 300 labeled document chunks. So it was very quick iteration. We weren't doing it over our entire document corpus. So I think that probably took less than a day for me to do."

I emphasized that how much time you spend on evaluation really depends on what kind of existing infrastructure you have: "I've joined companies where their embedding model is like sequential call to OpenAI. And I was like, 'well, this is why it's taking you 6 days to do these experiments.'"

I recommend time-boxing experimentation: "I mostly try to time box how much research we're going to do, and then figure out how many experiments we can run. And usually what's going to happen is as you iterate on your prompts and on your models, the marginal improvement in performance will slowly decrease."

The goal isn't perfection - it's making the most of your experimental time. I personally use Modal for this - I can reembed all of Wikipedia with any arbitrary model in about 10 minutes, which makes hyperparameter sweeping much more feasible.

**Handling metadata in retrieval evaluations**

When asked about incorporating metadata into the evaluation process, Kelly suggested several approaches:

"I think maybe metadata could be useful when you're performing the retrieval task... if you have metadata like, let's say you have a query and retrieve a category of documents that have a certain metadata tag, maybe that can count as a partial retrieval success."

She also noted that metadata can be valuable for pre-filtering documents before applying an LLM judge: "If all this data was just scraped from the website, maybe there was a metadata tag that says 'this is from our news section.' We'd want to filter those out, because that's not really relevant to our users."

I added that metadata filters can be evaluated separately from retrieval quality: "If you have really simple ones like 'show me all the news articles from last week,' we can individually test our ability to select date ranges." This allows you to verify both retrieval accuracy and structured extraction tasks independently.

**Final thoughts**

Kelly concluded by emphasizing that generative benchmarking requires human involvement to be effective: "When we talk about generative benchmarking, that also doesn't mean that this entire process is 100% automated. You do need some human in the loop if you really want a good eval."

The main takeaway from the session was that good performance on public benchmarks doesn't guarantee good performance for your specific use case.

As Kelly put it: "I think the main takeaway from this entire talk is that if you have good performance on public benchmarks like MTEP, that doesn't necessarily guarantee that same performance for your specific use case, and generative benchmarking is a pretty good solution to that."

For those interested in trying generative benchmarking, Kelly mentioned that Chroma has made their tools available, and I noted they're offering $1,000 in API credits for participants in the cohort.

---

FAQs

## What is generative benchmarking?

Generative benchmarking is a method to create custom evaluation sets from your own data to test AI retrieval systems. It involves generating realistic queries from your document corpus and using these query-document pairs to evaluate how well different embedding models and retrieval systems perform with your specific data. Unlike public benchmarks, this approach gives you insights directly relevant to your use case.

## Why are custom benchmarks better than public benchmarks like MTEB?

Custom benchmarks address several limitations of public benchmarks like MTEB (Massive Text Embedding Benchmark). While MTEB is widely used for comparing embedding models, it uses generic data that may not reflect your specific domain, contains artificially clean query-document pairs, and may have been seen by models during training. Good performance on MTEB doesn't guarantee good performance on your specific data and use case.

## How does the generative benchmarking process work?

The process involves two main steps. First, chunk filtering identifies document chunks that users would realistically query about, filtering out irrelevant content. Second, query generation creates realistic user queries from these filtered chunks. The resulting query-document pairs form your evaluation set, which you can use to test different embedding models and retrieval components.

## What's involved in the chunk filtering step?

Chunk filtering uses an aligned LLM judge to identify document chunks that contain information users would actually query. This involves creating criteria for relevance, providing a small set of human-labeled examples, and iterating on the LLM judge to improve alignment with human judgment. This step helps filter out irrelevant content like news articles or marketing material that wouldn't be useful in a support context.

## How do you generate realistic queries?

Query generation uses an LLM with specific context about your application and example queries. Providing this context helps the LLM focus on topics users would ask about, while example queries guide the style of generated queries. This approach creates more realistic, sometimes ambiguous queries that better reflect how users actually search, rather than perfectly formed questions that match document content exactly.

## How do you evaluate retrieval performance with the generated benchmark?

Once you have your evaluation set with query-document pairs, you can test different embedding models by embedding each document chunk, storing them in a vector database, and then embedding each query to retrieve the top K document chunks. If the matching document is in the top K results, that counts as a success. This gives you metrics like recall@K and NDCG that you can compare across different models and configurations.

## What insights can generative benchmarking provide?

Generative benchmarking can help you select the best embedding model for your specific data, identify irrelevant content in your document corpus, and evaluate changes to your retrieval pipeline like adding re-ranking or chunk rewriting. It can also reveal when public benchmark rankings don't align with performance on your data, as demonstrated in a case study where model rankings differed from MTEB rankings.

## Do I need production data to use generative benchmarking?

No, you can use generative benchmarking even if you don't have production data yet. All you need is a document corpus to generate an evaluation set. However, if you do have production queries, you can use them to further align your generated queries to real user behavior, identify knowledge gaps in your document corpus, and make your evaluation set even more representative.

## Is generative benchmarking fully automated?

No, generative benchmarking isn't 100% automated. It requires human involvement to get good results. You'll need to align your LLM judge, provide context and example queries to steer query generation, and manually review data throughout the process. The human-in-the-loop aspect is critical for creating evaluation sets that truly reflect your use case.

## How can I try generative benchmarking on my own data?

You can try generative benchmarking on your own data by using Chroma's open-source tools. The full technical report is available at research.trychroma.com, and you can run the process with just a few lines of code. Chroma Cloud is also available if you want to use their hosted vector database solution.

## How does contextual chunk rewriting fit into retrieval evaluation?

Contextual chunk rewriting involves adding context to document chunks to improve retrieval. While it can be effective, especially for content like tables or technical information that lacks context, it's also expensive since it requires running an LLM on every chunk. A more efficient approach might be to only rewrite chunks that need additional context, which you can identify during the filtering process. The value of this approach can be quantified through your evaluation metrics.

---

--8<--
"snippets/enrollment-button.md"
--8<--

---
