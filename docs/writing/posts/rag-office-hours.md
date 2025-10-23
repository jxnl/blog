---
title: Frequently Asked Questions
date: 2025-08-10
description: Comprehensive FAQ compiled from all office hours sessions across cohorts
---

# Frequently Asked Questions

This comprehensive FAQ is compiled from all office hours sessions across multiple cohorts.

!!! tip "Quick Navigation"
Use your browser's search (Ctrl+F) to find specific terms or questions, or browse through the questions below.

<!-- more -->

This is a collection of questions and answers from the office hours sessions of our course.

[Systematically Improving RAG &mdash; readers get 20% off with code EBOOK](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button .md-button--primary }

## What is your take on DSpy? Should we use it?

Generally, I think DSpy allows you to do some kind of prompt optimization by synthetically creating a bunch of few-shot examples and then identifying which of these examples could improve the performance of your system.

Personally, I feel like most of the time you should be spending a lot of time actually just tweaking those prompts yourself. The most valuable part of looking at data, few-shots, and examples is you building an intuition of what customers are looking for and what mistakes the system is making.

Your product isn't just a prompt—it includes how you collect feedback, how you set expectations in the UI, how you think about data extraction, and how you represent chunks in the context. If you spend the time to look at how the model is making mistakes and what users are asking for, you'll make much more progress in improving the product as a whole.

DSpy is fine especially when you have very specific evaluations. For example, maybe you have a 35-class classification task where all you care about is accuracy. Then DSpy really works because you can figure out which of the 10 examples you need to maximize your accuracy.

But most of the time, that's not the case. If I'm building a model to extract sales insights from a transcript, I don't have a dataset of "here's all the sales insights." The real work might be extracting everything and hand-labeling some stuff. Because these tasks are very hard to hill-climb (when metrics aren't just classification accuracy), tools like DSpy don't work as well.

Another good use of DSpy is around using LLMs as judges. If you have a tonality or factuality evaluation you really care about, it makes sense to label a hundred examples yourself and then use prompt optimization tools to create your own judge that aligns with your grades.

---

## Is it useful to prompt language models with an understanding of structure and rationale for their actions?

Yes, absolutely. Understanding structure and rationale is critical because your product includes the ways you collect feedback, set expectations in the UI, perform data extraction, and represent chunks in the context.

It's not just about the prompt—it's a whole system. And if you can spend time looking at how the model makes mistakes and what users are asking for, you'll make much more progress in improving the product holistically.

When you build an intuition for what's happening, you can make smarter design decisions across the entire product experience.

---

## How do we introduce a concept of time and vector search to answer questions like "What's the latest news?" without needing to move to a graph database?

The answer is to use a SQL database. If you use something like Timescale or PostgreSQL, there are many ways of doing time filtering.

One specific thing to note is the difference between pgvector and pgvector-scale. Pgvector does not do exhaustive search, so there's a chance you don't recall all information because of how the database segments things. With pgvector-scale, it will exhaustively search every single row in your database if required. This small difference means a lot if you're trying to find very specific details.

The general idea is to use structured extraction to identify start and end dates, prompt your language model with an understanding of what those dates are, and then use filtering. You would do an embedding search plus a BETWEEN statement in your time query. This works pretty well.

---

## Is knowledge graph RAG production ready by now? Do you recommend it?

In my 10 years of doing data science and machine learning, I generally stay away from any kind of graph modeling. The reason is that every time I've seen a company go into this graph-based world, within 4-5 years they decide to move back to a PostgreSQL database.

There are several issues with graph databases:

1. They're really hard to learn - it's much easier to hire talent that knows PostgreSQL than graph databases.
1. Defining schemas in PostgreSQL and joins is well-defined, whereas in graph databases there's often too much debate and not enough best practices.
1. Most cases don't require more than one or two traversals of your graph.

When I was at Facebook, their graph was actually just a very large MySQL database. This makes me cautious about using graph databases unless you have expert users.

The only company I really believe could effectively use a graph database is LinkedIn, because they need to compute things like nearest neighbors up to three or five degrees away.

Even for cases like Microsoft's approach where you build a document graph with entities and relationships, I'd prefer to use fine-tuned embeddings. A graph can be defined as an adjacency matrix, and fine-tuning your embeddings can get you pretty close to the similarity definition that a graph could maintain.

I'd rather start with data and say, "There are certain kinds of queries that really need a graph structure" and let that justify the graph structure. Most technology needs to be justified by what the product needs to deliver rather than thinking about technology first.

---

## Would you recommend using Colbert models or other specialized retrieval approaches?

All of these models do similar things at their core. To decide what to use, we should start with a synthetic dataset to measure precision and recall. Then the real question becomes: do any of these interventions (graph RAG, Colbert models, embeddings, re-rankers) beat the baseline in terms of precision and recall?

It might be that graph for a certain problem is only 2% better, in which case it might not be worth the complexity. But if you found that, for parsing hospital records, graph RAG is 40% better on recall and precision, then it doesn't matter what I think—the data would speak for itself.

For Colbert specifically, it probably does very well for certain tasks. For example, statements like "I love coffee" and "I hate coffee" would be very similar in embedding space because embeddings don't fully understand negation. With a Colbert model, the cross-attention mechanism can figure out that these statements are different.

But you need to tell the model what's important in your context. Without enough tests to guide us, it's hard to know if these interventions work. Usually, it's hard to beat the baseline of embedding search with a good re-ranker. Colbert might do 4-5% better, but you need to justify that improvement against the added complexity.

---

## When working with legal documents that have multi-level outlines and reference sections from other documents, what approach would you recommend?

This could be done with a graph, but it could also be done with a simpler pointer system. When you load data, you can pull in other references. For example, in a construction project, whenever we pull up an image, we also pull up the paragraph above and below the image, augmenting the context.

We can do the same for legal documents—if it references another page or citation, we pull in that citation. Technically, this is a graph, but it's often easier to build this as a few LEFT JOINs in a PostgreSQL table.

When we pull in text chunks, if there are references, we just do another left join back to the original chunk. These systems tend to be much simpler to reason about than dealing with reference types in a graph. Usually, that level of complexity really needs to be earned when building bigger systems.

---

## Are we going to cover any fundamentals of how to systematically do generation?

In terms of generation, a lot comes down to prompting and using LLMs as judges, which we'll talk about in Week 3 when discussing product experience.

If you have specific aspects of generation you want to explore, it's mostly about ensuring formatting is correct and chain of thought is reasonable. The challenge is that you can't systematically improve generation primarily because generation evaluations are much more subjective.

If it's just formatting, that can be very explicit. But challenges with generation will mostly be addressed through LLM-as-judge approaches and different levels of regular expressions.

For example, we have an evaluation for summarization that simply measures what percentage shorter the summary is relative to the original input. These are very basic evaluations for summarization.

---

## What's your take on using RAG for report generation in response to requests for proposals?

The expert on report generation will talk in Week 4. Look out for a talk from Vantager, who does this for financial due diligence. Companies can give them existing reports, which they parse into a spec, and then when you upload new PDFs, it automatically generates a report for you.

There's a lot of economic value that can come from report generation, and it's probably more valuable than just doing generic question answering.

---

## What is your experience using reasoning models as the answer generator model?

Before there were specific reasoning models, I've been pushing everyone to at least have thinking tokens and a reasoning block in the output. This gives language models time to think and allows you to render in a way that minimizes perceived latency.

Now that O1 and DeepSeek are available, unless latency is a concern, I would try to use these reasoning models. O3 Mini is fairly affordable, and O1 is very affordable. You can render the product in a way that makes users feel it's faster.

DeepSeek's reasoning capability is one reason it stood out to people—they can actually see it think. For many practitioners, we've been asking language models to think step by step for quite a while.

---

## How do we set user expectations on the delay while using reasoning models?

The first UI tip is to stream out the thinking part of the model to the customer. Things will feel about 45% faster just because something is moving on the page.

The second approach, which DeepSeek does well, is to have a button called "Think harder" or "Reasoning." If users don't use it, they get the faster V3 model, but if they press reasoning, it switches to the R1 model. This both tells users you want the model to think (which they know will be slower) and, by rendering the thought tokens, improves the perceived latency.

---

## How should we handle multiple RAG sources with different levels of information?

When you have multiple RAG sources (like a calendar and a news site with more detailed event information), it can slow down the system when you want to use an LLM to act as a judge and provide a holistic answer.

One approach is to predict what types of questions are easy versus hard and route them effectively. Another approach is to improve the user experience by rendering sources before rendering the text. Show an animation like "I am thinking" and have document 1, 2, and 3 appear, then "I'm reading," and finally the answer.

Notion AI's UX does this well—it says "thinking about your question," "searching documents," animates the documents coming in, and then starts talking. The key is to keep the screen moving to make users believe something is happening.

Adding a loading screen that moves can make users feel the system is 30% faster, even if the actual processing time is the same.

---

## What strategies can help when there are negative consequences of "thinking too hard" with reasoning models?

One approach is to predict whether a question is easy or hard and decide when to turn on thinking. You could use a model like BERT to classify this.

If that's possible, you can make the decision to think on behalf of the user. The objective would be to maximize customer satisfaction while minimizing token costs.

Some companies like have their own proprietary model that tells you which is the best model to route to. You could have a model that's trained so that if you ask "what's 1+1," it sends that to a simpler model, but if you ask about reading a legal document, it routes to an R1 model.

For evaluation questions specifically, it really depends on the complexity. Some evaluations are simple yes/no decisions, while others involve complex reasoning like assigning the correct speaker to different comments in a transcript. You'll need to test with your specific use case.

---

## What advice would you give for introducing LLMs into a healthcare company that may not fully grasp their potential?

First, build a demo and let leadership see the results. Then, clearly identify what types of queries you won't attempt to answer, pre-loading all the risk discussions upfront.

Instead of saying "my model is 80% correct," say "I've identified the 20% of questions that don't work at all, but for the 80% of questions we can solve, the success rate is 99%."

Do the upfront work to know the failure modes and economically valuable opportunities, then present them clearly. Add guardrails to say what the LLM won't attempt to do. Much of this is about setting expectations for leadership.

---

## Are there open source re-ranking models that come close to Cohere's re-rankers in quality?

There are definitely good cross-encoders available, though some of the top models on leaderboards are 7 billion parameters, which may have high latency.

Modern BERT (a new BERT-based embedding model with about 8,000 token sequence length compared to the original 512) will likely lead to more powerful BERT-based re-rankers.

However, training your own re-ranker on your specific data will likely beat benchmark models. With just 6,000 examples from your own data, you can train a better embedding model and cross-encoder than what's publicly available, costing around $1.50 and 40 minutes on a laptop.

---

## Outside of personal experiments, what resources or mediums do you rely on to stay up to date on RAG?

Much of the content coming out is very hypey, and many research papers focus on public evaluations that don't mean as much as more fundamental work on data analysis, experimentation, and evaluation.

When reading papers, focus more on how they present results and think about experimentation rather than specific methodologies or implementations. The things that work well are often too maintenance-heavy or expensive for production use cases with millions of PDFs.

I like Anthropic's blog posts because they're fundamental—discussing how to think about error bars, clustering, and other approaches that everyone can use, not just researchers with 40,000 rows in a database.

Outside of that, a lot of information is in private Discords and Twitter. I'll have someone make a summary of the Discords with interesting "alpha" or insights.

---

## When working with documents with metadata, should search and retrieval methods change based on the level of metadata provided within the queries?

Yes, they should. For example, in a construction project, we found people really cared about who made the last edits on legal contracts or who sent particular information. The metadata was very important—queries like "which contracts did this person send us" become like SQL queries.

We learned that when answering questions about who's doing what, we should include their contact information. These are small details in improving a RAG system that create economic value.

Similarly, if you're building information that will be queried across time periods, you probably care about when documents were published and last crawled to determine relevance. A query like "what is the latest research in physics" might look at the past 6 months, while "what is new in AI" might only look at the past two weeks because it moves so quickly.

It comes down to analyzing the queries people are asking and figuring out what creates economic value.

---

## Do you know if Anthropic is working on an answer to O1 or R1 (reasoning models)?

Yes and no. If you use Claude's web app, it secretly has thinking tokens. Every time it says "pondering" or "thinking," it's actually outputting thinking tokens that you can't see.

If you ask Claude to replace the <antThinking> token with {anyThinking}, you'll start seeing those thinking tokens. You can request this token in the API as well.

The real question is whether Anthropic has thinking models that use RLHF, and I'm not fully sure about that. Their CTO has stated they don't do distillation, but there are mixed interpretations of what that means.

Claude 3.5 Sonnet is still impressive even without visible reasoning, including its vision capabilities. The bigger issue is that Anthropic is very concerned about safety and has questions about whether thinking tokens could lie to users or follow different policies.

---

## When working with unstructured data, mostly PDFs and drawings, how do you approach data labeling and what models do you use?

For unprocessed data, I look at companies like Llama Parse, Extend, and Reducto, which parse headers, bodies, tables, and figures so you can work with them separately.

For the most part, Claude Sonnet does a very good job—it's just a matter of how much data you need to process. For specific tasks like understanding figures, visual language models like Qwen via Ollama work well for single PDFs, though batch local processing is more challenging as tools like VLLM don't yet support these models.

---

## Why does this course favor LanceDB versus other vector databases?

The main reason is that I want everyone to experience running evaluations on not just embedding search but also full-text search. I want you to try hybrid search with or without a re-ranker.

With LanceDB, incorporating these approaches is just one extra line of code. You can do a search with different modes (lexical, vector, hybrid) and easily add a re-ranker. It's the simplest way to try all these combinations and discover what works best.

Additionally, LanceDB is backed by DuckDB, which means the same database that supports full-text search, semantic search, and re-rankers also supports SQL. If you want to analyze your queries with SQL, you can do that easily.

Another advantage is that LanceDB can be hosted on S3 and is easy to set up for large amounts of data.

---

## Which industry or application domain do you think is most difficult for LLMs?

It's hard to say definitively, but generally:

1. Tasks with complex images are difficult
1. Highly regulated industries like legal and healthcare contexts present challenges
1. Financial services, especially ratings agencies, face enormous regulatory hurdles

The fundamental challenge is that anything difficult for humans to collect data on will be hard for an LLM. It's about how much volume of data we have per industry and what kind of feedback loops exist.

If an LLM makes a decision that takes weeks to verify, it's going to be hard to improve. The timeline for regulatory approval in some industries (like ratings agencies) can be years, creating a massive barrier to implementing LLM-based solutions.

---

## Did you find a use case where re-rankers improve metrics?

Almost every case I've seen shows improvements with re-rankers, whether it's legal documents, question answering over books, or financial documents. A Cohere re-ranker typically improves performance by 6-12% while adding about 400-500ms of latency.

Companies like Cohere are building industry-specific rankers that support financial text, medical text, and code. They're working hard to beat OpenAI embeddings, and they generally succeed.

Re-rankers solve problems that embeddings miss, like distinguishing between "I love coffee" and "I hate coffee," which look similar in embedding space but are clearly different with cross-attention in a re-ranker.

---

## Can you share resources on how to create hybrid embeddings for PostgreSQL vector databases?

If you use a library called ParagraphDB, you can set up both sparse BM25 indices and dense embedding-based indices. This allows you to implement rank fusion.

Pinecone has good resources about this topic that I can share.

---

## For medical/healthcare administration, how can we get LLMs to be something that are trustworthy with serious decisions?

One approach is to use chain of thought models where we can read the reasoning to understand how the model arrived at a decision. Anthropic's concern may be that the chain of thought could be misleading.

There's likely a future where we can build UIs that let humans verify not only the decision but also the chain of thought behind it. Then we can train models so that even the reasoning aligns with user preferences. If a model gets the right answer but with faulty reasoning, that's where we'd provide feedback.

Another approach is to use ensembles—sample a suite of LLMs and use majority voting on decisions to establish confidence. I often train multiple smaller language models to grade things on a 0-1 scale, then use a classical ML model (like logistic regression) to make the final prediction. This helps with explainability because you can see which features influenced the prediction.

---

## For multimodal retrieval (text + images), what approaches work best?

For visual content like photographs, CLIP embeddings work well since they're inherently multimodal—they can represent both images and text in the same embedding space.

For instructional manuals with images, I'd pass the images to a language model and ask for a detailed summary of what the image shows, including all text in the image. Then embed that summary instead. This creates a text representation that points to the original image.

The approach has two steps:

1. Given an image, create a synthetic question that would retrieve it
1. Create a summary that would be retrieved for that question

For product marketing scenarios, CLIP embeddings can work well, but you need to define what "similar" means in your context. Does a red shirt match other red shirts, or just shirts of the same color? Should expensive silk shirts match inexpensive polyester versions?

This is why fine-tuning embedding models to understand your specific definition of similarity is important.

---

## How do you approach chunking very long documents (1,500-2,000 pages)?

If you have extremely long documents, I'd first try a page-level approach to determine if answers typically exist on a single page or span multiple pages.

One compelling approach is from a paper called RAPTOR. After chunking documents, they recluster the chunks. You embed every page, run a clustering model, and identify concepts that span multiple pages. Then summarize those clusters and use the summaries for retrieval—if the summary is retrieved, you can include all related pages in the context.

For metadata, look at your queries to determine what matters. If users frequently ask about publication dates or document authors, those should be included. The needs will become obvious as you analyze user queries—you'll realize what's important and what creates economic value.

Generally, if you can reorganize text chunks by clustering and bringing related information together, that's very valuable. For example, with tax law documents where laws are on pages 1-30 and exemptions on page 50, you could process the document once to place exemptions directly below the relevant laws. This preprocessing step might cost $10 of LLM calls per document, but for legal documents that might not change for years, it's worth the investment.

---

## Do you have a go-to approach for visual document image embeddings (like quarterly reports with tables, images, graphs)?

For visual documents like quarterly reports full of tables and images:

1. Dockling is a free library that works quite well, though it might take about 11 seconds per PDF
1. Claude Sonnet also works well for extraction
1. Reducto, Llama Parse, and other commercial tools can be worth the cost to save time
1. For multilingual content, VDR2B-Multi v1 handles multiple languages well

There's an ongoing discussion about using Gemini 2 (with its million-token context window) to convert documents to markdown and extract all the information. This approach is becoming more viable as models improve, potentially reducing the engineering needed for preprocessing.

Recent testing shows Reducto still has higher accuracy (0.9 ± 0.1) compared to Gemini (0.84 ± 0.16), but the gap is narrowing. The reason Reducto performs so well is that they have people manually labeling thousands of PDFs to train their models.

---

## Why at Meta did you prefer SQL databases over graph databases?

Graph databases are useful when you need complex traversals, like finding all of Jason's followers who follow a specific account, then finding what they like, and sorting by aggregated likes per product.

However, what we found is that most use cases are actually simpler—often just requiring 2-3 left joins in SQL rather than complex graph traversals. From a skills perspective, it's easier to hire people who know SQL well than to find graph database experts.

At scale, graphs are also hard to manage. Around 2017-2018, only LinkedIn had a true graph database because they needed to compute 3rd-degree friendships very quickly. For most companies, SQL databases offer better performance, easier maintenance, and more familiar tooling.

Over a 12-year career, we kept trying different technologies (Hadoop, Spark, etc.) but always ended up returning to SQL. The pattern is consistent across many organizations.

---

## What have you learned about prompt caching?

Prompt caching is a technique where language models can avoid reprocessing the beginning of prompts that are often identical.

Different providers handle this differently:

- Anthropic caches prompts for 5 minutes; if you make the same request within that time, the entire message is cached
- OpenAI figures out the optimal prefix to cache automatically

This is valuable because it can save significant processing time and costs, especially when you have many few-shot examples or large system prompts. If you have 50+ examples in your prompt, caching can dramatically improve performance.

For models like Claude on Bedrock, prompt caching wasn't available a few months ago but is likely coming soon. It's the kind of feature that rolls out gradually across providers.

---

## For visual document image processing, what's the state of the art?

There's a recent discussion on Hacker News about using Gemini 2 (with its million-token context window) to process documents and convert them to markdown, extracting tables, layout information, and text.

The engineering needed for document pre-processing is getting simpler as these models improve. Recent tests show Reducto still has higher accuracy (0.9 ± 0.1) compared to Gemini (0.84 ± 0.16), but the gap is narrowing.

Reducto's performance comes from having people manually label thousands of PDFs, then training models on that high-quality data. This reinforces the point that with 6,000-10,000 high-quality labels from your own data, you can train models that outperform even the biggest general models on your specific tasks.

---

## How does Brain Trust work with the notebooks in this course?

Brain Trust just saves the results that your laptop is running locally. It's not executing anything or using a better database—it's more like an observability tool (similar to Datadog).

When we run the notebooks, everything is running on your laptop in LanceDB. The only thing Brain Trust sees is row IDs and scores. Think of it as a powerful UI over a database that's saving your logs, not as a computation service.

---

## What's the difference between bi-encoders and cross-encoders?

A bi-encoder converts all documents into numbers (embeddings) first, and then the assumption is that when we compare those numbers, documents that look similar are similar. Because we pre-compute everything, we can search very quickly.

A cross-encoder doesn't compare numbers—it compares the actual sentences. This approach can't compare a million documents with a million other documents (too expensive), so instead it takes one question and 50 documents and compares each one individually. That's the "cross" part of cross-encoder.

The advantage of cross-encoders is that a language model can compare words like "love" and "hate" in "I love coffee" and "I hate coffee" and understand they're different, whereas bi-encoders just have lists of numbers that don't capture this nuance.

We'll cover this topic more deeply in Week 2, but the key takeaway is that bi-encoders are faster but less accurate, while cross-encoders are slower but better at understanding semantic distinctions.

---

## What's the process for fine-tuning embedding models?

In Week 2, we'll cover this topic extensively. The overall message is that:

1. It's probably a bad idea to train your own language model
1. It's a very good idea to train your own embedding model

Fine-tuning embedding models is much less resource-intensive—it typically costs around $1.50 and takes about 40 minutes on a laptop. With just 6,000 examples from your domain, you can train embedding models and cross-encoders that outperform general-purpose models on your specific tasks.

This is especially useful when you need embeddings to understand domain-specific concepts or when you're trying to define what "similar" means in your particular context (e.g., product recommendations where price range matters).

---

## How do you understand metrics like precision and recall in one-to-one answer scenarios?

For questions with exactly one correct answer, these metrics behave somewhat differently. Recall will be either 0% or 100% depending on whether K is large enough to include the correct answer.

For example, if we want to retrieve exactly one document and there's only one correct answer, precision could be either 0% or 100%, and the same for recall.

The metrics become more meaningful when:

1. There are multiple relevant documents
1. We're analyzing trends across many queries
1. We're comparing different retrieval methods

Even with one-to-one mappings, MRR (Mean Reciprocal Rank) is still useful to see where the correct answer appears in your results.

What really matters isn't the absolute number but whether we can move these metrics in a positive direction with our interventions. It's like weighing yourself—the absolute number may vary by scale, but if you've gained two pounds, you've definitely gained two pounds.

---

IF you want to get discounts and 6 day email source on the topic make sure to subscribe to

<script async data-uid="010fd9b52b" src="https://fivesixseven.kit.com/010fd9b52b/index.js"></script>

---

## How would you evaluate the effect of different parsing strategies in RAG, notably on documents with weird layouts, tables, and charts?

For documents with complex layouts like tables and charts, there are multiple levels of evaluation:

First, you need to evaluate OCR accuracy - checking whether text is being parsed correctly (e.g., is a 0 being parsed as an 8?). Then there's the bounding box detection problem - checking if tables are fully recognized as single bounding boxes using metrics like intersection over union.

It's generally safer to evaluate OCR/parsing and retrieval separately because parsing errors can be hard to trace back when they're part of the full RAG pipeline. If you parse an 8 as a 0 and generate synthetic data from that, you won't be able to capture that error in your evaluations.

I've leaned on parsing vendors because they're the most incentivized to have good and accurate labels. This lets me focus on retrieval, which is what will create the most value for my specific use case. While there are other businesses focused on PDF processing, no one will focus specifically on your ability to do retrieval well with your data.

---

## When does it make sense to create a targeted summary for an application's objective versus fine-tuning embedding models?

This depends on whether you have data to fine-tune and what your embedding should capture. If you're writing the summary yourself, you're essentially making an assumption about what the embedding should look like.

For example, with image embeddings, maybe the most common questions aren't just about what's in the photo but about the cinematic mood. In that case, it might make sense to have a language model create a summary describing the mood because I want to be able to search for "atmospheric" or "dark and gloomy" rather than just "trees in a forest."

However, if you have actual user interaction data, it's better to use that data to tell us what's similar rather than creating assumptions. For example, with blueprint images, an image model might just say "this is a blueprint," but what I specifically did was extract information like number of rooms, bathrooms, sizes, and addresses - information that would be harder for a CLIP embedding to capture.

In general, I'd much rather use the data my app generates than hard-code these summaries, but summaries can be useful when you need to extract specific structured information that embedding models might miss.

---

## What are the recommended approaches for evaluating RAG for single documents, like report generation for a proposal?

When working with a single PDF document that might be varying in length (from 10 to 400 pages), semantic chunking can be valuable to separate paragraphs based on their semantic meaning rather than just token-based chunking. This is especially important when requirements for different disciplines might be found in different sections (e.g., structural requirements mentioned within architectural requirements).

One approach is to generate synthetic questions per paragraph, asking "What are the requirements being mentioned in this paragraph?" rather than "What question can you ask from this paragraph?" This helps identify the key information.

For retrieval, you can also inject a summary of the page that a paragraph was extracted from and embed them together. This way, when retrieving, you have both the specific chunk and context about where it comes from, which can improve recall.

Whether adding summaries improves recall is an empirical question - if it increases recall by 1%, it might not be worth the extra LLM calls, but if it improves recall by 6-8%, it could be worth investigating further.

---

## Could you distill key reasons when someone should consider fine-tuning open source embedding models over proprietary models?

If you have 6,000-10,000 examples of question-document relevancy pairs, you can likely outperform closed-source models with a fine-tuned model. This is because your tasks can be much more specific than what general models are optimized for.

It can also be more valuable if you need to embed massive datasets at scale. By spinning up your own GPUs, you can process much more text per second at a lower cost. For example, embedding 20GB of text data might take only 15 minutes and cost around $20, whereas using OpenAI APIs would be more expensive and much slower.

The main downside is the need to maintain your inference server, which adds complexity. It's less about whether the model will perform well and more about whether you have the time and resources to maintain the infrastructure.

---

## Is there a reason to ever fine-tune the LLM rather than or in combination with fine-tuning the retriever model?

I'm pretty open to businesses fine-tuning their retrieval models because companies like OpenAI or Anthropic aren't primarily focused on making retrieval better - they're not launching new embedding models daily. Companies like Cohere, on the other hand, are actually thinking about retrieval.

If you spend effort fine-tuning an LLM, you need to consider inference, CUDA drivers, and whether your fine-tuned model will be competitive when the original model provider releases a new version in a few months.

It's generally very costly to fine-tune language models, and you often don't get much benefit. However, if there are specific reasons - like tonality, personalization, or access to proprietary data - it might make sense. But for a team of 4-5 people, it's probably not a good idea to spend effort maintaining that kind of infrastructure.

In contrast, fine-tuning embedding models can be done on a laptop, run on cloud instances, and be cost-effective. For most teams, the maintenance cost of running your own LLM is just too high to justify.

---

## One weakness of RAG is difficulty in detecting relationships between concepts because the retriever model isn't aware of how concepts relate to each other. Should we fine-tune the LLM for this?

Before considering fine-tuning the language model, I would ask: How much can we put into few-shot examples in the prompt? Can we come up with good chain-of-thought examples that describe these relationships? Can we provide a glossary?

The maintenance cost of running an LLM is so high that it's worth really trying to squeeze out as much as possible through prompt engineering, longer system prompts, more few-shot examples, and prompt caching before considering fine-tuning.

For example, Bloomberg spent millions on their own model, and within 5-6 months, GPT-4 was better. Instead of fine-tuning, consider using RAG to retrieve relationship information first, put that in the context, and then add the actual question. This is more maintainable and adaptable as new models are released.

---

## What is the main failure modes (like distribution mismatch or biases) that you've seen when relying on synthetic data for retrieval fine-tuning?

The biggest issue is mismatch between user questions in reality versus in the synthetic data. Once you have synthetic data for fine-tuning retrieval models, it's hard to imagine a case where creating more data for your use case would make the model worse.

What's more important is figuring out how to intelligently incorporate real-world examples from users into the few-shot examples for synthetic data generation, making it a more diverse process. You can check this by:

1. Looking at the variance of embeddings against each other to see if they're too similar
1. Checking general statistics like character count variance in questions
1. Ensuring the synthetic data matches user data characteristics

For example, if your customer questions typically have around 30 characters but your synthetic data averages 90 characters because the language model is too verbose, that's a simple distribution mismatch to fix.

---

## Can you share the intuition for the difference between a fine-tuned embedding model and a fine-tuned re-ranker?

The embedding model allows you to do search over a large number of documents - given an embedding model, you might retrieve the top 100 text chunks. The re-ranker model then takes these 100 chunks and finds the best 25.

We generally want to use both, and the dataset to train these models is actually the same dataset. If you can only afford to fine-tune one, you might choose based on where your bottleneck is:

1. Is recall at 100 already good (95%) but recall at 10 is poor (50%)? Then focus on the re-ranker.
1. Are you missing relevant documents even in your top 100 results? Then focus on the embedding model.

The key insight is that by having metrics on both stages, you can identify where to focus your improvement efforts.

---

## Do we need more data to fine-tune re-rankers than bi-encoders?

It depends on the model, but generally, Cohere has done a good job of being data-efficient for producing embedding models. The amount of data needed may vary by model and task.

---

## For collaborative filtering models, how do you address the cold start problem (new users/items the model hasn't seen) without retraining the model?

There are multiple approaches to this. Instead of using classical collaborative filtering models, many systems now build models with user embeddings and item embeddings. The question becomes: can we use some other model to predict the embeddings we would have trained using interaction data?

For example, in an e-commerce setting, if we trained our item embeddings using purchase data and a new item comes in, we could train a vision model to predict the embedding of the item based on its image and metadata. We can use that as an initial set of recommendations.

The core idea is using other available data to predict the embeddings that would have come from interaction data (like checkout data). This approach helps bridge the gap for new items or users.

---

## How do you handle RAG for multimodal content like PowerPoint presentations that have complex layouts?

For documents with complex layouts like PowerPoint presentations, the parsing and chunking processes are linked. You might want to evaluate them separately since parsing errors will be hard to detect in the full RAG pipeline.

One approach is to use general-purpose parsing tools like Dockling, Claude Sonnet, or commercial tools like Reducto, Llama Parse, and Extend. For multilingual content, models like VDR2B-Multi v1 handle multiple languages well.

Recent developments include using models like Gemini 2 (with its million-token context window) to convert documents to markdown and extract information, though specialized tools like Reducto still have higher accuracy (0.9 ± 0.1 vs. 0.84 ± 0.16 for Gemini). These gaps are narrowing as general models improve.

---

## Why did you prefer SQL databases over graph databases at Meta/Facebook?

Graph databases are useful when you need complex traversals, but most use cases only require 2-3 left joins in SQL rather than complex graph operations. From a skills perspective, it's easier to hire people who know SQL well than to find graph database experts.

At scale, graphs are also hard to manage. Around 2017-2018, only LinkedIn had a true graph database because they needed to compute 3rd-degree friendships very quickly. For most companies, SQL databases offer better performance, easier maintenance, and more familiar tooling.

Over a 12-year career, we kept trying different technologies (Hadoop, Spark, etc.) but always ended up returning to SQL. Most cases don't require more than one or two traversals of your graph, making SQL a more practical choice.

---

## What have you learned about prompt caching?

Prompt caching is a technique where language models can avoid reprocessing the beginning of prompts that are often identical:

- Anthropic caches prompts for 5 minutes; if you make the same request within that time, the entire message is cached
- OpenAI figures out the optimal prefix to cache automatically

This is valuable because it can save significant processing time and costs, especially when you have many few-shot examples or large system prompts. If you have 50+ examples, caching can dramatically improve performance.

For models like Claude on Bedrock, prompt caching wasn't available a few months ago but is likely coming soon. It's the kind of feature that rolls out gradually across providers.

---

## What's the difference between bi-encoders and cross-encoders?

A bi-encoder converts all documents into numbers (embeddings) first, and then compares those numbers. Because we pre-compute everything, we can search very quickly.

A cross-encoder doesn't compare numbers—it compares the actual sentences. This approach can't compare a million documents with a million other documents (too expensive), so instead it takes one question and 50 documents and compares each one individually.

The advantage of cross-encoders is that they can understand semantic distinctions like the difference between "I love coffee" and "I hate coffee," whereas bi-encoders just have numeric representations that might miss this nuance.

Bi-encoders are faster but less accurate, while cross-encoders are slower but better at understanding semantic distinctions.

---

## What's the process for fine-tuning embedding models?

It's probably a bad idea to train your own language model, but it's a very good idea to train your own embedding model.

Fine-tuning embedding models is much less resource-intensive—it typically costs around $1.50 and takes about 40 minutes on a laptop. With just 6,000 examples from your domain, you can train embedding models and cross-encoders that outperform general-purpose models on your specific tasks.

This is especially useful when you need embeddings to understand domain-specific concepts or when you're trying to define what "similar" means in your particular context (e.g., product recommendations where price range matters).

---

## What non-intuitive things have you learned about recommendation systems?

The big insight about recommendation systems is that inventory matters a lot more than the actual algorithm. While Tiktok's algorithm is good, what really allows it to produce great recommendations is the vast amount of content available. Without those videos, you can't do much - and the same applies to RAG.

The metadata you have and the inventory you have are much more important than the algorithm itself. For example, if recommendations for "Greek restaurants near me" are bad, the solution might be to add more Greek restaurants to your database, not to tweak the algorithm.

Similarly, if queries after 7 PM perform poorly, maybe you're missing information about whether restaurants are open. The solution is to collect that data rather than change your algorithms.

The hard work in recommendation systems is often: Do we have enough rows in the database? How much content do we have? And for that content, do we have the right metadata?

---

## When working with documents with metadata, should search and retrieval methods change based on the level of metadata provided within the queries?

Yes, they should. For example, in a construction project, we found people really cared about who made the last edits on legal contracts or who sent particular information. The metadata was very important for queries like "which contracts did this person send us," which function more like SQL queries.

Similarly, if you're building information that will be queried across time periods, you probably care about when documents were published and last crawled to determine relevance. A query like "what is the latest research in physics" might look at the past 6 months, while "what is new in AI" might only look at the past two weeks because it moves so quickly.

It comes down to analyzing the queries people are asking and figuring out what creates economic value.

---

## Do you have a go-to approach for visual document image embeddings (like quarterly reports with tables, images, graphs)?

For visual documents like quarterly reports full of tables and images:

1. Dockling is a free library that works quite well, though it might take about 11 seconds per PDF
1. Claude Sonnet also works well for extraction
1. Commercial tools like Reducto, Llama Parse, and others can be worth the cost to save time
1. For multilingual content, VDR2B-Multi v1 handles multiple languages well

Recent testing shows Reducto still has higher accuracy (0.9 ± 0.1) compared to Gemini (0.84 ± 0.16), but the gap is narrowing. Reducto performs well because they have people manually labeling thousands of PDFs to train their models.

---

## How do you handle multilingual RAG?

Cohere has put the most effort into multilingual models, with both multilingual local LLMs and embedding models.

I recommend figuring out which languages appear in your queries and ensuring your evaluation reflects that distribution. Check whether the models you're considering (Cohere, OpenAI) perform well on these languages.

While translation might seem like an option, if it worked well, companies like OpenAI and Cohere would already be using synthetic translation data to improve their language models. To evaluate performance across languages, create synthetic questions in multiple languages and verify whether recall rates differ between languages.

---

## How do you approach chunking very long documents (1,500-2,000 pages)?

If you have extremely long documents, start with a page-level approach to determine if answers typically exist on a single page or span multiple pages.

One compelling approach is from the RAPTOR paper. After chunking documents, they recluster the chunks by embedding every page, running a clustering model, and identifying concepts that span multiple pages. Then they summarize those clusters and use the summaries for retrieval—if a summary is retrieved, all related pages are included in the context.

For metadata, look at your queries to determine what matters. If users frequently ask about publication dates or document authors, those should be included. The needs will become obvious as you analyze user queries.

If you can reorganize text chunks by clustering and bringing related information together, that's very valuable. For example, with tax law documents where laws are on pages 1-30 and exemptions on page 50, you could process the document once to place exemptions directly below the relevant laws. This preprocessing step might cost $10 of LLM calls per document, but for legal documents that might not change for years, it's worth the investment.

---

## How do you understand metrics like precision and recall in one-to-one answer scenarios?

For questions with exactly one correct answer, these metrics behave somewhat differently. Recall will be either 0% or 100% depending on whether K is large enough to include the correct answer.

For example, if we want to retrieve exactly one document and there's only one correct answer, precision could be either 0% or 100%, and the same for recall.

The metrics become more meaningful when:

1. There are multiple relevant documents
1. We're analyzing trends across many queries
1. We're comparing different retrieval methods

Even with one-to-one mappings, MRR (Mean Reciprocal Rank) is still useful to see where the correct answer appears in your results.

What really matters isn't the absolute number but whether we can move these metrics in a positive direction with our interventions.

---

## How does a long context window affect RAG systems?

While having longer context windows allows for more content to be included, there are always tradeoffs with latency and cost. Just because we can fit more in context doesn't mean we should always do so.

Like how Amazon could theoretically score every product in their inventory for each user but chooses not to because each 100ms of latency costs them 1% in revenue, we still need to make choices about what to include in context.

The battery analogy is apt: iPhone batteries get more powerful every year, but battery life stays the same because we build more power-hungry apps. Similarly, as context windows grow, we'll find ways to use that additional capacity rather than making everything faster or cheaper.

There will always be cost, performance, and latency tradeoffs to consider. Having a longer context window doesn't eliminate the need for efficient retrieval - it just changes what problems we can solve.

---

## What tips do you have for making decisions about RAG system architecture without prototyping everything?

Start by asking for examples of 40-50 questions that customers might ask. Reading these helps build an intuition about what query mechanics need to exist.

For example, if questions include "what's the most recent news?", you'll need date filters. If queries ask "who do I talk to about fixing XYZ?", you need features for finding contacts.

This helps identify what metadata you need and whether you can access it. From there, building a demo with tools like LangChain or Llama Index should be quick. You may need to rewrite things later, but if the demo can answer generic questions, that's when you start thinking about synthetic data.

The key is getting the system in front of beta testers, collecting feedback, and analyzing what's working and what's not. This helps prioritize the next features to build. If 80% of questions are actually about image search, then that's clearly the next thing to build, regardless of what methodology is trending on Twitter.

---

## How do you optimally blend small pools of real data with large synthetic data sets?

Focus on whether blending improves your evaluation suite. If you have 500 real examples, put 250 in your training set and leave 250 for evaluation. Then experiment with different blends of synthetic and real data to see how they perform on your evaluation suite.

You might find that as you use more synthetic data, you perform worse on your real user data but better on synthetic data. You can weight these differently - perhaps real data success is worth 1.2 points while synthetic data success is worth 0.9 points - to create a single score for system health.

A lot of machine learning is empirical - you can't predict these things ahead of time. You need to run experiments and see what works.

---

## How do you approach function calling for complex workflows that require multiple function calls?

Instead of having the language model immediately execute functions one at a time, prompt it to show the entire plan to the user and potentially ask for confirmation. Have a separate function called "plan" where the model says "Based on this request, I think I'm going to use function 1, then 2, then 3. What do you think?"

When the user clicks yes or no, you've allowed human confirmation of the correct order. Since the plan already exists in the context, it's easier for the model to execute correctly.

The second benefit is that user requests, plans, and accept/reject decisions can be used as few-shot examples. You can embed these examples so that next time someone asks a similar question, you can say "Last time someone asked this, they approved calling functions 1, 2, 3 in this order."

This helps build a dataset of few-shot examples over plans, making the system more reliable.

---

## How do you constrain a RAG system that pulls from multiple data sources?

After conducting topic analysis of user questions, you can identify which types of questions you can answer well and which ones you struggle with. For low-percentage, low-performance questions, you might decide to simply decline those queries.

For example, if your system doesn't handle contact information well, you could add to your prompt: "If someone is asking about contact information, say no and tell them to message support." This saves face and avoids attempting questions you can't answer well.

Conversely, if there are questions you can answer very well (even if they're a small percentage), highlight these as sample questions in your UI to guide users toward queries you're confident in handling.

Much of the progress in making systems better comes from improving UI, better educating users about capabilities, and enhancing the quality of your inventory rather than just tweaking algorithms.

---

## Do you sometimes use differently tuned embeddings within the same query?

Unless you're at massive scale, having multiple embedding models for different content types (like product descriptions vs. comments) probably won't yield enough performance improvement to justify the maintenance cost.

There's evidence that having a single unified model trained on all your data performs better than specialized models. In machine translation, we used to train separate models for each language pair, but researchers found that a single model trained to translate all languages performed better than any individual model.

The unified model learns something about the underlying system that allows it to handle even rare cases better than specialized models would. The same principle likely applies to embedding models.

---

## How do you reason about papers and new research in RAG and LLMs?

Most papers published weekly aren't that important, and many are just reinventing ideas from decades ago. Instead of flooding yourself with information, focus on running experiments with your own data and solving specific problems.

The popular stuff on Twitter is generally reasonable to follow, but even then, much research is a distraction if you're building something. For example, a recent popular paper on "reasoning powered RAG" was essentially just using an LLM to judge relevancy pairs in a for loop - something basic that's been around for a while.

Rather than chasing the latest research, focus on building strong evaluation suites, analyzing your data, and solving specific problems in your implementation. These are the durable skills that will last throughout your career.

---

## Does a long context window make RAG obsolete?

No. Just like Amazon could theoretically score every product in their inventory for each user but chooses not to because each 100ms of latency costs them 1% in revenue, we still need to make choices about what to include in context.

The battery analogy is apt: iPhone batteries get more powerful every year, but battery life stays the same because we build more power-hungry apps. Similarly, as context windows grow, we'll find ways to use that additional capacity rather than making everything faster or cheaper.

There will always be cost, performance, and latency tradeoffs to consider. Having a longer context window doesn't eliminate the need for efficient retrieval - it just changes what problems we can solve.

---

## How do you handle the upkeep of documents that go in and out of scope or have frequent version changes?

For "evergreen" vs. "Rhodian" (frequently changing) documents, include published dates and make sure they're in the context so the language model is aware of them. For example, with HR holiday calendars for different years, include the dates so the model can reason about which is current.

Consider implementing both published dates and last modified dates, and be explicit in your function calling to filter on these attributes (e.g., only return documents published or updated in the past year).

The key question is how sensitive your model is to low precision, and whether that low precision is mainly happening because of your inability to expire outdated documents.

---

## How do you approach building voice AI for outbound calls or structured conversations?

Graph-based models or finite state machines have been very successful in the agent world. In this approach, you're in different states (introduction, data collection, etc.) with different system messages for each state.

For example, when collecting payment data to book a meeting, you have logical checks to ensure the date is correct and that you have necessary information like a phone number. The set of function calls available also changes based on the state.

Once you have fully successful conversations, you can summarize them and put them back in the system prompt to ensure transitions are more accurate. You can prompt the model with these few-shot examples to improve transition states: "When I have 5 few shots, my transitions are more accurate. When I have 20 few shots it gets too confused. So now I've picked 15 for now."

This finite state machine approach has been around for decades and is still very effective, with LLMs improving the transitions between states.

---

## When working with metadata, should you include it in the chunk or add it separately?

There are a few approaches:

1. Embed the string without metadata but add metadata when sending to the LLM
1. Embed the string with metadata included

This is something to test empirically - does including metadata in the embedding hurt retrieval? Cohere's embedding models (like Compass) can embed JSON quite well.

Including metadata in chunks is common practice as it allows answering questions like "who wrote this document" or "what's their contact information." This metadata can then be used for function calls, such as "Jason wrote the document 2 weeks ago, it has not been updated since. Here's Jason's email, click to write an email to Jason."

---

## How can you best apply synthetic data generation to agent workflows with multiple tools?

Instead of generating synthetic questions, you can generate synthetic queries that would trigger certain function calls. If you have 3-4 different functions, you can create synthetic queries that should call specific functions or combinations of functions.

If each individual function call is accurate, then the combined sequence should also be accurate. You can also use planning to improve data generation - create questions that would result in specific functions being called in sequence, then verify that with certain requests, these functions are indeed called by the model.

This approach helps ensure reliability across different types of function calling patterns.

---

## Key Takeaways

1. **Fine-tuning priorities**: Fine-tune embedding models, not LLMs. With just 6,000 examples, you can create embedding models that outperform general models on your specific tasks at minimal cost.

1. **Inventory matters more than algorithms**: Having the right documents and metadata is more important than the algorithm itself. Missing information can't be retrieved no matter how good your algorithm is.

1. **Evaluation is empirical**: Many decisions about chunking, including metadata, and blending synthetic data should be driven by empirical testing rather than theoretical assumptions.

1. **Parsing strategy**: For complex documents, consider evaluating parsing/OCR separately from retrieval performance since parsing errors will be difficult to trace in the full pipeline.

1. **Function calling with planning**: For complex agent workflows, have the model create a plan first and get user confirmation rather than executing functions immediately. This creates training data for future interactions.

1. **State machines still work**: Graph-based/finite state machine approaches remain effective for structured conversations, with LLMs improving the transitions between states.

1. **Metadata inclusion**: Include relevant metadata in chunks to answer questions about document properties like authorship, modification dates, and contact information.

1. **Long context doesn't eliminate RAG**: Despite larger context windows, there will always be latency, cost, and performance tradeoffs that make efficient retrieval necessary.

1. **Research pragmatism**: Focus on solving specific problems with your data rather than chasing the latest research papers, which often reinvent existing techniques.

1. **Cross-encoders vs. bi-encoders**: Cross-encoders (re-rankers) understand semantic distinctions better but are slower; bi-encoders (embedding models) are faster but less nuanced. Use both for optimal performance.

---

## Want to go deeper? Get the RAG Playbook

If you're looking to systematically improve your RAG applications, check out the [Systematically Improving RAG &mdash; readers get 20% off with code EBOOK](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button .md-button--primary } course. This 4-week program covers evaluation, advanced retrieval, and building a data flywheel for continuous improvement.

---

## When gathering negative feedback from documents not being found, how do we use and validate the reliability of an LLM labeler?

When it comes to getting negative feedback that documents were not found, I'd assume we're running into issues around low recall. This might manifest as low re-ranker scores or low cosine similarities with embedding models.

What I would do is identify whether the language model itself can identify if documents are irrelevant. We'll need some manual labeling step. With our clients, we generally find questions that emit flags - maybe you tell a language model to always say "we couldn't find relevant documents" when it can't find anything.

You can then label that as traffic is being processed. We might sample 1% of traffic, and some percentage of that might have that message. That's one level of detection.

The second level would be building a streamlit UI where we can manually label whether we agree with the irrelevancy assessment. The hard task is determining if any of 10 text chunks are relevant to a question. The easier task is determining if a single text chunk is relevant to a question. That's easy for a human to do and also pretty easy to prompt for.

This approach helps ensure the judgment we're using is aligned with human preferences. There's obviously a big difference between 60% alignment and 95% alignment, but this is a good start for figuring out whether low relevancy is causing the lack of documents.

---

## In the segmentation topic, we talked about inventories and capabilities. Is it realistic to do this automatically or is it something we have to do manually?

I would generally recommend doing this manually, because it's so important for what your business is trying to do that you need to actually think about these problems.

We've delegated so much thinking to language models. If we just think a bit harder about our problem, we often find very specific issues.

For example, with a client doing tax law resolution, the first 20 pages were massive articles, and then pages 30-40 were the exemptions to those articles. We spent maybe $20 of LLM calls to rewrite the documents so that the exemptions were close to the relevant articles. Now we have a single page/chunk covering an article and all its exemptions, with references to related articles.

We run that job once a week when new tax laws come in. Since we only have about 45 documents we really care about, I'd rather spend the money upfront to get the process right rather than waste customer time requerying data.

The real goal isn't to get a number right - it's to figure out what to do next. The AI can't tell us that. Your job isn't to automate this process; you're being paid to figure out what the next intervention should be.

---

## Can you elaborate on your view on RAG versus recommendations? How would you approach the use case of friend suggestions?

When you build a recommendation system, there are several steps:

1. **Sourcing** - What inventory can I show my customer? In the friends case, this would be all users on the platform.
1. **Query** - Either your user ID or a question embedding.
1. **Scoring** - For simple RAG, this is cosine distance of embeddings and maybe re-ranker distance. For friends, it might include mutual connections, location, etc.
1. **Filtering** - In RAG this might be top 10 results or embeddings greater than a threshold. For friends, filters might include having at least 3 mutual friends, same zip code, etc.
1. **Rendering** the results

When users take actions (adding/removing friends, opening files, deleting citations), you collect feedback to improve your system. When a language model sees 10 documents but only cites 3, those 3 are likely more relevant. You can use that signal to improve your re-ranker or embedding model.

If the user deletes one of those citations, you have a triplet: documents the model thinks are important, plus a negative example. When training, these need to be adjusted accordingly.

It's like different levels of signals in e-commerce: liking a product is a weaker signal than adding it to cart, which is weaker than buying it, which is different from buying and returning it. That's your portfolio of data collected over time.

---

## In the 4th lecture you mentioned the formula expected value as impact times the number of queries, times the probability of success. Can you explain more what you mean by impact?

Impact here is a general term that the Facebook folks like to use. I generally think of impact as economic value.

In the construction example I often mention, about 70% of questions were simple things like "Where do I show up today?" or "How thick is the drywall?" These weren't individually valuable.

But we also found a set of questions that were super valuable - around scheduling and figuring out if contracts were signed. These were only about 10% of queries but extremely important. When we asked our clients, they said that preventing one missed contract could save $60,000 in delays.

This told us these queries had high economic value, even though they were less frequent. So we invested resources in making sure we could query contracts and schedules to answer that segment.

Impact is about how valuable a problem is and how much it's worth, rather than just how frequently it occurs. Every metric you track should enable you to take follow-up action afterward - it's not just about knowing the number.

---

## What is the lifecycle of feedback? If we improve the UI, old labels might be out of date and new data will be labeled differently. What is good to keep versus letting go?

This depends on how much data we have and the blend of that data. If we had a million labels before changing the UI, I'd push hard to keep the new UI somewhat similar to ensure the data we collect remains comparable.

If we're really changing things dramatically, there are modeling techniques to control for this. You might pre-train on the old data for your embedding model, then use that as a foundation for training a newer model. You can also control for the source of data in your modeling.

You can have different evaluations to verify performance on the old data versus the new data, then choose how to weight those scores. Generally, I'd try to keep things as generic as possible - you don't want a dataset that's too specific and won't generalize.

For embedding models specifically, I'd typically include everything, as more data is generally better.

---

## Is it interesting to collect feedback not only as thumbs up or thumbs down, but let users explain in text what is wrong with the answer?

Yes and no. Thumbs up/down is super useful, and it would be hard to convince me not to use these binary labels. Going to a 5-star scale creates issues where you don't know if users consider 3 or 4 stars to be "average."

With free text feedback, you'll face two issues:

1. Probably less than 10% of users will give a text response. If only 1% of users leave feedback at all, and only 10% of those leave text, you get very little text data, and you don't know how biased that sample is.
1. You likely won't be able to read all the free text, so you'll build clustering models to analyze the feedback - in which case, you might as well just have 5 buttons for the most common issues (too slow, answer too long, format incorrect, etc.).

It's about maximizing data per label. Having buttons for common issues will get you more useful data than open text fields.

That said, free text can help you figure out what those buttons should be. For enterprise situations, we include the default buttons plus free text, and when users enter text, we post it to Slack where the team and customer can see it. This shows users their feedback is seen, making them more likely to provide it.

But think about how often you've thumbs-downed a ChatGPT response, let alone written why. Most users simply won't take the time.

---

## How do you handle recall when dealing with large knowledge bases with a messy topology (near-identical documents, overlapping content, hub pages, etc.)?

This is challenging, especially with something like a large software product knowledge base (44,000+ documents) where many people have been adding content, creating overlap and interstitial hub pages.

One approach is to build a system where if you retrieve a subset of pages, you can reference the connections. Similar to how e-commerce sites show "people who viewed this also viewed" suggestions.

As context windows get larger, you could implement a system where if you pull in a page that references other documents, you traverse one level and bring in those referenced documents too.

You could also do clustering and summarization. If your repository is very valuable, maybe it costs 10 cents to process a page, but with a budget of 50 cents per query, you could chunk everything, cluster similar content, and then summarize the clusters. This essentially rewrites the knowledge base in a less duplicated way.

The more fundamental question is about how you define relevance. Do you have a policy document on what makes a document relevant? Google has a detailed document on what makes a good search result. You need to establish and document your criteria so everyone has the same understanding.

---

## Have you compared the effectiveness of classical and agent-based RAG systems with capabilities offered by models like Gemini Flashlight for real projects?

I prefer not to think about systems as "classical" versus "agent-based" RAG systems. Most RAG systems are essentially function calling in a for-loop or while-loop.

The goal is to provide the language model with two things:

1. Good functions
1. Good indices for each function to query that are well-defined

You want to ensure each index has good recall, each function is useful for the system, and you have good prompts to help the model choose the right function.

For real projects, it's not just about question answering but also about tool rendering. Some tool calls define UX elements - like a fitness company chatbot that renders modals for booking calendar events and following up with payment links. This becomes the economically valuable work - not just answering questions but helping the company make money.

---

## What's the moat for companies building RAG systems when so much is being open-sourced?

I generally think the moat is your labeled data. There probably isn't much difference between various newsfeed algorithms, but the moat is the inventory - the content that's already out there.

If you have relationships in a specific sector like construction and can be the first to build connectors and bring in that data, that's an easy moat (though not as defensible).

After that, it's about analyzing that data to understand what questions people are asking and building specialized tools for those needs. This is software that LLMs won't replace anytime soon.

Then it's understanding what relevance actually means - fine-tuning re-ranking models, training custom embedding models. These are aspects that LLM companies won't compete against.

The moat becomes your data - both relevancy data and access to the content itself - plus your understanding of customer needs and workflows. The more you understand what customers are truly trying to do (beyond just answering questions about PDFs), the better your product will be.

---

## In the UX lectures, you mentioned that explicit copy instead of just thumbs up/down can impact whether people give feedback. Have you observed an impact based on what the copy actually says?

Absolutely. At Zapier, they asked "How did we do?" which was a very vague question that didn't get much feedback.

When we A/B tested copy, the version that got 5x more feedback was "Did we answer your question?" This was much more specific and focused on the core value proposition, not about latency or formatting. If users said no, we'd follow up with "Do you have any other feedback? Was it too slow? Was the formatting wrong?" since we knew those were common failure modes.

This not only got more feedback but also correlated better with customer satisfaction. The previous vague question made it hard to identify what was a good or bad answer - some might say we did poorly because we answered correctly but too slowly.

At Raycast, our copy now is "Did we take the correct actions?" since we're showing function calls like "Set a 1-hour lunch on my calendar and update my Slack status." We show users the sequence of function calls and ask if we're taking the correct actions.

The key is that every metric you track should lead to a follow-up action. It's not just about knowing the number.

---

## How can we extract value from template/pre-filled questions in chatbots?

For a situation like a lawn care subscription company's chatbot where 70% of conversations start with template questions, I'd be curious to understand what the follow-up questions look like. This helps determine if we could create complete guides for common paths.

If people start with a certain template question, do their follow-ups cluster in a specific domain? This can help you understand if your example questions are actually helpful or if you should be writing better content to answer these questions more comprehensively.

One approach is to use a language model to summarize conversations, identifying what topics come after the template questions. This gives you insight into actual user intents that might be hidden behind that initial templated interaction.

You should analyze which topics are economically important by looking at metrics like thumbs up/down data. For instance, we found that many negative ratings come from users who want to talk to a real person but can't easily figure out how to do that.

It's also valuable to analyze what products you should recommend based on question patterns. If you're seeing thumbs-down ratings, analyze whether it's because you don't have the right content in your knowledge base, or if there are capabilities you're missing. Often, the solution might be as simple as hiring someone to write targeted content for frequently asked questions.

---

## How do you handle business knowledge translation (like acronyms) in RAG?

When you have documents that spell everything out formally but users want to query using acronyms (like "What's the deal with ABC?"), I'd generally just put this translation knowledge in the prompt unless you have an enormous number of acronyms.

If you have fewer than 80 acronyms or terms that need translation, putting them directly in the prompt is the simplest and most effective approach. You only need to explore more complex approaches when you have evidence that this simple solution isn't working.

You can also create synthetic data to test how well your system handles these acronym queries, which is usually straightforward to generate.

---

## What are the best practices for chunking in RAG systems?

The general advice from companies like OpenAI and Anthropic is to start with around 800 tokens with 50% overlap using a sliding window approach. That should be enough to get you started.

After that initial setup, the real improvements come from understanding what kinds of questions are being asked and what the answers look like. If most questions can be answered by a single document, focus on improving document search and relevancy rather than chunking. If answers typically come from small paragraphs across many documents, then experiment more with chunking.

We've spent weeks doing chunking experiments and often haven't seen significant improvements. It's rarely the case that changing from 500 to 800 tokens suddenly makes everything work better - that would suggest most answers require just a few more sentences in the same document, which is usually not the issue.

What's been more helpful is looking at the questions and working backward: What are people trying to do, and what design assumptions can I make to better serve that? For instance, if users are searching for blueprints, maybe summarizing blueprints first would help, or perhaps including text above and below the blueprint, or even applying OCR and building a bounding box model to count rooms.

Solve specific problems where you can justify that "this is 20% of our questions" - if you make those 20% twice as good, you've improved overall performance by 8%, which is meaningful.

---

## Are XML tags still best practice for prompting models?

Yes, we've learned that even the GPT-4 models now perform better with XML formatting. We have internal evaluations from Zenbase showing that XML is good not just for Anthropic models but also for ChatGPT models.

The second thing we've found is that you generally want to have all the long context information at the beginning of the prompt - first the goal, then all the documents, with the actual questions at the bottom.

Claude's prompt rewriter has been very helpful for showing how to write better prompts. I almost always run my prompts through it first before setting up evaluation suites, as it's a free way to get useful feedback.

---

## How do you handle tokenization concerns with things like wallet addresses?

When dealing with data that contains wallet addresses (which are 52 characters of what looks like nonsense), I'd worry less about the tokenization itself and focus more on validation.

For example, in situations where we use UUIDs, we reference content with a UUID, and we tell the model to cite everything. We then have an allowlist of valid UUIDs from our data, and we check that any UUID the model outputs exists in that allowlist.

So if you have a use case where users ask about wallet IDs, focus on making sure the model can only reference valid wallet IDs from your dataset rather than worrying about how they're tokenized.

These days, models aren't typically off by a few characters - they'll either get it right or completely make up new identifiers. Having logical checks in your code is more important than the tokenization strategy.

You can also generate synthetic test data where you know which wallet addresses should appear in the answers and ensure there are no hallucinations.

---

## Should we transform content from narrative format to Q&A format for better retrieval?

Yes, massively. This can be very beneficial, especially for a question-answering chatbot.

It's already an assumption to think that everything is going to be in the form of a question. For some assistants, it might be more about conversations or past memories. If you know your use case is primarily Q&A, then extracting question-answer pairs from your documents is valuable.

You can build a system where when you embed a question, you retrieve the embedding of similar questions, but pull in both the question and its answer. This makes sense if your use cases are mostly Q&A-based rather than narrative requests like "tell me a story."

One of the big assumptions in RAG is that the embedding of a question is similar to the embedding of a relevant document, which is actually a massive assumption that doesn't always hold true.

To prevent retrieving too many similar question-answer pairs (which could be redundant when getting top-K results), consider doing clustering. You could extract 10 questions per document, then cluster similar questions together and rewrite them to create a more concise, focused knowledge base.

---

## Can you recommend any open source libraries or tools for streaming UIs and interstitials?

I can't necessarily recommend a specific library too strongly because most companies I've worked with have built these themselves. However, if you're in the Python world, using something like FastAPI and server-side events (SSE) API is probably the simplest approach. In the slides, we give an example of what this looks like - you're basically using the yield keyword from Python generators to emit events.

If you're using JavaScript and part of the Vercel/React ecosystem, I think Vercel's AI library does a great job of handling structured streaming. Other libraries like LangChain, LlamaIndex, and Instructor also support partial streaming where you can send incomplete JSON to a frontend, which can then rerender it.

For interstitials, I've been impressed with what Ankur from BrainTrust has done in their playground. I've reached out to him to ask about recommendations for this.

With these tools, the implementation is fairly straightforward. The bigger challenge is often designing a UX that communicates progress effectively. Notion's approach is a good example - when you enter a search query, it shows "making a search request," rewrites the request, then renders documents one by one, and finally shows steps like "carefully reading documents," "thinking," and "formulating an answer." This is really just buying time while showing progress, but it dramatically improves the perceived responsiveness.

---

## Why aren't data labeling companies a bigger focus in current AI discussions?

This is an interesting historical shift. Around 2018, data labeling was a huge focus because the biggest models were vision models that required massive amounts of labeled data. Vision models aren't very data-efficient - training ImageNet required labeling a million JPEGs. Companies like Scale AI won by excelling at tasks like self-driving car LiDAR labeling.

As we've moved to LLMs, two things have changed:

1. The big winners (like Scale AI) have already established themselves and now focus on large contracts. Smaller players either grew or struggled to find viable business models on smaller contracts.
1. LLMs are much more data-efficient.

The data efficiency of modern LLMs is remarkable. You're better off having 1,000 very high-quality labels to fine-tune a model than 10,000 mediocre labels. This means that instead of outsourcing labeling work, it often makes more sense to have subject matter experts do a one-month project to create the data you need.

We're so sample-efficient now that offshore labeling doesn't make economic sense for many use cases, especially when LLMs have been shown to match or exceed the quality of offshore labeling for many tasks. If you have specific legal workflows, you're better off asking the lawyer on your team to do the labeling.

The real challenge now is: how do you find people who are smarter than GPT-4 to label data to train the next generation of models? That hiring problem is different from the traditional labeling company approach.

---

## How do you see re-rankers evolving beyond just measuring relevancy?

Right now, most RAG systems only rank based on relevancy between a query and a document. But I think re-rankers will soon incorporate much more side information, similar to what we see in e-commerce recommendation systems.

In e-commerce, we have additional rankers for things like price sensitivity, seasonality, and product age to determine if customers prefer trendy or timeless items. This hasn't really happened in the RAG world yet.

As AI systems accumulate multiple years of memories about users, figuring out what information to put in context will become much more interesting. Re-rankers won't just measure string similarity between a question and document - they'll likely incorporate user features, environmental features, and contextual information to determine relevance.

For example:

- Security constraints (only searching documents you have access to)
- Time/recency components for memories
- Domain authority when sources disagree
- User preferences based on past interactions

Even systems like Deep Research might evolve to pull from sources you tend to agree with, or deliberately include sources that challenge your viewpoint. These personalized relevancy signals could dramatically improve RAG systems beyond simple semantic matching.

---

---

## Key Takeaways and Additional Resources

### Key Takeaways:

- Data quality is becoming more important than ever - good models make data quality the differentiator
- When collecting feedback, be specific with your questions to increase response rates
- Focus on economically valuable workflows, not just answering questions
- For messy knowledge bases, consider clustering and summarization approaches
- The moat for RAG companies is proprietary data and domain expertise, not algorithms
- Binary feedback (thumbs up/down) generally gets more responses than free text
- Always have a clear next action from any metric you collect
- Focus on impact (economic value) rather than just query volume

### Additional Resources:

- Google Search Relevancy document/policy is a good reference for defining relevance
- RAPTOR paper for document summarization approaches
- Week 3-4 content in the course covers more on these topics
- For prompt rewriting, Claude's prompt rewriter is highly recommended
- When dealing with streaming UIs and latencies, Notion's approach of showing steps visually is a good reference
- For friends example in recommendation systems, consider platforms like Facebook's friend recommendation system as reference implementations

_Note: I'll continue to add resources and notes from future office hours sessions_

---

IF you want to get discounts and 6 day email source on the topic make sure to subscribe to

<script async data-uid="010fd9b52b" src="https://fivesixseven.kit.com/010fd9b52b/index.js"></script>

---

## What can "segments" mean beyond query volume and satisfaction values in a RAG system?

Segmentation really depends on who your customers are and what they're trying to do. With a generic chatbot, it's hard to figure out what segmentation means. But if you think about intents of a specific application, you can uncover different patterns.

For example, with a nutrition company chatbot, you might discover segments within product search – different capabilities around understanding deliveries, rescheduling, recurring orders, etc. Data analysis helps figure out what's important to build for the customer.

In a construction context, we found segments around:

- Users inputting specific project IDs (e.g., "Tell me about RFC 1257")
- Questions about time windows ("What do I have due today?" or "What's happening this week?")
- Counting items in documents

The goal of segmentation is to help you figure out what new function tools to build and what workflows might be viable. Another example: for a product that takes screenshots of users' computers, we found 10% of customers asking "How much time did I spend in this application?" That's impossible to answer with just screenshots, but we realized we had a Postgres database of all screenshots with timestamps, so we built a specific tool to query, group, and sum that data to answer the question.

The key is to find external understanding of your data – what are you worried about, and if you discover certain properties, what can you do about it?

---

## How should we approach segmentation for chatbots where the output is a whole conversation rather than just a query response?

If you have the compute resources, do similar classification and segmentation over your conversations. You'll uncover different insights beyond just tools.

When analyzing queries alone, we're basically asking how well we can execute tools to answer in one generation. By analyzing conversations, we might find segments that tell us:

- Users think the chatbot talks too much or not enough
- Users are frustrated with responses
- Common patterns in how conversations progress

The general idea is to gain an external understanding of your data – what properties are you concerned about, and if you discover X% of conversations have a certain property, what action can you take?

For example, if you find many users asking the language model to rewrite answers in their own words, should that be part of your system prompt? Analysis might show only 10% want tone matching, while most users actually prefer the AI voice.

---

## What approaches do you recommend for topic clustering, and have you tried using thinking models to generate clusters?

I generally use what I call "old school" approaches – K-means and DBSCAN. I typically start with the default settings in BERTTopic, which has been very good. The topic modeling goal isn't to uncover topics for production use but to do data analysis that helps you understand your data better.

For example, I might take Ada 2 embeddings, use K-means to pick 10-30 clusters, and look at 100 questions per cluster. That might take 2-3 days but teaches you a lot about your data. It's rarely the case that you run topic models and can just use them directly in your business.

When working with thinking models for clustering, I still do the initial clustering first because I might have 20 million questions to analyze. I'll cluster that data, find good and bad examples across clusters, and put that into Claude 3.7 or similar models, asking them to:

- Name each cluster
- Provide a short description
- Give good examples of what belongs in the cluster
- Provide nuanced examples of what's not in the cluster

This produces a YAML file that I can then use for classification. The language model helps expand our understanding, especially when we can't easily enumerate all possibilities ourselves.

---

## What are your thoughts on chunk size and chunk overlap? Is it worth trying out different chunking strategies?

I generally use 800 tokens with 50% overlap, which is what OpenAI recommends in their blog posts. In my experience, chunking strategies rarely make a significant difference compared to other improvements.

There's only a small subset of questions where chunk size makes a difference – you would need a question that can only be answered by a paragraph where two concepts are exactly 500 tokens apart. Performance gains usually come from better re-ranking, contextual retrieval (where you rewrite text chunks given the entire document), or better filtering and metadata capabilities.

I've rarely seen chunk size be the 10% improvement win – it might be a 1-2% improvement, which could just be noise. I would focus more on contextual retrieval if you have the compute budget for it.

For semantic chunking (using an LLM to determine good chunking points), I'm actually pretty convinced that contextual retrieval is better than dynamically chunking. The real question is whether you need to cite things word-for-word (in which case you shouldn't rewrite chunks) or if you just need general question answering.

I'd always spend more compute upfront to improve data quality. For example, I worked with a company doing Brazilian tax law with 50 documents, each 600 pages long. I asked, "Why are you only spending 70 cents to process this PDF? Why not spend $30?" If you're processing billions of dollars through the system, you should invest in good ingestion.

---

## What strategies can improve experimentation speed when working with RAG systems?

If you feel like you're not running enough experiments, focus on improving your infrastructure:

1. **Write parallelized code**: Many teams are still doing all their tests using for loops. Spending 1-2 hours learning to write parallelized code can dramatically reduce your experimentation time, going from days to hours. Using tools like multiprocessing to hit multiple endpoints simultaneously is much better than having code break on iteration 2,000.

1. **Improve data access and understanding**: Document how to query your data effectively. It's a waste of time if you write a query to prepare data, and someone comes back a day later saying, "That's wrong, we actually need to include only last week's data."

1. **Build modular pipelines**: If your entire RAG application is a giant Python file, it will be hard to test. But if each search index is a separate POST request, you can test them individually. This allows you to focus on one component (like an image retriever system) and improve it from 30% to 80% accuracy in one afternoon before integrating it back into your router.

1. **Test locally when possible**: Create smaller synthetic datasets for quick iteration before running larger tests.

Being able to test components in isolation is crucial for rapid experimentation. A lot of this comes down to good software engineering practices and thoughtful system design.

---

## How do you handle multiple languages in a RAG system, especially when job titles may be similar but written differently across languages?

For multilingual challenges like job titles across different languages, I recommend two approaches:

1. **Metadata extraction and filtering**: Build classifiers to add more metadata to your ontology. For example, "software engineering recruiter" and "software engineer" go into two different classes, allowing you to filter for one and not the other. This improves search precision.

1. **Fine-tune embedding models with triplets**: Create a dataset with examples like "software engineer" (query), "python developer" (positive example), and "software engineering recruiter" (hard negative). This teaches your model to separate similar-looking job titles that have different meanings.

For handling multiple languages, run tests to see whether translation improves performance. For instance, does your classifier perform better if you translate everything to English first, or if you use the original languages? If translating provides only a 1-2% improvement but requires complex infrastructure to maintain, it might make sense to accept slightly lower performance.

If you lack training data for certain languages, consider using synthetic data creation. Use $2,000 of API credits to generate examples that cover edge cases in your domain, like distinguishing between "real estate developer" and "python developer" across languages.

---

## What are your thoughts on vision RAG, and what databases would you recommend for multimodal embeddings?

Vision RAG isn't talked about as much because it's more expensive and most of the important data is typically in text. That said, there are valuable use cases – like a company that does RAG over video clips to help movie producers find content, using Gemini Flash to describe what's happening in scenes.

For databases, I'd recommend looking at:

- ChromaDB
- LanceDB
- TurboBuffer (used by Notion and Cursor)
- PgVector with Scale (for relational data with many reads/writes)

However, I'm finding that pure multimodal embeddings aren't always the best approach anymore. Often it's better to generate a text summary of the image data. For example, when trying to embed images and text in the same space, CLIP embeddings often work worse than just doing image captioning and then embedding that text.

In week 5, I'll talk more about this – there are many things you can't do with multimodal embeddings. They're trained mostly with caption data, which limits their capabilities for certain tasks.

---

## What are your experiences with the Model Context Protocol (MCP) and how might it change RAG systems?

MCP is becoming increasingly important because it allows different systems to connect with each other. When you own all the code, you don't really need MCP since you can just use function calling. But the ability to connect different systems is very compelling.

Some interesting examples of MCP usage:

- Having an MCP server in Cursor to do image generation while building a video game
- Creating an MCP server to access network logs for debugging web applications
- Building MCP servers that connect to production databases so Cursor can understand your schema and write SQL
- Setting up an MCP server that writes conversation notes to Notion automatically

What makes MCP powerful is that it standardizes these integrations and reduces boilerplate code. The protocol founders explain that it's easy to integrate with other servers when building your own client or server. Instead of rebuilding connectors with databases or services, you can reuse patterns and implementations.

Claude 3.7 with Claude Code, for instance, has impressive agent functionality using MCP. It features better context management through commands like "/compact" which summarizes conversation history effectively without bloating the context window.

---

## How can we use synthetic data generation for summarization tasks?

There are many creative ways to generate synthetic data. For summarization, you can:

1. **Create reverse tasks**: For example, start with the outcomes you care about (like action items) and ask an LLM to generate a transcript that would produce those items. Then you can verify if your summarization system correctly extracts the original action items from this synthetic transcript.

1. **Use data augmentation techniques**: Look at techniques from other domains like speech detection, where researchers combine clean audio samples to create more complex scenarios (like overlapping speakers). You can apply similar principles to text.

1. **Apply transformations similar to image processing**: In computer vision, we've long used techniques like converting color photos to black and white, then training models to predict the original colors. Similarly, we convert high-resolution images to low-resolution and train models to predict the original resolution. We can apply similar transformations to text data.

The key is to think about ways to go from your desired output backward to input data, or to systematically transform existing data in ways that preserve the information you care about while changing other aspects.

---

## When using structured outputs with few-shot prompts, should the examples use the exact same JSON schema or can they be plain text?

I would almost always try to keep the JSON format consistent in your few-shot examples. This is somewhat superstitious, but I feel like the attention mechanism will always attend better to similar tokens.

The schema itself is probably not what's going to break things these days. More likely, problems will arise from unintended properties of your examples. For instance, if all your action items in the few-shot examples are very short (under 4 words), your outputs will tend to be very short too. The examples communicate that these properties are correlated.

I'd rather keep everything in JSON because there will be other random issues that come up. The only caution is to make sure you have checks in place so that when the language model has nothing in the context, it won't just automatically recite the few-shot examples.

For complex contexts (like insurance claims that require understanding policies and forms), if including the context for each few-shot example would make your context window explode, consider few-shotting the thinking more importantly. Show examples of the reasoning process: "I noticed the customer said they had 28 people, and our pricing page has different pricing for teams with less than 30 employees, so I'll use that pricing tier and mention they could get a better price with more employees..."

---

## How do you approach RAG when you have transcripts or unstructured text without clear paragraph markers?

For transcripts without clear paragraph markers, a few approaches work well:

1. **Use diarization models** to get speaker tags, which can serve as natural boundaries (each dialog line becomes a chunk)

1. **Detect silences** in the audio and chunk on those silences

1. **Consider the structure of your content** - for instance, if it's an interview format, you might know it's always question-answer pairs, so you can embed those pairs together

It ultimately depends on your specific use case. For a general conversation, chunking on silences or using diarization with a sliding window over dialog will work. For job interviews or expert interviews, understanding the structure (question followed by answer) lets you optimize your chunking strategy.

If you have mixed domains and raw transcripts without access to the original source, you might need to default to generic approaches like 800 tokens with 40% overlap, then rely more on contextual retrieval techniques.

---

## What are your recommendations for building slide presentations with AI tools?

I've been using AI tools to build academic-style slides with LaTeX and Beamer. My process is:

1. Load all relevant content into Cursor (in my case, all 6 hours of course transcripts)
1. Create an outline for the presentation
1. Use Claude to extract key case studies and insights from the transcripts
1. Have the LLM generate slides using LaTeX Beamer format
1. Use a simple auto-compiler (built with Watchdog) that recompiles the PDF whenever the file changes

The advantages of this approach:

- You can create both slides and a detailed document from the same source
- The LLM can generate diagrams using TikZ (a graphics creation library)
- Everything is vector-based so it looks clean at any resolution
- You can have the LLM add callouts, highlights, and formatting

This approach lets me essentially talk to my slides and have them update in real-time. I can say "make this section shorter" or "add an example about X" and see the changes immediately in the PDF preview.

For those who prefer different formats, you could also try reveal.js for web-based presentations. The key is finding a workflow that lets you focus on content while the AI handles formatting and details.

---

## How do AI coding tools compare (Claude Code, Aider, Cursor, Windsurf)?

There's been significant evolution in AI coding tools, with different strengths and approaches:

- **Claude Code** has impressive agent functionality with excellent context management. It features a "/compact" command that summarizes conversation history effectively without bloating the context window. Some users report it's more capable than Cursor for certain tasks, particularly with how it handles context and managing complexity.

- **Aider** is a CLI-based tool that gives very low-level control over the files you can edit. It's open source and allows granular control over which models you use at specific points. Some users have migrated from Cursor to Aider due to its flexibility, though it has a steeper learning curve.

- **Cursor** is widely used for its UI and integrations. It works well for incremental changes to code and has good MCP integrations, but some find its context management becomes less effective over time on complex projects.

- **Windsurf** is particularly good at handling projects with good requirements and system design. It excels at context management over time and keeping track of multiple files in a repository. It's especially valuable for staff engineers and system architects who start with clear system designs.

The key differentiation often comes down to context management - how well the tool maintains an understanding of your entire codebase and project requirements as you work. For complex projects, tools that help document the goals and requirements (like adding branch goals in comments) tend to perform better.

---

## How do you use Deep Research and other search tools effectively?

Different search tools serve different purposes depending on context:

- **Claude's Deep Research** works well for technical documentation, business-level competitive analysis, and generating comprehensive memos. Its tone is particularly well-suited for business communications that need minimal editing. Many users leverage it to materialize blog posts or analyses they want to read (e.g., "Write me a blog post on why someone should look at MCP versus just using the Open API spec").

- **Grok's Deep Search** has different strengths, with some users preferring it for timely news or quick research questions. Interestingly, usage patterns often split between mobile (Grok) and desktop (Claude/OpenAI) platforms based on when and where research is being done.

- **Perplexity** offers another approach to deep research, useful for generating product specs and learning resource reports, especially for colleagues without AI engineering backgrounds.

The quality of these tools has advanced to the point where they can effectively replace traditional research methods for many use cases, saving significant time for competitive analyses and technical investigations.

---

## What makes Lovable stand out for no-code app generation?

Lovable has emerged as a powerful tool for no-code app generation:

- It excels at creating fully functional applications with modern UIs from scratch, going beyond simple prototypes to production-ready systems
- Its deep integration with Supabase provides authentication, real-time features, and database capabilities out of the box
- Every code change gets pushed to GitHub, allowing developers to fix issues locally in tools like Cursor or Windsurf when needed
- Each commit creates a preview deployment on Cloudflare, streamlining the development and testing process
- The tool can implement complex features like row-level security, push notifications, and real-time commenting systems using websockets

Users report that Lovable outperforms alternatives like V0 and Bolt for creating complete applications, though it can be expensive ($200+ for complex projects). The tight integration with Supabase is particularly valuable, with many users becoming paid Supabase customers after using Lovable to build their applications.

---

## What emerging techniques are promising for handling long documents in RAG?

Handling long documents effectively is still evolving, with several promising approaches:

1. **Hierarchical retrieval**: Create summary or header-level embeddings for entire documents/chapters, then more granular embeddings for sections/paragraphs. This allows multi-stage retrieval that narrows down from document to specific passages.

1. **Graph-based approaches**: Build knowledge graphs connecting concepts across documents, enabling retrieval that follows conceptual relationships rather than just lexical similarity.

1. **Hybrid sparse-dense retrieval**: Combine embedding-based retrieval with keyword/BM25 approaches to capture both semantic and lexical matches, which is particularly valuable for documents with specialized terminology.

1. **Learning to rewrite**: Train models to rewrite retrieved chunks into more coherent contexts that preserve the key information while eliminating redundancy.

1. **Recursive summarization**: For extremely long documents, apply recursive summarization techniques that gradually compress information while maintaining key details.

Projects like LangChain's Document Transformer framework and repositories focusing on document processing show significant advances in these areas. The most effective systems often combine multiple approaches based on the specific characteristics of their document collections.

---

## How can I approach RAG for messy knowledge bases with duplicate documents?

When dealing with messy knowledge bases that contain duplicate or near-duplicate documents:

1. **Pre-processing pipeline**: Implement de-duplication strategies during ingestion. This could involve computing similarity scores between documents and merging or filtering based on a threshold.

1. **Metadata extraction and filtering**: Add more metadata to your ontology by building classifiers for different document types or topics. This allows you to filter for specific categories during retrieval.

1. **Query classification**: For ambiguous queries, implement both pre-retrieval and post-retrieval classification to identify query intent and determine when clarification is needed.

1. **Progressive disclosure**: Consider displaying intermediate results with summarized information about potential topics before generating a complete answer. This helps users navigate ambiguity, especially for queries that could refer to multiple topics.

1. **Dynamic presentation**: For high-latency requirements (e.g., responses needed in under 6 seconds), consider showing retrieved documents first while the full answer is being generated, allowing users to see some results immediately.

Remember that the goal isn't perfect retrieval but helping users find the information they need. Sometimes showing multiple possible interpretations of a query is more helpful than trying to guess the single "right" answer.

---

## When is it better to use DAGs versus agentic approaches?

For specific workflows with well-defined steps, DAGs (Directed Acyclic Graphs) often provide more reliable and predictable results than fully agentic approaches:

1. **Use DAGs when**:

   - The workflow has clear, sequential steps
   - You know the process is correct and just need to choose the right workflow
   - You're implementing established protocols (like therapy approaches or compliance processes)
   - Predictability and consistency are critical

1. **Use agentic approaches when**:
   - The problem space is exploratory
   - Tasks require adaptation to unpredictable user input
   - The workflow needs to evolve based on intermediate results
   - You need to handle a wide variety of open-ended requests

The distinction often comes down to control versus flexibility. DAGs provide more control over the exact process, while agentic approaches offer more flexibility but less predictability.

For example, in a therapeutic chatbot following an established CBT protocol, a DAG approach ensures the conversation follows the correct therapeutic sequence. However, for an open-ended research assistant, an agentic approach allows for more dynamic problem-solving.

---

## How do I create effective negative examples for training retrieval models?

Creating effective negative examples for training retrieval models involves several strategies:

1. **Hard negative mining**: Find examples that are semantically similar but actually irrelevant. For job listings, "software engineer recruiter" is a hard negative for "software engineer" queries - they look similar textually but represent different job categories.

1. **Top-K analysis**: Run retrieval with your current model, then have an LLM evaluate which results in the top K are actually irrelevant. These make excellent negative examples because they expose weaknesses in your current model.

1. **Controlled random sampling**: While pure random sampling provides some signal, it's often too easy for the model to distinguish. Instead, use controlled randomization that preserves some properties of the positive examples.

When working with triplet learning (query, positive example, negative example), the quality of your negative examples often has more impact on model performance than adding more positive examples. Focus on finding negative examples that are difficult to distinguish from positive ones.

For multimodal or multilingual applications, you may need to create synthetic data, especially for languages with limited training data. This can be done by using LLMs to generate examples that explore edge cases in your domain.

---

## What strategies can improve response time in RAG systems with tight latency requirements?

For applications requiring responses in just a few seconds:

1. **Progressive rendering**: Show retrieved documents first (which can be returned in 150-400ms) while the LLM generates the complete answer in the background. This gives users immediate results while they wait for the full response.

1. **Caching**: Implement aggressive caching for common queries. When a question-answer pair receives positive feedback (like being forwarded, shared, or rated highly), save it as a new document that can be quickly retrieved for similar questions.

1. **Response type classification**: Use a lightweight classifier to determine if a query needs full retrieval and generation or if it can be answered with a simpler approach.

1. **Contextual snippet generation**: During retrieval, generate quick summaries of each chunk that can be displayed alongside search results before the complete answer is ready.

1. **Parallel processing**: Run multiple retrieval strategies in parallel and combine the results, rather than using sequential processing that adds to the total latency.

The key insight is to avoid an all-or-nothing approach to response generation. By decomposing the process into steps that can be displayed incrementally, you can significantly improve perceived latency even when the complete answer takes longer to generate.

---

## What are your experiences with the Model Context Protocol (MCP)?

MCP (Model Context Protocol) is becoming increasingly important as it allows different AI systems to connect with each other:

1. **Key benefits**:

   - Standardizes integrations between AI systems
   - Reduces boilerplate code when connecting to different services
   - Allows models to access data and functionality they wouldn't normally have permission to use

1. **Practical examples**:

   - Image generation servers in Cursor for creating assets while building applications
   - Servers that connect to network logs for debugging web applications
   - Connectors to production databases that help models understand schemas and write SQL
   - Automation tools that write conversation notes directly to Notion or other note-taking systems

1. **Comparison to function calling**:
   - When you own all the code, function calling may be simpler
   - MCP becomes valuable when connecting separate systems with different permission models
   - Provides a standardized way to expose capabilities across different AI platforms

The protocol is still evolving but shows promise for creating more powerful AI systems by composing specialized components. Some implementations like Claude 3.7 with Claude Code demonstrate how MCP can enable better context management and more sophisticated agent capabilities.

---

## Key Takeaways and Additional Resources

### Key Takeaways:

- The goal of segmentation is to understand customer needs and determine what tools to build next
- Chunking strategy (800 tokens, 50% overlap) is rarely the bottleneck - focus on contextual retrieval instead
- For topic modeling, start with BERTTopic defaults and then use thinking models to better understand clusters
- Spend more compute upfront to improve data quality - particularly for high-value documents
- Write parallelized code to dramatically speed up experimentation
- For multilingual RAG, test whether translation improves performance enough to justify the added complexity
- Consider transforming image content to text summaries rather than using pure multimodal embeddings
- MCP is becoming increasingly important for connecting different AI systems together
- Use structured JSON consistently in few-shot examples rather than plain text
- For slide creation, AI tools can generate both content and formatting in vector-based formats
- For long documents, consider hierarchical retrieval, graph-based approaches, hybrid sparse-dense retrieval, learning to rewrite, and recursive summarization
- For messy knowledge bases, implement pre-processing pipeline, metadata extraction and filtering, query classification, progressive disclosure, and dynamic presentation
- For DAGs versus agentic approaches, use DAGs when the workflow has clear, sequential steps, and use agentic approaches when the problem space is exploratory
- For negative examples, use hard negative mining, top-K analysis, and controlled random sampling
- For response time, implement progressive rendering, caching, response type classification, contextual snippet generation, and parallel processing

### Additional Resources:

- BERTTopic: https://maartengr.github.io/BERTopic/index.html
- MCP Agent: https://github.com/lastmile-ai/mcp-agent
- Claude Code: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview
- RepoPrompt: https://repoprompt.com/
- Aider CLI coding tool: https://aider.chat/
- Lovable for no-code app generation with Supabase integration
- Cursor and Windsurf for AI-assisted coding environments

---

IF you want to get discounts and 6 day email source on the topic make sure to subscribe to

<script async data-uid="010fd9b52b" src="https://fivesixseven.kit.com/010fd9b52b/index.js"></script>

---

## How should we handle Excel files with multiple sheets and tables?

Handling Excel files with multiple sheets and tables is challenging, and few companies have solved this problem well. Experience from companies like Zapier shows that connecting Excel spreadsheets to automation tools requires many controls to work properly.

The recommended approach is implementing checks on uploads to ensure files meet certain criteria. These checks might verify if an Excel file contains a single table, stays within size limits, or contains a specific number of tables. For simpler Excel files with single tables, implementing validation and processing works well, but for more complex files with multiple sheets and scattered tables, exporting to PDF might allow for easier parsing.

It's important to segment data and build specific extractors based on the data's structure. Single-table files can go through a dedicated single-table pipeline, while multi-table files might work better through a PDF parsing pipeline.

The most practical advice is to focus on simpler problems first and reject more complex ones until better solutions are developed. Solving for the simpler 40% of use cases while avoiding the most complex scenarios can be an effective strategy. Exporting Excel files as CSVs might also provide better compatibility with processing tools in many situations.

---

## What tools are recommended for SQL generation?

[Claude Sonnet](https://www.anthropic.com/claude) has proven effective for generating SQL queries. Success depends heavily on whether the system can retrieve the correct tables and CREATE statements.

The key to successful SQL generation is having good descriptions and CREATE statements for the tables, as well as ensuring that embedding and search capabilities properly identify the right tables when needed.

A recommended approach from [Timescale](https://www.timescale.com/blog/enhancing-text-to-sql-with-synthetic-summaries) involves first retrieving relevant tables, then retrieving pre-existing, approved SQL snippets. When both the correct tables and appropriate SQL patterns are in context, the generation process becomes significantly more reliable.

The complexity increases with many tables and columns, but focusing on retrieving the correct tables first, then incorporating approved SQL snippets to guide the generation process creates a two-step approach that significantly reduces errors in SQL generation.

---

## What is the Linear Adapter for embeddings and how does it work?

Linear adapters provide a cost-effective way to fine-tune embeddings. An embedding model takes data and produces a vector, with the dot product of two vectors indicating how similar they are. A linear adapter learns how to "rotate" these vectors slightly to better align with specific queries.

The approach is very economical - if a vector has 500 dimensions, the linear adapter is just a 500 by 500 matrix that multiplies the original vector. This allows for significant improvements in embedding quality with minimal computational cost.

Linear adapters can be compared to [LoRA (Low-Rank Adaptation)](https://research.trychroma.com/embedding-adapters), but with key differences. LoRA works between many layers of a neural network, while a linear adapter works only at the end. Additionally, linear adapters can be applied to pre-trained embeddings like those from OpenAI without needing access to the original model weights.

This approach enables domain-specific adaptations - for example, creating different adapters for marketing versus sales questions, or specialized adapters for legal, marketing, or tax information. The cost benefit is significant - training a linear adapter typically costs around $12 and can be done quickly, making it much more accessible than full model fine-tuning.

Implementation uses the standard fine-tuning process with triplets (question, positive example, negative example), but specifically changes the embedding function for the query. This rotation of vectors into more effective alignments can significantly improve retrieval performance for domain-specific applications.

---

## How does partitioning work in retrieval systems?

Partitioning in retrieval systems refers to how data is organized and segmented, rather than being about individual users. In applications like Cursor, a "user" might represent a documentation page. When working with code libraries like Requests, there might be a dedicated Requests index that multiple users access, but the partition is organized around the library package, documentation URL, or codebase.

Similarly, in applications like Notion, a "user" isn't an individual email account but represents an entire workspace. This means a company's complete Notion workspace would exist in a single index.

An interesting approach is partition-specific fine-tuning, which involves using different models to embed questions versus text chunks. Standard fine-tuning uses one model for both the question and the text chunk, but it's possible to fine-tune only one side of that equation. This might involve using the same model to embed all text chunks but having a different model to embed the question.

This technique proves particularly valuable in e-commerce settings. One embedding model might identify products that are similar to each other (creating a "similar products" carousel), while a different embedding model could identify complementary products (for "frequently bought together" recommendations). Both embeddings operate on the same product data but serve different retrieval purposes.

---

## What is the Model Context Protocol (MCP) and how does it differ from regular APIs?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/concepts/prompts) functions like a USB-C connector for AI systems - it's about standardization rather than specific functionality. While the devices that connect may vary, the connection method itself is standardized.

The key advantage of MCP over traditional APIs is the separation of client from backend. With a REST API, developers must write specific code to interact with each API, and each application needs to implement these integrations. MCP creates a standardized way for different systems to connect without custom code for each integration.

Consider an enterprise example where different teams might focus on different functionality: one team might work on email search while another builds CRM search tools. Both teams can develop their MCP clients, and the chatbot developers can easily integrate both without writing extensive custom code for each system.

This standardization means tools built with MCP work across multiple platforms without requiring custom integration code. A tool that works in one MCP-compatible environment (like Cursor) will work in others (like Claude desktop app) with minimal additional effort.

Beyond just function execution, MCP also supports resources and prompts. The MCP developer can provide not just functionality but also the prompts needed to use that functionality effectively. This means client developers don't need to write their own prompts for common operations like summarization or action item extraction.

This approach significantly reduces the need for glue code and allows developers to build applications without having to own all the client code, making integrations between different AI systems much more seamless.

---

## What AI tools are recommended for daily work?

[Claude Code](https://claude.ai/code) stands out among AI coding tools, particularly for its high-quality prompts. What makes it exceptional is how it handles context and continuity - when asked to write blog posts, it will first analyze existing posts to create a style guide, then reference that guide for every new post it writes.

This attention to existing style and consistency makes it particularly effective for content creation tasks. Despite higher costs compared to some alternatives (potentially $100+ per weekend of heavy use), many users find the value justifies the expense, with some noting they would willingly pay $200 monthly for the service.

For report generation specifically, there's significant value in tools that provide templated outputs. Ideally, a report generation tool would allow users to standardize formats across different reports - ensuring all market analysis reports follow the same structure, or that candidate evaluation reports maintain consistent formatting rather than varying significantly in format and depth.

This points to a broader trend in AI tool development - the need for tools that not only generate content but do so in consistent, predictable formats that align with existing workflows and style guidelines.

---

## What approaches are being used for multimodal applications?

Multimodal applications combining vision and language models are expanding into specialized domains. One example shared during office hours involved food image analysis, where a system extracts structured data from food photographs.

These systems can identify cuisine type, restaurant information, nutritional content, and dietary characteristics like whether a food item is vegan. While acknowledging practical limitations ("there's a limit to what you can effectively do"), early experiments show promising results in extracting valuable information from visual food content.

This example demonstrates how multimodal AI applications are moving beyond basic image recognition to extract detailed, structured information from visual content. The integration of vision models with language models allows systems to interpret and categorize visual information in ways that support practical applications like dietary tracking or restaurant recommendations.

---

## What emerging trends should we be aware of?

Report generation emerges as a particularly important trend in AI applications. The ability to automatically generate structured reports from unstructured data represents significant economic value for organizations.

Structured outputs and templates are increasingly valuable, especially for business use cases where standardized formats are essential. The ideal scenario allows for consistency in outputs - ensuring all reports of a specific type follow the same structure rather than varying significantly in format and organization.

Several organizations are developing report generation capabilities for internal use, with teams requiring standardized reports on a regular basis. This trend spans multiple industries, with financial due diligence being one area where automated report generation from multiple PDF sources shows particular promise.

The growing importance of fine-tuning approaches for handling data from multiple teams or domains also represents a significant trend. As organizations deploy AI systems across different business units, finding ways to effectively fine-tune models while maintaining performance becomes crucial.

Report generation capabilities demonstrate how AI can move beyond simple question answering to create significant economic value through structured information synthesis - transforming unstructured data into formatted reports that follow organizational templates and standards.

---

## How should we handle retrieval across multiple queries in a conversation?

When handling retrieval across multiple queries within the same conversation, the simplest approach is often the most effective. Using function calls for retrieval is recommended, where each call retrieves text chunks and includes information in XML format specifying the context and the question.

A key consideration is whether to keep retrieved context from previous queries in the message history for subsequent queries. This requires careful balancing, as including all previous context can consume tokens quickly.

The recommended practice is to prompt the retrieval system to always generate fully specified queries. For example, if the first question is "Where does Jason live?" and the follow-up is "What's the population of that city?", the retrieval system should be prompted to expand the second query to "What is the population of New York City?" This approach can be implemented through few-shot examples that demonstrate how to handle conversational context.

This strategy works because the model has access to both the previous question and answer in its context, allowing it to formulate complete, self-contained queries even when the user's input is ambiguous or relies on previous context.

An additional benefit of this approach is the ability to generate follow-up questions based on retrieved content. For instance, if a text chunk mentions that "Jason lived in different places when he was younger versus when he was older," the system can suggest follow-up questions like "Where did Jason live when he was younger?" This not only improves information discovery but also demonstrates to users that there are more interesting questions they could ask about the topic.

---

## What innovations are happening in memory and context management for agents?

Recent innovations in memory and context management for agents focus on creating more dynamic and self-improving systems. Rather than simply saving memories at the end of a conversation, newer approaches incorporate real-time memory creation and utilization during interactions.

Frameworks like Letta are incorporating self-editing capabilities alongside memory management. This integration allows agents to refactor their understanding and approach during a conversation rather than only learning from interactions after they conclude.

Implementation of these advances requires significant infrastructure changes, as memory layers affect prompt construction and the overall flow of agent interactions. The approach involves creating memories as the conversation progresses, which in turn influences the prompts used in subsequent exchanges.

With newer models like Claude 3.7 Sonnet, there's a shift in how tools are used by agents. Similar to the adaptation period seen with Claude Opus or GPT-4, these models require different prompting patterns to effectively utilize tools. Studying how systems like Cloud Code implement their tool use can provide valuable insights for optimizing agent performance with newer models.

---

## What can we learn from examining Cloud Code's approach to prompts and tools?

Cloud Code's approach to prompts and tools offers valuable insights for designing effective AI systems. Analysis of the Cloud Code source (extracted from their minified code) reveals highly detailed and carefully structured prompts for various tools.

Cloud Code implements a robust workflow where tools are designed to work together cohesively. Each tool's prompt contains specific instructions about how to use other tools first, creating a well-defined sequence of operations. For example, tools may include instructions to check for uniqueness before proceeding or to use specific validation approaches.

The prompts are remarkably detailed, with extensive instructions for common operations. For instance, batch tools contain comprehensive guidelines just for creating pull requests. This level of specificity helps ensure consistent and reliable performance.

Another notable aspect is Cloud Code's implementation of specialized tools like a notebook tool, showing how diverse functionality can be incorporated into a unified system. The prompts demonstrate that Claude is capable of working with numerous tools simultaneously when the system is properly designed.

This examination highlights the importance of thoughtful prompt engineering and tool design in building effective AI systems. By providing clear, detailed instructions and establishing well-defined workflows between tools, systems can achieve more reliable and sophisticated functionality.

---

## How can we create automated evaluation reports and insights for RAG systems?

Automated evaluation reports can significantly enhance RAG system development by providing structured insights and clear next steps. A comprehensive approach involves building a pipeline that:

1. Takes validation datasets and runs them through the RAG system
1. Computes various metrics (correctness, citation accuracy, URL validity)
1. Generates visualizations segmented by topic, question type, and other dimensions
1. Uses LLMs to analyze metrics and provide insights
1. Creates recommendations for system improvements

The reports can include both detailed analyses (15+ pages) and condensed slides for easier consumption in meetings. Key components include:

- Methodology explanations for stakeholders who may not be familiar with technical details
- System architecture diagrams
- Performance visualizations broken down by different segments
- Statistical analysis of which topics or question types perform well or poorly
- LLM-generated insights that explain patterns in the data
- Specific recommendations tied to the codebase

This process can effectively "close the loop" in the flywheel of development by identifying specific areas for improvement. For example, the system might recommend improving schema handling, enhancing retrieval tools, or adding more data for underrepresented topics.

The insights generated by LLMs analyzing the metrics can often align well with developer intuitions, but having them formally documented provides better clarity for prioritization and communication with stakeholders. These insights can be directly translated into development tickets, creating a streamlined workflow from evaluation to implementation.

The ultimate goal is to use these insights to guide the next iteration of development, run the evaluation again, and continue improving through this structured feedback loop.

---

## What strategies help maintain context when working with AI coding assistants?

When working with AI coding assistants like Cursor, maintaining context throughout a development session can be challenging. Several effective strategies have emerged from practical experience:

Creating and maintaining to-do lists within project documentation provides an effective way to preserve context. By instructing the AI to update the to-do list after completing each task, you ensure the progress remains in context for subsequent interactions. This approach creates a record of what has been accomplished and what remains to be done.

Templates within documentation files help maintain consistent structure across generated content. For example, having templates for different documentation sections ensures the AI follows established patterns when creating new content. This approach allows you to simply prompt the AI to "make more concept templates that generally look like this," maintaining consistency through visual examples rather than complex rules.

For more structured workflows, some developers create development plans using models like Claude Opus, which provide a roadmap the AI can follow. This helps prevent the AI from getting lost during implementation or going down unproductive paths.

Many developers find that keeping AI agents away from certain code areas (particularly tests) helps maintain structure. This can be accomplished either through explicit instructions or by adding files to the cursor.ignore configuration, which prevents them from being indexed while still allowing the AI to run commands like pytest.

Follow-up prompts at the end of interactions help maintain momentum. By asking what else needs to be done or what the next steps are, you encourage the AI to reference the to-do list and continue working on remaining tasks, creating a more cohesive development experience.

---

IF you want to get discounts and 6 day email source on the topic make sure to subscribe to

<script async data-uid="010fd9b52b" src="https://fivesixseven.kit.com/010fd9b52b/index.js"></script>

---

## What is Deep Research and how does it relate to RAG?

Deep Research is essentially a model fine-tuned for tool use that leverages RAG and iteration in a loop to produce reports. It can be viewed as RAG with solid data sources and strong reasoning capabilities on top. Deep Research is distinct from standard RAG applications because it typically produces more comprehensive outputs like reports rather than just answering specific questions.

While Deep Research generates reports that might differ in structure between runs, more advanced approaches like those used by Vantage aim to create standardized, deterministic reports. The ideal approach is to define a specific structure for reports, particularly when you know exactly what questions need to be answered for your domain.

There's significant economic value in creating structured reports rather than just answering ad-hoc questions. For example, instead of building a system that allows recruiters to query interview transcripts individually, creating a standardized hiring report that distills key information from all interviews provides greater business value. This approach helps stakeholders make better decisions rather than just saving time on information retrieval.

The techniques taught in the RAG course are directly applicable to building Deep Research-style systems, particularly when focused on specific domains rather than general-purpose research.

---

## Should we use long context windows or RAG for complex questions?

Long context windows should be leveraged first when possible, as they generally produce better results than relying solely on chunk retrieval. The ideal approach is often to use document-level retrieval rather than chunk-level retrieval when working with long context models.

When faced with specific tasks that require processing lengthy documents (like generating pricing emails based on policy documents), consider creating dedicated tools that use the full context window rather than breaking documents into chunks. This can be implemented as a function that uses a very long prompt containing all relevant policy documents.

This approach simplifies the retrieval problem from needing good chunk retrieval to just needing good document retrieval, which can be accomplished with simpler techniques like full-text search. The decision becomes not about whether you have good chunk retrieval but rather if you have good document retrieval capabilities.

As models' context windows continue to expand, this approach becomes increasingly viable for more use cases, potentially reducing the complexity of some RAG implementations.

---

## How important is human-labeled data for RAG systems?

Human-labeled data remains essential for building high-quality RAG systems, though many teams underestimate its importance. Teams that are reluctant to invest in data labeling often struggle to achieve meaningful performance improvements.

From a consulting perspective, one effective approach is to demonstrate the impact of data quality through experimentation. Show how model performance improves with synthetic data, then demonstrate how it plateaus. This creates a data-driven argument that once synthetic data reaches diminishing returns, real human-labeled data becomes necessary for further improvement.

For high-value applications, the investment in human labeling is justified. Companies like Vantage, which produces due diligence reports for investment decisions, dedicate staff to labeling and evaluating the quality of question-answer pairs. This reflects the understanding that without at least one human producing high-quality data, systems will struggle to achieve meaningful differentiation in output quality.

The economic argument is compelling: if a model is helping make decisions that involve millions or billions of dollars (as in investment due diligence or hiring), the cost of high-quality human labeling is minimal compared to the value it creates.

---

## How do you handle model evaluation when generating reports rather than simple answers?

Evaluating report generation presents different challenges than evaluating direct question answering. While individual components can be measured with standard metrics, evaluating complete reports often requires human judgment against a defined rubric.

Language models can perform reasonably well as judges against a rubric, but they primarily assess whether all required elements are present rather than providing nuanced feedback on quality or analysis. Human evaluation remains important for assessing whether the analysis itself is valuable and meets business needs.

This challenge mirrors broader evaluation difficulties in the generative AI space, where outputs become more complex and subjective. The solution often involves creating clear rubrics for what constitutes a good report in your specific domain, then combining automated checks with strategic human review.

Teams should focus on defining what makes a report valuable to their specific users rather than pursuing generic quality metrics. This might involve understanding whether users need comprehensive information, specific recommendations, or particular formatting that helps with decision-making.

---

## What broader trends are emerging in AI consulting?

The AI consulting landscape is evolving rapidly, with several key trends emerging:

1. **Shift from implementation to experimentation**: More consulting work now involves helping teams design and run effective experiments rather than just implementing specific techniques. This includes teaching scientific methods, hypothesis formation, and systematic testing.

1. **Focus on data quality over algorithms**: Successful consultants emphasize improving data quality and data collection processes rather than just applying newer algorithms. Many organizations still lack basic data infrastructure for effective AI work.

1. **Organizational change management**: A significant portion of AI consulting now involves helping teams adapt to new workflows and develop the right skills. This includes teaching software engineers to approach problems more like data scientists.

1. **Economic value alignment**: The most successful AI implementations focus on creating decision-making value rather than just time savings. Products that help customers make better decisions (like hiring recommendations or investment analysis) can command higher prices than those that merely save time.

The role of consultants remains valuable even as AI tools become more accessible because they bring expertise in experiment design, data quality improvement, and aligning AI capabilities with business value.

---

## How will AI impact the consulting industry itself?

The consulting industry will continue to evolve alongside AI advancements, but consultants who adapt will remain valuable. The core value of consulting is increasingly about bringing expertise in scientific methods, data analysis, and business process transformation rather than simply implementing technology.

Several shifts are occurring in the consulting space:

1. **Distribution becomes more important**: Consultants who can effectively share their insights through content creation (blogs, videos, courses) will have advantages in attracting clients.

1. **Process expertise over pure technical knowledge**: As technical implementation becomes easier with AI tools, consultants who understand how to change organizational processes and workflows become more valuable.

1. **Organization and workflow design**: Consultants who can help structure workflows and processes that leverage AI effectively will remain in demand, even as some technical implementation work becomes automated.

1. **Connection to economic value**: Consultants who can clearly connect AI capabilities to business value and ROI will continue to thrive, focusing less on technology and more on business outcomes.

While AI will automate some aspects of consulting work, it simultaneously creates new opportunities for consultants who can help organizations navigate the complex landscape of AI implementation and business transformation.

---

## How should we handle training data contamination from AI-generated content?

As more content on the internet becomes AI-generated, concerns about training data contamination and potential "model collapse" are valid but may be overstated for several reasons:

1. **Unexplored modalities**: Even if text data becomes saturated with AI-generated content, there are many other modalities (video, computer interaction data, etc.) that remain largely untapped for training.

1. **Mode covering vs. mode collapse**: Advanced research at organizations like OpenAI focuses on developing models that can identify multiple solution modes rather than collapsing to the lowest-resistance path. Models that are "mode covering" can maintain diversity in their outputs even when trained on some low-quality data.

1. **Real-world data sources**: For many specialized applications, the most valuable data isn't from the public internet but from proprietary sources or human interaction with systems. This data remains largely uncontaminated.

1. **Post-training refinement**: Much of the current improvement in AI models comes from post-training techniques like RLHF rather than pre-training alone. This allows models to improve based on high-quality human feedback even if pre-training data becomes noisier.

OpenAI researchers reportedly maintain confidence that there's still significant high-quality data available, suggesting that concerns about running out of training data may be premature.

---

## What are emerging trends in AI tool development?

Several noteworthy trends are emerging in AI tool development:

1. **Advanced agents like Manus**: New tools like Manus are providing powerful capabilities by combining foundation models (like Claude Sonnet) with extensive tooling. While details are limited, these systems represent a new generation of AI assistants with enhanced capabilities.

1. **Cloud Code improvements**: Cloud Code has shown impressive performance for specific tasks, sometimes outperforming tools like Cursor for certain types of development work. However, success often depends on the user's expertise in the domain they're working in - users still need significant knowledge to effectively guide AI tools.

1. **Context management evolution**: Newer AI tools are improving how they manage context over time, creating better continuity between sessions and maintaining understanding of project requirements.

1. **Focus on expert augmentation**: The most successful AI tools are those that augment human expertise rather than trying to replace it entirely. Tools work best when users have clear goals and domain knowledge, with the AI handling implementation details.

Despite significant advances in AI capabilities, domain expertise remains crucial for effective use of these tools. The relationship between user expertise and AI capabilities creates a complex dynamic where both need to evolve together for optimal results.

---

## How will data collection evolve for AI applications?

Data collection for AI is shifting in several important ways:

1. **Purposeful logging**: Companies are moving beyond debugging-focused logging to capturing data specifically designed for model training. This requires engineers to think about what signals might be useful for future models rather than just for troubleshooting.

1. **Structured feedback collection**: More companies are implementing systematic ways to collect user feedback and interactions, recognizing these signals as valuable training data rather than just product metrics.

1. **Data quality over quantity**: There's growing recognition that having smaller amounts of high-quality, well-labeled data is often more valuable than vast amounts of noisy data.

1. **Economic value alignment**: Organizations are increasingly evaluating what data to collect based on economic value rather than technical feasibility alone. This means focusing data collection efforts on areas where improved model performance translates directly to business outcomes.

Many companies still struggle with basic data collection infrastructure, often lacking the systems needed to capture useful signals from user interactions. Building these foundations remains a critical first step before more advanced AI applications can be developed.

---

## How should we think about distribution and economic viability in AI products?

The most successful AI applications focus on creating decision-making value rather than just time savings. This fundamental shift in value proposition affects pricing, distribution, and product design:

1. **Value-based pricing**: Products that help customers make better decisions (like hiring recommendations or investment analysis) can command higher prices than those that merely save time. For example, recruiters charge 25% of a hire's salary not because they save time but because they help make better hiring decisions.

1. **Structured outputs**: There's increasing value in AI systems that produce standardized, structured outputs (like reports) rather than just answering ad-hoc questions. This creates more consistent value and makes the outputs more directly usable in business processes.

1. **Domain specialization**: Applications focused on specific domains with clear economic value (financial analysis, legal research, specialized technical fields) can support higher pricing than general-purpose AI tools.

1. **Content as marketing**: For many AI consultants and product builders, content creation (blog posts, courses, etc.) derived from their expertise serves as efficient marketing. This "sawdust" from their core work helps attract clients and build credibility.

The most economically viable AI products are those that align directly with high-value business decisions rather than just providing generalized capabilities or incremental efficiency improvements.

---

## What recommendations do you have for structuring the course and its content?

Several suggestions emerged for improving the course structure and content:

1. **Better content organization**: Ensure core videos and tutorials are prominently featured in the main menu rather than buried under multiple links. This would improve discoverability and help students stay on track.

1. **Standardized office hours format**: Implement a consistent format for office hours, with the first 10-20 minutes dedicated to setting context about the week's material before moving to questions. This helps orient participants who may be joining different sessions.

1. **Email reminders with direct links**: Send regular emails with direct links to the week's core videos and tutorials to ensure students know exactly what to watch and when.

1. **Calendar integration**: Consider adding placeholder calendar events for self-study time to help students schedule time to watch asynchronous content.

1. **Expanded coverage of enterprise tools**: While OpenAI tools were featured prominently for practical reasons, more coverage of enterprise platforms (Azure, AWS, Google Vertex) would be valuable for many students working in corporate environments.

1. **Open-source alternatives**: Include more examples using open-source tools alongside commercial offerings, especially for cases where data residency requirements make cloud services challenging.

The feedback emphasized that while the course content was valuable, improvements to structure and discoverability would help students manage the significant amount of material more effectively.

---

## How can we use Slack effectively after the course ends?

The Slack channel will remain available as an ongoing resource for students after the course concludes. Several recommendations for effective use include:

1. **Specific questions get better answers**: When asking questions in Slack, provide specific details about your use case, what you've already tried, and exactly what you're trying to accomplish. This allows for more targeted and helpful responses.

1. **Share real-world applications**: Sharing how you're applying concepts from the course to real projects provides valuable context for others and creates learning opportunities for everyone.

1. **Ongoing community learning**: The Slack channel offers an opportunity to continue learning from peers who are implementing RAG systems across different industries and use cases.

1. **Access to course materials**: All course materials will remain accessible through Maven, and the Slack community provides a way to discuss those materials as you continue to review them.

The instructor emphasized that students will get as much value from the community as they put in through specific, thoughtful questions and sharing their own experiences.

---

## What future trends do you anticipate in AI development?

Several key trends are likely to shape AI development in the near future:

1. **Structured output generation**: The ability to generate consistent, structured reports and analyses will become increasingly valuable, particularly for business applications where standardized formats are essential.

1. **Report generation workflows**: Building on the structured output trend, more sophisticated workflows for generating comprehensive reports from multiple data sources will become mainstream.

1. **Scientific approach to AI development**: Organizations that adopt rigorous experimentation, hypothesis testing, and data analysis will pull ahead of those that simply implement the latest techniques without careful evaluation.

1. **Economic alignment**: AI applications that directly support high-value decision making will see stronger adoption and commercial success compared to those that merely provide incremental efficiency improvements.

1. **Integration of multiple modalities**: While still evolving, the ability to reason across text, images, video, and interactive data will create new application possibilities, though many practical applications will still focus on extracting structured information from these inputs rather than general understanding.

The most successful organizations will be those that develop systematic processes for continuous improvement of their AI systems rather than chasing the latest models or techniques without a clear evaluation framework.

---

## How do you balance providing generic AI solutions versus domain-specific implementations?

The balance between generic AI solutions and domain-specific implementations depends on both economic factors and technical feasibility:

1. **Start with domain specificity**: Focusing on specific domains allows for more valuable outputs, better evaluation, and clearer value propositions. This approach makes it easier to create systems that provide significant value.

1. **Specialize by intent rather than content**: Even within a domain, segmenting by user intent (what they're trying to accomplish) rather than just content type creates more focused and effective solutions.

1. **Economic viability**: Domain-specific solutions can often command higher prices because they solve specific high-value problems rather than providing general capabilities. This makes them more economically viable despite smaller potential market size.

1. **Technical feasibility**: Creating effective general-purpose AI systems remains technically challenging, while domain-specific implementations can achieve high performance by narrowing the scope of what they need to handle.

For most organizations building AI applications, starting with a specific domain and set of well-defined use cases is likely to produce better results than attempting to build general-purpose systems. This focus allows for better data collection, more effective evaluation, and clearer alignment with business value.

---

## Key Takeaways and Additional Resources

### Key Takeaways:

- Deep Research can be understood as RAG with high-quality data sources and strong reasoning capabilities
- Structured reports often provide more business value than ad-hoc question answering
- Long context windows should be leveraged first when possible before falling back to chunking
- Human-labeled data remains essential for high-quality RAG systems, especially as systems reach the limits of improvement from synthetic data
- Evaluating report generation often requires human judgment against defined rubrics
- AI consulting is shifting toward experimental design and process transformation rather than just implementation
- Data collection is evolving to focus more on purposeful logging and structured feedback collection
- The most economically viable AI products align with high-value business decisions rather than just providing efficiency improvements
- Content organization and standardized formats for course materials can significantly improve the learning experience
- Domain-specific AI implementations typically provide better economic and technical outcomes than general-purpose solutions

### Additional Resources:

- [The Future of RAG](https://jliu.net/blog/future-of-rag) - Jason Liu's blog post on where RAG is heading
- [Deep Research](https://openai.com/index/introducing-deep-research/) - OpenAI's introduction to Deep Research
- [Vantage](https://www.vantage.co/) - Company mentioned as an example of advanced report generation
- [Claude 3.7 Sonnet](https://www.anthropic.com/news/claude-3-7-sonnet) - Latest model referenced in discussions
- [Cloud Code](https://cloud.google.com/code) - AI coding tool discussed in the sessions
- [Manus](https://manus.ai/) - Emerging AI agent mentioned in the discussions

---

IF you want to get discounts and 6 day email source on the topic make sure to subscribe to

<script async data-uid="010fd9b52b" src="https://fivesixseven.kit.com/010fd9b52b/index.js"></script>

---

## How should we understand precision in the context of LLMs and RAG?

Precision has become increasingly important as most people are comfortable adding substantial information to the context window. The key question is how sensitive these models are to ambiguous or irrelevant information.

Most current models are very good at recall because they're optimized for "needle in the haystack" tests. Due to the attention mechanism with sliding windows, they can typically catch important information even when it's buried among other content. However, the sensitivity to irrelevant information is less well-studied.

As we increase the amount of data in the context, we need to understand what precision looks like and how it correlates with factuality or answer quality. Earlier models like GPT-3.5 were quite sensitive to long context with low precision - if you gave them too much information, they would "overthink" because of the volume of content to process.

This is why it's valuable to experiment with different retrieval settings: "For the top 10 documents, this is my precision and recall; for my top 25 documents, this is my precision and recall. If my recall is not increasing as a function of K (the number of documents), that's where I decide to set a threshold."

Some people set thresholds based on re-ranker scores, but that can be dangerous since these scores aren't true probabilities. You can't just set 0.5 as a universal threshold - you need to understand the precision-recall tradeoffs for your specific application.

**_Key Takeaway:_** Models can be sensitive to low-precision context, where irrelevant information causes them to incorporate red herrings into answers. Testing different document count thresholds is more reliable than using arbitrary re-ranker score cutoffs.

!!! success "Key Takeaway"
Models can be sensitive to low-precision context, where irrelevant information causes them to incorporate red herrings into answers. Testing different document count thresholds is more reliable than using arbitrary re-ranker score cutoffs.

---

## What role can small language models play in a RAG architecture?

Small language models can serve several valuable functions within a RAG system:

First, they can rewrite queries quickly and efficiently. For example, if a user asks "What is happening this week?", a small model could convert this into a structured query like a JSON object specifying "search all documents where the datetime is between today and today minus 7 days." This type of entity resolution and query parsing doesn't require the full knowledge of a large model but benefits from the lower latency of smaller models.

Second, small models can build better embedding spaces. Most current embedding models are relatively simple, but a small language model fine-tuned on your specific task could significantly improve embedding quality or re-ranking performance.

In this context, I think of "small" as meaning lower latency with less world knowledge - models that can perform specific tasks efficiently without needing to understand everything about the world.

**_Key Takeaway:_** Small language models can enhance RAG systems through query rewriting and improved embeddings, offering lower latency for specific tasks that don't require comprehensive world knowledge.

!!! success "Key Takeaway"
Small language models can enhance RAG systems through query rewriting and improved embeddings, offering lower latency for specific tasks that don't require comprehensive world knowledge.

---

## How can we measure quality in multi-turn conversations?

When evaluating multi-turn exchanges like simulated customer interactions or teacher training scenarios, there are several approaches to consider.

One approach is to model the interaction as a state machine or "LangDraft" type model where there are defined states that can be traversed. For example, in a customer support scenario, you might have an intake state, followed by various question states, triage states, and resolution states.

We've used this with "LLM therapists" where the system might say, "I can tell you're angry. Let me transition you to this sub-draft that deals with negative emotions." The user remains in that state until they've acknowledged something, then returns to the main flow.

Another approach is to use rubrics and data mining. We extract examples from historical transactions that match specific rubric criteria, then have experts score these examples. These scored examples become few-shot examples for future evaluations.

For instance, with venture capital funding requests, we might extract 200 examples of founders discussing how well they know each other, then have experts grade these as good, bad, or great. This creates a training set for evaluating future conversations.

The model we build with these rubrics typically extracts scores for 30+ criteria, with LLMs giving scores from 0-4, which then feed into a logistic regression model. This makes the evaluation somewhat explainable - if a candidate gets prioritized unexpectedly, we can see which features drove that decision.

**_Key Takeaway:_** For evaluating multi-turn conversations, combine state machines to enforce guardrails with human-labeled examples to create scoring rubrics. Using a simple model like logistic regression on top of LLM-generated feature scores maintains interpretability.

!!! success "Key Takeaway"
For evaluating multi-turn conversations, combine state machines to enforce guardrails with human-labeled examples to create scoring rubrics. Using a simple model like logistic regression on top of LLM-generated feature scores maintains interpretability.

---

## How do you approach data analysis to find business value in AI applications?

My favorite content in the course is actually weeks 4 and 5, where I cover my process for data analysis and uncovering new capabilities needed in AI systems.

When analyzing data from AI applications, I look for two main types of issues:

1. Inventory issues: These occur when the system lacks the necessary data to fulfill user requests. For example, if users search for content that doesn't exist in your database, the solution isn't to improve the AI - it's to add the missing content. Many companies don't realize their inventory might be the problem rather than their AI.

2. Capabilities issues: These involve functionality gaps where the system can't perform certain types of queries or filters. For instance, you might need to add metadata filters or specialized search capabilities to handle specific user needs.

I've found tremendous business value by identifying these issues through data analysis. In one case with a restaurant voice AI system, we discovered that when the AI attempted upselling, it generated 20% more revenue 50% of the time - a 10% overall increase. However, the agent only tried upselling in 9% of calls.

The solution wasn't to improve the AI's core capabilities but to add a simple check ensuring the agent always asks if the customer wants anything else before ending the call. This small change could generate an additional $2 million in revenue by increasing upselling attempts from 9% to 40%.

For me, the most enjoyable work is identifying these business opportunities that don't necessarily require complex AI improvements. Software engineers often aren't trained to think this way, but my background in data science makes this approach natural.

**_Key Takeaway:_** The biggest business value often comes from analyzing usage patterns to identify inventory gaps or missing capabilities, rather than improving core AI performance. Simple changes like adding missing data or implementing basic business rules can deliver millions in value.

!!! success "Key Takeaway"
The biggest business value often comes from analyzing usage patterns to identify inventory gaps or missing capabilities, rather than improving core AI performance. Simple changes like adding missing data or implementing basic business rules can deliver millions in value.

---

## How do you balance technical implementation with business outcomes?

I've worked with many companies where they think they want me to make their AI better, but my actual job is to make their business better. There's often substantial money to be captured by focusing on business outcomes rather than technical improvements.

For example, with a construction project, I spoke with contractors to understand their actual pain points. While they initially thought they needed better document search, the real issue was tracking delays and identifying who was causing them. This led us to implement contact search with metadata filters - a solution that addressed a $100,000/month problem.

Similarly, with Netflix, if users search for "Oscar-nominated" movies but get results about Oscar Wilde or actors named Oscar, the solution might not be more sophisticated AI. It could be as simple as paying IMDB for better awards metadata.

I'm constantly looking for these opportunities where a relatively simple technical solution can unlock significant business value. This approach has been much more impactful than pursuing technical sophistication for its own sake.

**_Key Takeaway:_** Focus on business outcomes over technical sophistication. Often the highest-value solutions involve simple changes that address real user needs rather than complex AI improvements.

!!! success "Key Takeaway"
Focus on business outcomes over technical sophistication. Often the highest-value solutions involve simple changes that address real user needs rather than complex AI improvements.

---

## What are your thoughts on the latest AI developments like Claude 3?

I'm currently reviewing the entire Instructor codebase to adapt it for Claude 3. The model is making about 15 pull requests for me, so we'll see how that goes.

Regarding the guest speakers we've had, I found the Chroma presentation particularly valuable for its hands-on, practical approach. While the Exa presentation was more high-level and story-focused, both offered valuable perspectives.

I try to balance technical depth with accessibility in these sessions. When Nils gave his talk, it quickly became very technical with neural network diagrams and mathematical equations, and I could see people leaving the call. It's challenging to find the right balance between technical content and storytelling.

**_Key Takeaway:_** Balancing technical depth with accessibility is crucial when presenting AI concepts. Different audiences require different approaches to effectively communicate complex ideas.

!!! success "Key Takeaway"
Balancing technical depth with accessibility is crucial when presenting AI concepts. Different audiences require different approaches to effectively communicate complex ideas.

---

## How should we approach building RAG applications for course materials?

If someone wanted to build a RAG application over all the course transcripts and office hours, I'd love to see that. However, this would quickly reveal the limitations of simple chunking approaches.

You'd discover that people have different capability requests - like wanting to know who asked specific questions or what was discussed in a particular week. This would require metadata filters for cohort numbers, transcript types (lectures vs. office hours vs. lightning lessons), and speaker identification.

You might also need to handle requests for information about guest speakers, like their LinkedIn profiles. All of these are inventory issues that could be solved by ensuring you have the right metadata alongside your content.

For a dataset as small as course transcripts, long-context models like Claude 3 might work well without complex RAG. It's really the enterprise use cases with massive document collections that need sophisticated RAG approaches.

**_Key Takeaway:_** Even simple datasets like course transcripts reveal the importance of metadata and structured information for effective retrieval. Many issues are inventory problems rather than AI problems.

!!! success "Key Takeaway"
Even simple datasets like course transcripts reveal the importance of metadata and structured information for effective retrieval. Many issues are inventory problems rather than AI problems.

---

## How do you handle UI/UX development for AI applications?

I try to write most things as command line tools - I'm a "filthy machine learning Python engineer" who finds any UI to be too much work. Even Streamlit feels excessive to me when a command line interface would suffice.

That said, Claude has demonstrated how well you can do with thoughtful UX patterns. In Week 3, I'll talk about UX patterns that make applications feel responsive - like how Claude shows progress counters as it's uploading and downloading tokens, ensuring something on the page is always moving to indicate work is happening.

For those who need to build UIs but lack JavaScript skills, LLMs are remarkably good at writing JavaScript. I've built many bespoke data labeling applications in just 5 hours by prompting models to convert JSON structures to PostgreSQL databases and build the corresponding UIs.

The software can be ephemeral enough that I don't worry about long-term maintenance. For more polished applications, I recommend checking out Lovable.dev - I've built about 20 apps with them that work quite well.

**_Key Takeaway:_** Focus on learning the concepts rather than specific implementation details. Modern LLMs can generate high-quality UI code, making it easier than ever to build functional applications without deep frontend expertise.

!!! success "Key Takeaway"
Focus on learning the concepts rather than specific implementation details. Modern LLMs can generate high-quality UI code, making it easier than ever to build functional applications without deep frontend expertise.

---

## What's been your most rewarding project in the AI space?

My background is in physics - I initially thought the universe would generate the most interesting datasets. Then I went to Facebook because I believed people-to-people interactions would be the most fascinating data. Now I'm focused on people-to-AI interactions, and in the future, it will likely be AI-to-AI interactions. I'm essentially chasing the most interesting datasets I can analyze.

The most rewarding projects have been those where data analysis revealed clear business opportunities. For instance, with the restaurant voice AI system, identifying the upselling opportunity was straightforward but incredibly valuable.

I enjoy working with teams that have access to subject matter experts who can help interpret the data. For the construction project, I spoke with contractors wearing hard hats on Zoom to understand why certain questions were valuable and what problems they were trying to solve.

This approach of combining data analysis with domain expertise has consistently led to high-impact solutions that address real business needs rather than just technical challenges.

**_Key Takeaway:_** The most rewarding AI projects combine data analysis with domain expertise to identify high-impact business opportunities rather than pursuing technical sophistication for its own sake.

!!! success "Key Takeaway"
The most rewarding AI projects combine data analysis with domain expertise to identify high-impact business opportunities rather than pursuing technical sophistication for its own sake.

---

## Final thoughts on balancing course workload

I recognize that the course material can be overwhelming, especially for those balancing it with full-time jobs. We'll have no notebooks in Week 3, which should provide a buffer, and you'll always have access to the Slack channel even after the 6 weeks are over.

For those feeling overwhelmed, remember that many people take multiple cohorts to fully absorb the material. The flexible structure is intentional - unlike more prescriptive courses, this approach allows you to focus on what's most relevant to your specific needs.

As one participant noted, they've found at least one "golden nugget" from each session so far, including the introduction where I presented the "sandwich view" of RAG systems. These conceptual frameworks can provide clarity when you're deep in implementation details.

Remember that the AI field is moving incredibly quickly, and none of us can absorb everything. The goal isn't to become an expert on everything but to get really good at leveraging AI to stay ahead of everyone else.

**_Key Takeaway:_** Learning complex technical skills requires finding the right balance between depth of content and time for absorption. Focus on what's most relevant to your needs and remember that continuous learning is more important than perfect comprehension.

---

FAQs

!!! success "Key Takeaway"
Learning complex technical skills requires finding the right balance between depth of content and time for absorption. Focus on what's most relevant to your needs and remember that continuous learning is more important than perfect comprehension.

---

## How can I balance this course with my day job?

Managing this course alongside your regular work can be challenging. Many students find success by aligning the course with existing work projects, allowing them to apply what they're learning directly to their professional tasks. If you don't have a relevant project, the course notebooks provide boilerplate code you can use as a starting point. Remember that Week 3 has no notebooks, which gives you a buffer to catch up if needed. The course is designed with some flexibility, so you can prioritize the most relevant content for your needs.

---

## What should I do if I don't have a specific project to apply the course material to?

You can start with the boilerplate code provided in the notebooks. These are designed to demonstrate key concepts even without a specific application in mind. Additionally, consider looking for datasets from colleagues or within your organization that might benefit from the techniques taught in the course. Many people have conversation data or other information they're not sure how to leverage effectively. The course materials are structured to help you experiment with these techniques regardless of whether you have a specific project.

---

## How are the course materials structured?

The course includes lecture videos, notebooks with code examples, office hours, and summary notes. Each set of notebooks focuses on a specific theme or concept, such as synthetic data generation or evaluation metrics. The notebooks are designed to be practical and applicable to real-world scenarios. Week 3 has no notebooks, providing a buffer period. Weeks 4-5 focus on data analysis processes and building specific tools based on identified needs. The course also includes guest lectures from industry experts to provide different perspectives.

---

## Where can I find the summary notes and FAQs?

Currently, summary notes are posted in Slack, but they will eventually be available in Notion or another website format. Many students find these notes helpful as they allow them to focus more on understanding the content rather than taking extensive notes during lectures.

---

## What's the instructor's approach to evaluating RAG applications?

The instructor emphasizes a data-driven approach to evaluations rather than relying on subjective assessments. This includes measuring precision and recall for different numbers of retrieved documents, understanding how models respond to ambiguous information, and using metrics to make informed decisions about system design. The instructor discourages using adjectives to describe performance and instead encourages teams to use numbers, plots, and quantifiable metrics to evaluate their systems.

---

## How can small language models be used in a RAG architecture?

Small language models can serve several purposes in a RAG architecture. They can be used to quickly rewrite queries, breaking them down into more structured formats. They can help build better embedding spaces or re-rankers that are fine-tuned for specific tasks. Small language models generally offer lower latency with less world knowledge, making them suitable for specific components of a RAG system where full context understanding isn't necessary.

---

## What are the most valuable insights from the course so far?

Many students highlight the "sandwich view" of RAG systems (where RAG is presented as a recommendation system between LLM layers) as particularly insightful. The course provides practical "golden nuggets" in each session, including frameworks for thinking about RAG applications, evaluation techniques, and implementation strategies. The balance between technical details and storytelling across different guest lectures has been valuable for understanding both theoretical concepts and practical applications.

---

## What's the instructor's perspective on building UI/UX for LLM applications?

The instructor suggests focusing on understanding concepts rather than specific UI technologies. Command-line tools can be highly effective for many applications, and modern LLMs are excellent at generating JavaScript and other frontend code when needed. Understanding server-sent events and streaming is particularly important for creating responsive LLM applications. The instructor emphasizes that streaming is essential for good user experience - applications without streaming capabilities are generally considered subpar in the current landscape.

---

## How does the instructor approach business value in AI projects?

The instructor focuses on identifying business value through data analysis rather than just improving AI capabilities. This involves analyzing user interactions, identifying patterns, and determining whether issues are related to inventory (missing data) or capabilities (features the system can't perform). Often, the most valuable insights come from discovering simple business improvements that don't require complex AI solutions. The instructor recommends working closely with subject matter experts to understand the real business needs behind technical requirements.

---

## Will there be opportunities to continue learning after the course ends?

Yes, students will still have access to Slack after the 6-week course concludes, and the instructor encourages continued questions. Additionally, students can join future cohorts of the course if they need more time to absorb the material. Many students find they benefit from going through the content multiple times as the field evolves.

---

## How should we understand precision in the context of LLMs and RAG?

Precision has become increasingly important as most people are comfortable adding substantial information to the context window. The key question is how sensitive these models are to ambiguous or irrelevant information.

Most current models are very good at recall because they're optimized for "needle in the haystack" tests. Due to the attention mechanism with sliding windows, they can typically catch important information even when it's buried among other content. However, the sensitivity to irrelevant information is less well-studied.

As we increase the amount of data in the context, we need to understand what precision looks like and how it correlates with factuality or answer quality. Earlier models like GPT-3.5 were quite sensitive to long context with low precision - if you gave them too much information, they would "overthink" because of the volume of content to process.

This is why it's valuable to experiment with different retrieval settings: "For the top 10 documents, this is my precision and recall; for my top 25 documents, this is my precision and recall. If my recall is not increasing as a function of K (the number of documents), that's where I decide to set a threshold."

Some people set thresholds based on re-ranker scores, but that can be dangerous since these scores aren't true probabilities. You can't just set 0.5 as a universal threshold - you need to understand the precision-recall tradeoffs for your specific application.

**_Key Takeaway:_** Models can be sensitive to low-precision context, where irrelevant information causes them to incorporate red herrings into answers. Testing different document count thresholds is more reliable than using arbitrary re-ranker score cutoffs.

!!! success "Key Takeaway"
Models can be sensitive to low-precision context, where irrelevant information causes them to incorporate red herrings into answers. Testing different document count thresholds is more reliable than using arbitrary re-ranker score cutoffs.

---

## What role can small language models play in a RAG architecture?

Small language models can serve several valuable functions within a RAG system:

First, they can rewrite queries quickly and efficiently. For example, if a user asks "What is happening this week?", a small model could convert this into a structured query like a JSON object specifying "search all documents where the datetime is between today and today minus 7 days." This type of entity resolution and query parsing doesn't require the full knowledge of a large model but benefits from the lower latency of smaller models.

Second, small models can build better embedding spaces. Most current embedding models are relatively simple, but a small language model fine-tuned on your specific task could significantly improve embedding quality or re-ranking performance.

In this context, I think of "small" as meaning lower latency with less world knowledge - models that can perform specific tasks efficiently without needing to understand everything about the world.

---

## How can we measure quality in multi-turn conversations?

When evaluating multi-turn exchanges like simulated customer interactions or teacher training scenarios, there are several approaches to consider.

One approach is to model the interaction as a state machine or "LangDraft" type model where there are defined states that can be traversed. For example, in a customer support scenario, you might have an intake state, followed by various question states, triage states, and resolution states.

We've used this with "LLM therapists" where the system might say, "I can tell you're angry. Let me transition you to this sub-draft that deals with negative emotions." The user remains in that state until they've acknowledged something, then returns to the main flow.

Another approach is to use rubrics and data mining. We extract examples from historical transactions that match specific rubric criteria, then have experts score these examples. These scored examples become few-shot examples for future evaluations.

For instance, with venture capital funding requests, we might extract 200 examples of founders discussing how well they know each other, then have experts grade these as good, bad, or great. This creates a training set for evaluating future conversations.

The model we build with these rubrics typically extracts scores for 30+ criteria, with LLMs giving scores from 0-4, which then feed into a logistic regression model. This makes the evaluation somewhat explainable - if a candidate gets prioritized unexpectedly, we can see which features drove that decision.

**_Key Takeaway:_** For evaluating multi-turn conversations, combine state machines to enforce guardrails with human-labeled examples to create scoring rubrics. Using a simple model like logistic regression on top of LLM-generated feature scores maintains interpretability.

!!! success "Key Takeaway"
For evaluating multi-turn conversations, combine state machines to enforce guardrails with human-labeled examples to create scoring rubrics. Using a simple model like logistic regression on top of LLM-generated feature scores maintains interpretability.

---

## How do you approach data analysis to find business value in AI applications?

My favorite content in the course is actually weeks 4 and 5, where I cover my process for data analysis and uncovering new capabilities needed in AI systems.

When analyzing data from AI applications, I look for two main types of issues:

1. Inventory issues: These occur when the system lacks the necessary data to fulfill user requests. For example, if users search for content that doesn't exist in your database, the solution isn't to improve the AI - it's to add the missing content. Many companies don't realize their inventory might be the problem rather than their AI.

1. Capabilities issues: These involve functionality gaps where the system can't perform certain types of queries or filters. For instance, you might need to add metadata filters or specialized search capabilities to handle specific user needs.

I've found tremendous business value by identifying these issues through data analysis. In one case with a restaurant voice AI system, we discovered that when the AI attempted upselling, it generated 20% more revenue 50% of the time - a 10% overall increase. However, the agent only tried upselling in 9% of calls.

The solution wasn't to improve the AI's core capabilities but to add a simple check ensuring the agent always asks if the customer wants anything else before ending the call. This small change could generate an additional $2 million in revenue by increasing upselling attempts from 9% to 40%.

For me, the most enjoyable work is identifying these business opportunities that don't necessarily require complex AI improvements. Software engineers often aren't trained to think this way, but my background in data science makes this approach natural.

**_Key Takeaway:_** The biggest business value often comes from analyzing usage patterns to identify inventory gaps or missing capabilities, rather than improving core AI performance. Simple changes like adding missing data or implementing basic business rules can deliver millions in value.

!!! success "Key Takeaway"
The biggest business value often comes from analyzing usage patterns to identify inventory gaps or missing capabilities, rather than improving core AI performance. Simple changes like adding missing data or implementing basic business rules can deliver millions in value.

---

## How do you balance technical implementation with business outcomes?

I've worked with many companies where they think they want me to make their AI better, but my actual job is to make their business better. There's often substantial money to be captured by focusing on business outcomes rather than technical improvements.

For example, with a construction project, I spoke with contractors to understand their actual pain points. While they initially thought they needed better document search, the real issue was tracking delays and identifying who was causing them. This led us to implement contact search with metadata filters - a solution that addressed a $100,000/month problem.

Similarly, with Netflix, if users search for "Oscar-nominated" movies but get results about Oscar Wilde or actors named Oscar, the solution might not be more sophisticated AI. It could be as simple as paying IMDB for better awards metadata.

I'm constantly looking for these opportunities where a relatively simple technical solution can unlock significant business value. This approach has been much more impactful than pursuing technical sophistication for its own sake.

---

## What are your thoughts on the latest AI developments like Claude 3?

I'm currently reviewing the entire Instructor codebase to adapt it for Claude 3. The model is making about 15 pull requests for me, so we'll see how that goes.

Regarding the guest speakers we've had, I found the Chroma presentation particularly valuable for its hands-on, practical approach. While the Exa presentation was more high-level and story-focused, both offered valuable perspectives.

I try to balance technical depth with accessibility in these sessions. When Nils gave his talk, it quickly became very technical with neural network diagrams and mathematical equations, and I could see people leaving the call. It's challenging to find the right balance between technical content and storytelling.

---

## How should we approach building RAG applications for course materials?

If someone wanted to build a RAG application over all the course transcripts and office hours, I'd love to see that. However, this would quickly reveal the limitations of simple chunking approaches.

You'd discover that people have different capability requests - like wanting to know who asked specific questions or what was discussed in a particular week. This would require metadata filters for cohort numbers, transcript types (lectures vs. office hours vs. lightning lessons), and speaker identification.

You might also need to handle requests for information about guest speakers, like their LinkedIn profiles. All of these are inventory issues that could be solved by ensuring you have the right metadata alongside your content.

For a dataset as small as course transcripts, long-context models like Claude 3 might work well without complex RAG. It's really the enterprise use cases with massive document collections that need sophisticated RAG approaches.

---

## How do you handle UI/UX development for AI applications?

I try to write most things as command line tools - I'm a "filthy machine learning Python engineer" who finds any UI to be too much work. Even Streamlit feels excessive to me when a command line interface would suffice.

That said, Claude has demonstrated how well you can do with thoughtful UX patterns. In Week 3, I'll talk about UX patterns that make applications feel responsive - like how Claude shows progress counters as it's uploading and downloading tokens, ensuring something on the page is always moving to indicate work is happening.

For those who need to build UIs but lack JavaScript skills, LLMs are remarkably good at writing JavaScript. I've built many bespoke data labeling applications in just 5 hours by prompting models to convert JSON structures to PostgreSQL databases and build the corresponding UIs.

The software can be ephemeral enough that I don't worry about long-term maintenance. For more polished applications, I recommend checking out Lovable.dev - I've built about 20 apps with them that work quite well.

**_Key Takeaway:_** Focus on learning the concepts rather than specific implementation details. Modern LLMs can generate high-quality UI code, making it easier than ever to build functional applications without deep frontend expertise.

!!! success "Key Takeaway"
Focus on learning the concepts rather than specific implementation details. Modern LLMs can generate high-quality UI code, making it easier than ever to build functional applications without deep frontend expertise.

---

## What's been your most rewarding project in the AI space?

My background is in physics - I initially thought the universe would generate the most interesting datasets. Then I went to Facebook because I believed people-to-people interactions would be the most fascinating data. Now I'm focused on people-to-AI interactions, and in the future, it will likely be AI-to-AI interactions. I'm essentially chasing the most interesting datasets I can analyze.

The most rewarding projects have been those where data analysis revealed clear business opportunities. For instance, with the restaurant voice AI system, identifying the upselling opportunity was straightforward but incredibly valuable.

I enjoy working with teams that have access to subject matter experts who can help interpret the data. For the construction project, I spoke with contractors wearing hard hats on Zoom to understand why certain questions were valuable and what problems they were trying to solve.

This approach of combining data analysis with domain expertise has consistently led to high-impact solutions that address real business needs rather than just technical challenges.

---

## Final thoughts on balancing course workload

I recognize that the course material can be overwhelming, especially for those balancing it with full-time jobs. We'll have no notebooks in Week 3, which should provide a buffer, and you'll always have access to the Slack channel even after the 6 weeks are over.

For those feeling overwhelmed, remember that many people take multiple cohorts to fully absorb the material. The flexible structure is intentional - unlike more prescriptive courses, this approach allows you to focus on what's most relevant to your specific needs.

As one participant noted, they've found at least one "golden nugget" from each session so far, including the introduction where I presented the "sandwich view" of RAG systems. These conceptual frameworks can provide clarity when you're deep in implementation details.

Remember that the AI field is moving incredibly quickly, and none of us can absorb everything. The goal isn't to become an expert on everything but to get really good at leveraging AI to stay ahead of everyone else.

---

FAQs

---

## How can I balance this course with my day job?

Managing this course alongside your regular work can be challenging. Many students find success by aligning the course with existing work projects, allowing them to apply what they're learning directly to their professional tasks. If you don't have a relevant project, the course notebooks provide boilerplate code you can use as a starting point. Remember that Week 3 has no notebooks, which gives you a buffer to catch up if needed. The course is designed with some flexibility, so you can prioritize the most relevant content for your needs.

---

## What should I do if I don't have a specific project to apply the course material to?

You can start with the boilerplate code provided in the notebooks. These are designed to demonstrate key concepts even without a specific application in mind. Additionally, consider looking for datasets from colleagues or within your organization that might benefit from the techniques taught in the course. Many people have conversation data or other information they're not sure how to leverage effectively. The course materials are structured to help you experiment with these techniques regardless of whether you have a specific project.

---

## How are the course materials structured?

The course includes lecture videos, notebooks with code examples, office hours, and summary notes. Each set of notebooks focuses on a specific theme or concept, such as synthetic data generation or evaluation metrics. The notebooks are designed to be practical and applicable to real-world scenarios. Week 3 has no notebooks, providing a buffer period. Weeks 4-5 focus on data analysis processes and building specific tools based on identified needs. The course also includes guest lectures from industry experts to provide different perspectives.

---

## Where can I find the summary notes and FAQs?

Currently, summary notes are posted in Slack, but they will eventually be available in Notion or another website format. Many students find these notes helpful as they allow them to focus more on understanding the content rather than taking extensive notes during lectures.

---

## What's the instructor's approach to evaluating RAG applications?

The instructor emphasizes a data-driven approach to evaluations rather than relying on subjective assessments. This includes measuring precision and recall for different numbers of retrieved documents, understanding how models respond to ambiguous information, and using metrics to make informed decisions about system design. The instructor discourages using adjectives to describe performance and instead encourages teams to use numbers, plots, and quantifiable metrics to evaluate their systems.

---

## How can small language models be used in a RAG architecture?

Small language models can serve several purposes in a RAG architecture. They can be used to quickly rewrite queries, breaking them down into more structured formats. They can help build better embedding spaces or re-rankers that are fine-tuned for specific tasks. Small language models generally offer lower latency with less world knowledge, making them suitable for specific components of a RAG system where full context understanding isn't necessary.

---

## What are the most valuable insights from the course so far?

Many students highlight the "sandwich view" of RAG systems (where RAG is presented as a recommendation system between LLM layers) as particularly insightful. The course provides practical "golden nuggets" in each session, including frameworks for thinking about RAG applications, evaluation techniques, and implementation strategies. The balance between technical details and storytelling across different guest lectures has been valuable for understanding both theoretical concepts and practical applications.

---

## What's the instructor's perspective on building UI/UX for LLM applications?

The instructor suggests focusing on understanding concepts rather than specific UI technologies. Command-line tools can be highly effective for many applications, and modern LLMs are excellent at generating JavaScript and other frontend code when needed. Understanding server-sent events and streaming is particularly important for creating responsive LLM applications. The instructor emphasizes that streaming is essential for good user experience - applications without streaming capabilities are generally considered subpar in the current landscape.

---

## How does the instructor approach business value in AI projects?

The instructor focuses on identifying business value through data analysis rather than just improving AI capabilities. This involves analyzing user interactions, identifying patterns, and determining whether issues are related to inventory (missing data) or capabilities (features the system can't perform). Often, the most valuable insights come from discovering simple business improvements that don't require complex AI solutions. The instructor recommends working closely with subject matter experts to understand the real business needs behind technical requirements.

---

## Will there be opportunities to continue learning after the course ends?

Yes, students will still have access to Slack after the 6-week course concludes, and the instructor encourages continued questions. Additionally, students can join future cohorts of the course if they need more time to absorb the material. Many students find they benefit from going through the content multiple times as the field evolves.

---

## How should I approach medical RAG systems with complex queries?

When dealing with specialized domains like medical records where users ask comprehensive questions (e.g., "Give a complete medical history of patient X"), the key is understanding that you can't just throw everything into a generic RAG system and expect good results.

I've found that building separate indices for different document categories is essential. For example, with an oil and gas client I'm working with, we're processing millions of PDFs but categorizing them into about five different types: drill logs, specifications, geospatial diagrams, etc.

Within each category, we extract specific data structures. For drill logs, we identify that some pages represent different days of logging, so we extract metadata like dates, drill IDs, and personnel information. This allows us to build specialized tools for querying each data type effectively.

For medical history queries, you'd want to create structured data that can be queried directly - essentially turning it into a "SELECT \* FROM medical_history WHERE client_id = X" type of operation rather than relying on semantic search across unstructured text.

**_Key Takeaway:_** Don't try to build one universal RAG system. Instead, identify the categories of documents in your domain, extract relevant structured data from each category, and build specialized tools to query that structured data effectively.

!!! success "Key Takeaway"
Don't try to build one universal RAG system. Instead, identify the categories of documents in your domain, extract relevant structured data from each category, and build specialized tools to query that structured data effectively.

---

## What's the best approach to handling citations in RAG systems?

When your LLM isn't reliable for generating citations and semantic/fuzzy similarity doesn't work well (particularly in domains with many abbreviations like medicine), you need a more structured approach.

I recommend following Claude's citation approach, which uses XML tags to wrap citations. When you create statements, include XML that references the source ID. In your text chunks, you'll have chunk IDs and other metadata alongside the content.

To make this more precise, especially with longer contexts, include the first three words and last three words of the cited span. For example, if citing "similarity isn't reliable either for our use case," the citation would include both the chunk ID and "start is similarity isn't reliable, end is for our use case."

This approach works well with fine-tuning. We implemented something similar in Instructor, where an answer is structured as a list of facts, each with a substring quote, ensuring alignment between facts and quotes to minimize hallucinations.

**_Key Takeaway:_** Structure your citations with explicit references to chunk IDs and text spans rather than relying on similarity matching. This approach can be implemented through fine-tuning and provides much more reliable attribution.

!!! success "Key Takeaway"
Structure your citations with explicit references to chunk IDs and text spans rather than relying on similarity matching. This approach can be implemented through fine-tuning and provides much more reliable attribution.

---

## Should I use graph-based RAG approaches?

I'm generally skeptical about graph-based RAG systems. In my experience with data analysis over many years, graph databases often fall away in favor of embeddings and SQL databases.

The main challenge with graph RAG is that building out the taxonomy is often harder than you expect. You think you're avoiding the complexity of embedding models, but you're just substituting it with the problem of modeling out the taxonomy, which can be equally challenging.

For most use cases where you might consider a graph, you can achieve similar results with a few SQL joins. Unless you need to do complex traversals (like LinkedIn finding connections-of-connections), the overhead of learning graph query languages and modeling data as graphs usually isn't worth it.

Even Facebook, despite being fundamentally a social graph, uses a very large-scale MySQL instance rather than a dedicated graph database. If you only need one-way traversals, a standard relational database is typically sufficient.

**_Key Takeaway:_** Unless your use case requires complex multi-step graph traversals, you're likely better off using embeddings with SQL databases rather than implementing a graph-based RAG system. The taxonomy development often becomes more complex than the embedding approach you were trying to avoid.

!!! success "Key Takeaway"
Unless your use case requires complex multi-step graph traversals, you're likely better off using embeddings with SQL databases rather than implementing a graph-based RAG system. The taxonomy development often becomes more complex than the embedding approach you were trying to avoid.

---

## How do you recommend clustering and categorizing user queries?

For understanding what users are asking about, we've developed a library called Cura (similar to Anthropic's Clio) that performs population-level analysis of conversation history.

The process works like this:

1. We summarize every conversation
2. We extract key information: languages used, topics, tasks, requests, user complaints, and assistant errors
3. We concatenate everything and create embeddings
4. We perform clustering to identify patterns
5. We use a language model to group and label clusters

This approach gives you insights into what people are asking for, how big each cluster is, and metrics like error rates or user satisfaction for different types of queries. You can then identify which clusters are performing well and which need improvement, helping you decide where to invest in new tools or capabilities.

We're releasing a new version of Cura soon with better ergonomics and UI for exploration. This will be covered in more detail in Week 4 of the course.

**_Key Takeaway:_** Systematic analysis of user queries through summarization, extraction, embedding, and clustering helps identify patterns in how people use your system, allowing you to prioritize improvements where they'll have the most impact.

!!! success "Key Takeaway"
Systematic analysis of user queries through summarization, extraction, embedding, and clustering helps identify patterns in how people use your system, allowing you to prioritize improvements where they'll have the most impact.

---

## What's your recommendation for chunking documentation?

When dealing with documentation PDFs containing tables, definitions, paragraphs, and figures, I challenge the conventional wisdom about chunking. For documentation, I believe the chunk should often be the size of the document page.

The right question to ask is "which page do I need to look on?" rather than trying to break documents into arbitrary chunks. Modern models are large enough to handle page-sized chunks, and documentation typically uses consistent terminology (unlike cases where semantic search helps bridge vocabulary differences).

By combining semantic and lexical search and focusing on page-level retrieval, you can often get better results than with smaller chunks. This approach also respects the semantic boundaries that document authors typically maintain - they rarely split headers from content across pages or break logical sections in awkward places.

**_Key Takeaway:_** For documentation, consider using page-level chunking rather than arbitrary token-based chunking. This respects the document's inherent structure and works well when combined with both semantic and lexical search approaches.

!!! success "Key Takeaway"
For documentation, consider using page-level chunking rather than arbitrary token-based chunking. This respects the document's inherent structure and works well when combined with both semantic and lexical search approaches.

---

## What are the trade-offs between different vector database options?

I generally prefer using Postgres with pgvector because it allows me to join on different tables, which is extremely valuable. However, pgvector doesn't do exhaustive search by default, which can be a limitation with large datasets.

If you're dealing with very large vector collections, consider Timescale's pgvector_scale, which has better streaming methods for exhaustive search. Another advantage of the Postgres approach is that you can install pg_search from PostgresML to get BM25 implementation, giving you both vector search and lexical search in the same database.

This combination of vector search and lexical search in a single database that also supports filtering by metadata (like dates or access permissions) is powerful for real-world applications.

**_Key Takeaway:_** Postgres with pgvector provides a good balance of functionality for most RAG applications, especially when combined with pg_search for lexical search. For very large datasets, consider specialized extensions like pgvector_scale.

!!! success "Key Takeaway"
Postgres with pgvector provides a good balance of functionality for most RAG applications, especially when combined with pg_search for lexical search. For very large datasets, consider specialized extensions like pgvector_scale.

---

## How do you approach building economically valuable AI systems?

When building AI systems, I focus on economic value rather than just time savings. Time savings is bounded - you can only save as much time as someone currently spends. But economic value can be much larger.

For example, with construction blueprints, we realized that simply answering questions about window heights wasn't that valuable - it just saved a worker a few minutes. But by extracting structured data about room counts, building lines, and floor numbers, we could quickly locate the right blueprints when workers were on site, preventing costly delays.

In another case, we built voice agents that call car owners to schedule maintenance appointments. Rather than charging by call duration, the system charges a percentage of what the mechanic makes. This aligns incentives - the AI provider is motivated to resolve phone numbers correctly, ensure calendar synchronization works, and get customers to actually show up.

The most valuable systems help make better decisions, not just answer questions. If you're building a hiring assistant, don't just price based on tokens used - think about what a bad hire costs a company and how much value your system provides by helping them avoid that outcome.

**_Key Takeaway:_** Focus on building systems that drive economic value through better decision-making rather than just answering questions or saving time. Structure your pricing to align with the value you create, such as taking a percentage of revenue generated or costs avoided.

!!! success "Key Takeaway"
Focus on building systems that drive economic value through better decision-making rather than just answering questions or saving time. Structure your pricing to align with the value you create, such as taking a percentage of revenue generated or costs avoided.

---

## How did you handle blueprint analysis for construction projects?

For a construction project involving blueprints, we realized through user query analysis that workers needed to find specific documents based on their location in a building. They'd say things like "I'm on the 40th floor in a room with two bedrooms and a bathroom on the north-facing side - find me the schemas for the windows."

We built a system that extracted structured data from blueprints: which building, which floor, which "line" (position in the building), room counts, and directional orientation. This required a combination of bounding box models and LLMs to identify and extract this information.

The challenge was proving that we needed to invest in these specialized models. By analyzing the types of questions being asked, we could justify building tools that could count rooms, identify directions, and extract other key metadata that made retrieval much more effective.

For specialized domains like blueprints, it's crucial to understand the specific queries users have and build structured data models that directly address those needs rather than relying on generic text embeddings.

**_Key Takeaway:_** For specialized visual content like blueprints, invest in extracting structured data that matches the way users think about and query the information. This often requires specialized models beyond general-purpose LLMs, but the investment pays off in much more effective retrieval.

!!! success "Key Takeaway"
For specialized visual content like blueprints, invest in extracting structured data that matches the way users think about and query the information. This often requires specialized models beyond general-purpose LLMs, but the investment pays off in much more effective retrieval.

---

## Final thoughts on building effective RAG systems

The most successful RAG implementations I've seen share a few common characteristics:

1. They don't try to build one universal system but instead create specialized tools for different document categories and query types
2. They extract structured data that matches the way users think about and query information
3. They combine multiple search approaches - semantic, lexical, and metadata filtering
4. They focus on delivering economic value, not just answering questions
5. They evolve based on systematic analysis of user queries and pain points

As we continue to develop these systems, I expect to see more specialized, domain-specific implementations that go beyond generic question-answering to provide decision support and drive measurable business outcomes. The future of these agents will be selling work and outcomes, not just time and tokens.

---

FAQs

---

## What approach should I take for medical RAG with complex queries?

For complex medical queries like "give a complete medical history of patient," a generic chunking approach isn't sufficient. Instead, build separate indices for different categories of documents and create specific data structures for each type. For example, with medical records, you might create distinct structures for doctor's visits, referral letters, and prescriptions. This allows you to develop targeted tools that can directly query these structures rather than relying on general semantic search across all documents.

---

## How should I handle citations in my LLM responses?

When implementing citations in LLM responses, consider using an XML-based approach similar to Claude's citation system. This involves wrapping citations with XML tags that reference the source chunk ID along with the first and last few words of the cited span. For fine-tuned models, you can train the model to output citations in this format, which provides more precise references than simple chunk IDs. This approach works well even when the model rephrases information from abbreviation-heavy medical texts.

---

## What are your thoughts on graph-based RAG versus traditional approaches?

While graph-based RAG sounds promising, it often substitutes one complex problem (embedding models) with another (taxonomy modeling). For most use cases, a well-structured SQL database with appropriate joins is more practical than implementing a graph database. Graph databases require learning new query languages and modeling approaches, which adds significant overhead. Unless you need complex multi-step traversals (like LinkedIn's connection finder), the benefits rarely outweigh the costs. Most "graph-like" relationships can be effectively modeled with standard SQL joins.

---

## How should I approach chunking for documentation-based RAG?

For documentation, consider using page-level chunking rather than arbitrary token-based chunks. This aligns with how documentation is naturally structured and how authors organize information. Combine semantic search with lexical search for better results, as documentation typically uses consistent terminology. Test this approach with evaluations to verify its effectiveness for your specific use case. Remember that document creators are usually aware of page-level semantics and rarely split important concepts across pages.

---

## How can I understand what my users are asking about?

To analyze user queries effectively, use a conversation analysis tool like Cura. This approach involves:

1. Summarizing each conversation
2. Extracting key information (language used, topics, tasks, requests, complaints)
3. Embedding this data
4. Clustering similar conversations
5. Using an LLM to label and group these clusters

This gives you insights into what users are asking, which features are performing well, and which need improvement. You can then develop targeted tools to address the most common or high-value query types.

---

## What's your experience with extracting data from construction blueprints?

When working with construction blueprints, focus on extracting structured data that answers specific questions users ask. For example, in a condominium project, we extracted data like floor numbers, room counts, directional orientation, and unit identifiers. This required developing specialized bounding box models to identify key elements in the blueprints. The approach was driven by analyzing actual user queries, which revealed they needed to quickly locate specific information like window dimensions or material specifications for particular rooms or floors.

---

## Should I use Postgres with pgvector for my RAG implementation?

Postgres with pgvector is a good choice for RAG implementations because it allows you to combine vector search with traditional SQL queries, enabling pre-filtering by metadata like dates or access permissions. For better performance, consider pgvector-scale, which provides more efficient exhaustive search capabilities for larger datasets. Adding pg_search from PostgreSQL gives you BM25 implementation, allowing you to combine vector search with lexical search in the same database. This approach gives you flexibility to switch between semantic and lexical search while maintaining the ability to join with other data tables.

---

## How do you determine which user questions are worth optimizing for?

Focus on identifying which questions deliver the most economic value, not just which are most common. For example, in a construction project, helping workers quickly locate specific blueprint details might save a few minutes, but identifying unsigned contracts that could cause project delays delivers much higher value. Analyze your user conversations to identify these high-value query patterns, then build specialized tools to address them. The goal isn't just to answer questions faster but to help users make better decisions that impact their bottom line.

---

## What's your recommendation on model selection for RAG applications?

There's no one-size-fits-all model recommendation for RAG. Start by getting your retrieval right, as reasoning over data you can't find is a bigger issue than reasoning capabilities. Then run evaluations to test different models against your specific use cases. Consider your budget constraints across three dimensions: cost, latency, and performance. Your choice will depend on the economic value of the application - a financial analysis tool might justify using GPT-4 at $4 per report if it's still cheaper than human analysis, while a nutritionist website chatbot might need a more cost-effective model.

---

## How can I apply course concepts to my actual project while balancing time constraints?

Several participants expressed the challenge of finding time to apply course concepts to their real-world projects while managing full-time jobs. One participant noted, "I have a day job with a packed schedule. I already have to make room for lectures and these conversations, which leaves very little time to apply this to my project."

This is a common challenge when learning new technical skills alongside existing responsibilities. For those in this situation, I recommend focusing on completing the course first and then applying the knowledge afterward. The community will remain active even after the course ends, with the Slack channel staying open and all videos remaining available.

For those who need more immediate application, consider reaching out about a consulting engagement after the course. The reality is that deep implementation often requires dedicated time that's difficult to carve out while maintaining other responsibilities.

**_Key Takeaway:_** Learning and implementation often need to be sequenced rather than parallel when you have limited time. Focus on absorbing the knowledge first, then plan dedicated time for application afterward.

!!! success "Key Takeaway"
Learning and implementation often need to be sequenced rather than parallel when you have limited time. Focus on absorbing the knowledge first, then plan dedicated time for application afterward.

---

## What happens to the community after the course ends?

While we won't have structured bi-weekly meetings after the course concludes, the Slack channel will remain active, and I'll check it regularly to share resources and interesting developments. All course materials, including videos and the Maven pages, will remain accessible.

The community's activity level will largely depend on participant engagement - "it's basically going to be like however much you put in is what you're going to get out." We don't have a community manager pushing conversations, as my goal isn't to maximize message volume.

Many valuable interactions happen through direct messages rather than in public channels. For example, one participant is about to launch their own company, and we're jumping on calls to discuss their ideas and make introductions.

**_Key Takeaway:_** The community will continue beyond the formal course structure, but its value will depend on your active participation and willingness to engage with others.

!!! success "Key Takeaway"
The community will continue beyond the formal course structure, but its value will depend on your active participation and willingness to engage with others.

---

## How should I handle irrelevant data being pushed into my vector database?

One participant working on an application with high-performance RAG requirements asked about the impact of irrelevant data in their vector database: "How much do I need to worry if there's irrelevant data being pushed into our vector database? Is it not that big of a deal because we have metadata filtering and good retrieval, or is it a big deal?"

This concern tends to be model-specific. Foundation model companies have been optimizing for recall after discovering the "needle in a haystack" problem, where models struggled to find specific information buried in large contexts. While this improved recall, it made models more sensitive to precision issues.

The real risk now is that low precision might hurt your language model's ability to reason correctly. When dealing with irrelevant data, consider whether it's "adversarially irrelevant" - is the data actually conflicting rather than just unnecessary?

For example, in construction documentation, you might have an email saying a wall is yellow, an architect's note saying it's blue, and a text message claiming it's purple. In these cases, you need to establish authority hierarchies or time-based weighting to resolve conflicts.

**_Key Takeaway:_** The impact of irrelevant data depends on whether it's merely unnecessary or actively conflicting. Modern models are optimized for high recall but can be sensitive to precision issues, so conflicting information can be particularly problematic.

!!! success "Key Takeaway"
The impact of irrelevant data depends on whether it's merely unnecessary or actively conflicting. Modern models are optimized for high recall but can be sensitive to precision issues, so conflicting information can be particularly problematic.

---

## What metrics should I monitor for retrieval quality in production?

When asked about vector databases providing retrieval quality measurements, I recommended focusing on metrics you can monitor yourself rather than trusting vendor-provided metrics.

Consider tracking the average cosine distance of your queries over time. If this metric suddenly changes, it could indicate a shift in your data or user behavior. For example, in a previous recommendation system I built, we monitored cosine distance between products and noticed a sudden drop. After investigating by segmenting the data by signup date, gender, and life stage, we discovered we had onboarded many young users through a Super Bowl ad campaign who couldn't afford our $300 clothing items.

You might also monitor average re-ranker scores and look for changes over time or across different user segments. These metrics are more valuable than arbitrary tests created by vector database providers.

**_Key Takeaway:_** Focus on monitoring changes in metrics like average cosine distance rather than absolute values, and segment your analysis by relevant variables to identify the root causes of any shifts.

!!! success "Key Takeaway"
Focus on monitoring changes in metrics like average cosine distance rather than absolute values, and segment your analysis by relevant variables to identify the root causes of any shifts.

---

## What's the best approach for processing complex technical documentation?

A participant working on processing technical manuals for question answering described their current approach: "We're leveraging the internal structure of the document, taking sections, splitting them, but including the hierarchy of titles - section, chapter, and manual title. But it feels naive to me."

This challenge is common when dealing with structured technical content. One approach is to use traversal rather than pure semantic search - similar to how code-based agents navigate repositories. Instead of embedding everything, the system can navigate the document structure to find relevant information.

For example, when working with Brazilian tax codes (400-page PDFs), we implemented a system that traversed the documents using a combination of semantic search, full-text search, and grep-like tools. The system could navigate from main sections to specific appendices to find relevant information.

The key insight is that traversal is still a form of retrieval. As you collect traversal data, you can use it to improve your embedding models, potentially reducing the need for complex traversal in the future.

**_Key Takeaway:_** For complex technical documentation, consider combining semantic search with structural traversal. Use the document's inherent organization to guide your retrieval process, and collect this data to improve your embedding models over time.

!!! success "Key Takeaway"
For complex technical documentation, consider combining semantic search with structural traversal. Use the document's inherent organization to guide your retrieval process, and collect this data to improve your embedding models over time.

---

## Should I build complex hierarchical structures for document retrieval?

When discussing whether to build sophisticated graph structures for document retrieval, I emphasized the importance of getting to usable data quickly: "My metric is: whatever I build should be the thing that gets me to 10,000 rows in a CSV file."

Rather than spending extensive time modeling tax laws as a graph or building complex hierarchical indexes upfront, I recommend chunking everything, getting a working system, understanding the problems, and creating examples. This data-driven approach allows you to identify patterns that can inform more sophisticated solutions later.

The better lesson in AI development is that segmenting and solving individual problems can help you make progress now, while preparing unified datasets that will allow you to combine approaches when technology improves. This mirrors the evolution of speech-to-text systems, which initially required separate stages for waveforms, phonemes, and words before end-to-end solutions became viable.

**Key Takeaway:** Focus on collecting data and building working solutions rather than perfect architectures. The insights gained from real usage will guide your more sophisticated implementations later.

---

## How should we think about the relationship between RAG and agents?

An interesting perspective emerged during our discussion: "RAG is like the superpower for AI right now." We explored how the boundaries between RAG and other AI capabilities are blurring, with one participant noting "grep is RAG" - highlighting that any method of retrieving context for an AI system shares fundamental similarities with RAG.

I've been considering whether we should rename the course to focus on "RAG applications" since modern AI systems are essentially exposing a portfolio of tools to agents. Whether you're using semantic search or a grep-like function to pull in relevant code, you're still finding information to enhance the context available to the model.

The core principle remains the same: "It has to be put into the context at the right time so that you can get the response correct." This perspective frames RAG not just as a specific technique but as a fundamental paradigm for augmenting AI capabilities with relevant information.

Key Takeaway: The distinction between RAG and other AI augmentation approaches is increasingly blurred. The fundamental goal is getting the right information into the context at the right time, regardless of the specific retrieval mechanism.

---

## What's the value of the office hours format for learning?

Several participants expressed surprise at how valuable they found the office hours sessions. One noted, "I thought they wouldn't be useful, but I'm surprised with the quality of the questions being asked."

These interactive sessions provide an opportunity to hear how others are applying the course concepts and to discuss specific challenges that might not be covered in the structured lectures. The questions often reveal practical implementation issues that many participants are facing but might not have articulated themselves.

The conversations also help connect theoretical concepts to real-world applications, making the material more concrete and actionable. For example, our discussion about monitoring cosine distances in production systems provided a practical perspective on evaluation that complements the more structured content on evaluation frameworks.

**_Key Takeaway:_** Interactive learning formats like office hours provide valuable perspectives that complement structured course content, particularly for understanding how concepts apply to diverse real-world scenarios.

!!! success "Key Takeaway"
Interactive learning formats like office hours provide valuable perspectives that complement structured course content, particularly for understanding how concepts apply to diverse real-world scenarios.

---

## How should we pace the course to maximize learning?

When asked about the pacing of the course, I acknowledged that many participants are finding it challenging to keep up with all the material. One suggestion was to include a week in the middle with no new material to allow people to catch up, which received positive feedback.

I noted that Week 3 is intentionally lighter, with only a 40-minute video and no notebooks, designed as a catch-up week. However, I recognized that I should make this more explicit to help participants plan their time.

The six-week format provides more depth than a one-week intensive course would allow, but it requires consistent engagement to get the full benefit. Finding the right balance between comprehensive coverage and manageable pacing remains a challenge.

**_Key Takeaway:_** Learning complex technical skills requires finding the right balance between depth of content and time for absorption and practice. Building explicit catch-up periods into courses can help participants manage their learning journey more effectively.

!!! success "Key Takeaway"
Learning complex technical skills requires finding the right balance between depth of content and time for absorption and practice. Building explicit catch-up periods into courses can help participants manage their learning journey more effectively.

---

## What can we learn from leaked system prompts like Anthropic's Claude?

One participant asked about the recently leaked Anthropic Claude prompt, which was reportedly around 30,000 tokens: "Where does it leave room for actual content to be processed? Is it even realistic or just hype?"

I wasn't surprised by the size of this prompt, explaining that it makes sense for the Claude web app experience, which includes tools for fetching information. The API version likely has a smaller prompt, but it's still substantial if web search capabilities are included.

This reveals how much can be done through prompting without changing model weights. It's remarkable that models can now process 30,000 token system messages when just two years ago, the entire context was limited to 32K tokens.

The existence of such extensive system prompts raises questions about where certain capabilities should reside - in the prompt or in the model weights. For example, if a fetch tool were baked into the model weights, what would happen if you named your custom tool "web_search" and the model tried to call a hardcoded "fetch" function?

**_Key Takeaway:_** Large system prompts demonstrate how much functionality can be implemented through instructions rather than model training. This creates flexibility but also raises important questions about the boundary between prompt engineering and model architecture.

---

FAQs

!!! success "Key Takeaway"
Large system prompts demonstrate how much functionality can be implemented through instructions rather than model training. This creates flexibility but also raises important questions about the boundary between prompt engineering and model architecture.

---

## How can I balance the course with my regular work schedule?

Many participants find balancing the course with their day job challenging. The course requires time for watching lectures, completing exercises, and participating in discussions. Consider setting aside specific time slots in your schedule for course activities and prioritize what aspects are most valuable to you. Remember that you can always revisit materials after the course ends if you're unable to complete everything during the active weeks.

---

## Will course materials remain available after the course ends?

Yes, all course materials including videos, notebooks, and exercises will remain accessible after the course concludes. The Slack channel will also stay active, allowing you to continue asking questions and collaborating with other participants. While structured bi-weekly meetings won't continue, you'll still have access to all resources and can work through them at your own pace.

---

## How active will the community be after the course ends?

The community's activity level will largely depend on participant engagement. While there won't be formal scheduled sessions after the course, the instructors will check the Slack channel regularly and share relevant resources. The value you get from the community will correlate with how much you contribute to it. Many valuable connections happen through direct messages rather than in public channels.

---

## Is there a recommended approach to catching up if I'm behind?

Week 3 is intentionally lighter with only an hour-long video and no notebooks, providing an opportunity to catch up on previous materials. The course team is considering adding a "break week" in future cohorts to give participants more time to process information and complete exercises. Don't worry if you can't complete everything during the course timeframe—the materials will remain available afterward.

---

## How can I apply what I'm learning to my actual projects?

The most effective way to apply course concepts to your work is to start with the exercises to build foundational understanding, then gradually incorporate techniques into your projects. Some participants find it helpful to wait until after the course to fully implement what they've learned, as this allows them to focus on understanding the concepts first. For more personalized guidance, reaching out about consulting engagements after the course can be beneficial.

---

## What's the best approach to RAG (Retrieval-Augmented Generation) for technical documentation?

When working with technical documentation, consider these approaches:

1. Start by focusing on getting retrieval right before worrying about other aspects

1. Use document structure (sections, chapters, titles) to improve chunking

1. Consider a combination of semantic search, full-text search, and traversal approaches

1. Monitor metrics like cosine distance to evaluate retrieval quality

1. Begin with a simple implementation that works for most of your documents rather than trying to solve every edge case immediately

---

## How should I handle irrelevant data in my vector database?

The impact of irrelevant data depends on your specific model and use case. Modern language models are optimized for high recall, which can make them sensitive to low precision issues. Consider whether irrelevant data is merely noise or actually conflicting/adversarial. For conflicting information, you may need to implement authority rules (like prioritizing certain document types) or time-based weighting. Rather than trying to perfect your data filtering upfront, start with a basic implementation, collect examples, and iterate based on actual performance.

---

## Are vector databases providing built-in retrieval quality measurements?

While some vector databases may offer metrics, it's generally better to implement your own monitoring. Focus on tracking metrics like average cosine distance of your queries and monitor how these change over time or across different user segments. This approach allows you to detect shifts in data patterns or user behavior that might affect retrieval quality. Looking at changes in these metrics is often more valuable than the absolute values themselves.

---

## What open-source re-ranking models work well for fine-tuning?

When selecting re-ranking models for fine-tuning, I believe the right approach depends on your specific constraints and data volume. For many scenarios, the BGE models from the Beijing Academy of Artificial Intelligence (BAAI) have proven quite stable and easy to fine-tune with datasets of around 100,000 examples.

The model selection process isn't about finding a single "best" model, but rather systematically testing different options against your specific requirements. I've found that BAAI models tend to have more predictable loss curves during training compared to some alternatives where parameters might need more careful tuning.

Your model selection should consider several factors:

- Latency requirements (5-10 seconds for total search and retrieval in your case)
- Hosting constraints (on-premises deployment for medical applications)
- The volume of training data available
- The trade-off between performance and computational cost

For on-premises medical applications requiring self-hosting, I'd recommend starting with the BGE models and systematically testing different configurations. The process is inherently experimental - you'll likely need to train numerous models with different parameters and dataset preparations before finding the optimal combination.

**_Key Takeaway:_** Don't get fixated on finding the "perfect" model architecture. Instead, create a systematic testing framework where you can evaluate multiple models against your specific constraints of latency, hosting requirements, and performance needs.

!!! success "Key Takeaway"
Don't get fixated on finding the "perfect" model architecture. Instead, create a systematic testing framework where you can evaluate multiple models against your specific constraints of latency, hosting requirements, and performance needs.

---

## How should I approach creating training datasets for embedding models versus re-rankers?

The fundamental difference between training embedding models and re-rankers lies in how they handle similarity scores. Embedding models typically work with triplets (this is similar to that, different from something else) with binary scores of 1 or -1. Re-rankers, however, can be more nuanced with scores like 0.8 or 0.9, allowing for finer distinctions between results.

I've found that focusing first on building a strong dataset for your embedding model is usually the most efficient approach. If you're currently only training on positive examples, incorporating negative examples will dramatically improve performance - we're talking about a 30% improvement rather than just 6%.

For creating effective negative examples, I recommend being strategic rather than random:

In a financial context I worked with recently, we were distinguishing between "fuel" (for employee vehicle reimbursements) and "equipment fuel" (for company vehicles like tractors). Simply using random negative examples wouldn't help the model learn this subtle distinction. Instead, we created hard negatives by:

1. Taking a transaction from one category

1. Finding another transaction in the same category as a positive example

1. Using embedding search to find the most similar transaction from a different category as the negative example

This approach forces the model to learn the meaningful boundaries between similar but distinct concepts. For your medical data with abbreviations that have different meanings in different contexts, you could apply a similar strategy - finding examples where the same abbreviation appears in different contexts to create hard negatives.

**_Key Takeaway:_** Including well-crafted negative examples in your training data is crucial for model performance. Focus on creating "hard negatives" that challenge the model to learn subtle distinctions rather than obvious differences.

!!! success "Key Takeaway"
Including well-crafted negative examples in your training data is crucial for model performance. Focus on creating "hard negatives" that challenge the model to learn subtle distinctions rather than obvious differences.

---

## What are effective sources of negative examples for training data?

Some of the most valuable negative examples come from user interactions that indicate a mismatch between what the system thought was relevant and what the user actually found useful. I've implemented several approaches across different domains:

For citation systems:

When experts review citations and delete ones they find irrelevant, saying "regenerate without this document because it's misleading" - that's a perfect negative example. The question and the deleted chunk form a negative pair for training.

For recommendation systems:

- In content recommendation, when a salesperson deletes a suggested blog post from an automated email, that's a negative example
- In music services like Spotify, skipping a song is a weaker negative signal than deleting it from a playlist
- In e-commerce, items that are purchased together but later returned indicate a false positive that can be used as a negative example

For your medical context, you might consider:

- Tracking when users reject or ignore certain retrieved chunks
- Using expert feedback to identify misleading or irrelevant retrievals
- Creating synthetic data with language models to generate examples where abbreviations are used in different contexts

The key insight is that these high-signal negative examples often come from cases where the system initially thought it was right but was ultimately wrong - these boundary cases are extremely valuable for training.

**_Key Takeaway:_** The most valuable negative examples often come from user interactions that indicate a mismatch between system predictions and actual relevance. Design your system to capture these signals and incorporate them into your training data.

!!! success "Key Takeaway"
The most valuable negative examples often come from user interactions that indicate a mismatch between system predictions and actual relevance. Design your system to capture these signals and incorporate them into your training data.

---

## How should I think about compute allocation in retrieval systems?

When designing retrieval systems, especially for complex documents like legal texts or medical records, I think about it as a fundamental trade-off: where do I want to allocate my compute resources? This is essentially a decision between investing compute at "write time" (indexing) versus "read time" (retrieval).

There are two main approaches to consider:

Contextual retrieval (compute-heavy at write time):

- Rewrite text chunks during indexing to include all necessary context
- For example, converting "He is unhappy with her" to "Jason the doctor is unhappy with Patient X"
- This makes retrieval simpler but requires more upfront processing
- Anthropic has published about this approach for their Claude assistant

Tool use and traversal (compute-heavy at read time):

- Store minimal context in each chunk
- Use additional compute during retrieval to navigate between related chunks
- Similar to how Cursor IDE navigates code by finding functions and then examining surrounding context
- This approach is more flexible but can feel slower to users

For your medical application where the data is self-contained (not requiring external information), and where you want to minimize user wait time, I'd lean toward investing more compute at indexing time. This is especially true since you can run indexing jobs overnight without affecting user experience.

The decision also relates to data normalization - do you want to denormalize data by including related information in each chunk (like adding phone numbers whenever a person is mentioned), or keep information separate and join it at retrieval time? The answer depends on your specific use case and resource constraints.

**_Key Takeaway:_** Frame your retrieval system design as a strategic decision about compute allocation. For medical applications with self-contained data and latency constraints, investing more compute at indexing time to create context-rich chunks will likely provide a better user experience.

!!! success "Key Takeaway"
Frame your retrieval system design as a strategic decision about compute allocation. For medical applications with self-contained data and latency constraints, investing more compute at indexing time to create context-rich chunks will likely provide a better user experience.

---

## What determines the complexity of the architecture I should use?

I believe the volume and quality of your training data should be the primary factor determining architectural complexity. This is a principle I emphasize repeatedly: your dataset size dictates what approaches make sense.

As a general guideline:

- With ~100 examples: Use few-shot prompting
- With thousands of examples: Fine-tune embedding models
- With millions of examples: Fine-tune language models

The data volume determines what's feasible. If you told me you had a million examples, I'd probably just train a language model directly and worry about everything else later. With limited data, you need to be more strategic about targeting specific challenges like medical abbreviations with ambiguous meanings.

This is why I'm skeptical when I see engineers celebrating 98% accuracy on their first model - it usually means they've created a test set that's too easy. As your model improves, you should be making your test data harder by finding more challenging examples. If your retrieval dashboard is showing 95% accuracy, that's a sign you need to create harder test cases.

**_Key Takeaway:_** Let your data volume guide your architectural decisions. With limited data, focus on targeted improvements to specific challenges rather than complex architectures. As your model improves, continuously create harder test cases to drive further improvement.

!!! success "Key Takeaway"
Let your data volume guide your architectural decisions. With limited data, focus on targeted improvements to specific challenges rather than complex architectures. As your model improves, continuously create harder test cases to drive further improvement.

---

## How can I improve my system when I don't yet have real user feedback?

Without real user feedback, you can still make significant progress through synthetic data generation and expert knowledge. For your medical abbreviation challenge, you could:

1. Identify known ambiguous abbreviations in medical contexts

1. Use language models like GPT-4 to generate synthetic examples showing these abbreviations in different contexts

1. Have medical experts validate these examples or create additional ones

1. Build a curated dataset of hard negatives focusing on these ambiguities

This approach lets you systematically address known challenges before deployment. Once you have real users, you can implement feedback mechanisms to capture when they reject or modify system outputs, creating a virtuous cycle of improvement.

Remember that as your system improves, you need to continuously create harder test cases. If you're scoring 95% accuracy, it's not because your AI is exceptional - it's because your test data isn't challenging enough. The goal is to build a dataset that pushes the boundaries of what your system can handle.

**_Key Takeaway:_** Before having real users, leverage synthetic data generation and expert knowledge to create challenging test cases. Design your system to capture user feedback from the start, as this will become your most valuable source of training data once deployed.

---

FAQs

!!! success "Key Takeaway"
Before having real users, leverage synthetic data generation and expert knowledge to create challenging test cases. Design your system to capture user feedback from the start, as this will become your most valuable source of training data once deployed.

---

## What open-source re-ranking models are recommended for fine-tuning?

The Beijing Academy of Artificial Intelligence (BAAI) models, such as BGE re-ranker v3, are often good choices for fine-tuning. These models have proven to be stable during the training process and work well with the sentence transformers library. When selecting a model, consider your specific data volume and performance requirements. Testing multiple models with your dataset is ultimately the best approach to finding the optimal solution for your specific use case.

---

## How should I approach model selection for my re-ranking needs?

Start by exploring models that perform well on MTAB benchmarks on Hugging Face. Consider your constraints around latency, hosting requirements, and data volume. With the right dataset, the process becomes more about searching the model space to find what works best for your specific scenario. For medical or specialized domains, you'll want to test various models against your specific data to determine which one provides the best performance-to-cost ratio.

---

## What are the different types of re-ranking models available?

Re-rankers can be embedding models, cross-encoder models, or even large language models (LLMs). Each has different characteristics: embedding models typically classify results as relevant or not relevant, cross-encoders can provide more nuanced scoring (like 0.8 vs 0.9 relevance), and LLM-based re-rankers (like those used by Exa) can provide sophisticated re-ranking but may have higher latency. Your choice depends on your specific requirements and constraints.

---

## Training Data for Embedding and Re-Ranking Models

How important are negative examples when training embedding models?

Negative examples are extremely valuable when training embedding models. Including hard negatives (examples that are similar but should be classified differently) can improve performance by 30% or more compared to training with only positive examples. These hard negatives help the model learn subtle distinctions that are crucial for accurate retrieval, especially in specialized domains like medicine or legal text.

---

## What's an effective way to generate hard negative examples?

One effective approach is to find examples that are semantically similar but belong to different categories. For instance, if you're working with medical abbreviations that have different meanings in different contexts, you could create examples showing the same abbreviation used in different medical specialties. Another method is to use embedding search to find the most similar items that should be classified differently, rather than just using random negative examples.

---

## How can user feedback be leveraged to improve retrieval models?

User interactions provide valuable signals for creating training data. For example, if users delete a citation or regenerate an answer without a specific document, that's a strong signal that the document was irrelevant (a negative example). Similarly, if users consistently skip or remove certain recommendations, those can be used as negative examples in your training data. These real-world signals often create the most valuable training examples.

---

## What factors should I consider when designing a retrieval system architecture?

Consider where to allocate your compute resources: at indexing/write time or at query/read time. If you invest more in preprocessing your data (like contextual retrieval where you rewrite chunks to include necessary context), your query-time processing can be simpler and faster. Alternatively, you can keep preprocessing minimal and implement more sophisticated query-time processing like document traversal. Your decision should balance user experience requirements, cost constraints, and the specific characteristics of your data.

---

## How do I handle context in long documents where paragraphs depend on previous content?

There are two main approaches: (1) Contextual retrieval, where you rewrite text chunks at indexing time to include all necessary context, making each chunk self-contained; or (2) Document traversal, where your system can navigate through the document at query time to gather needed context. The first approach frontloads the processing cost but enables faster query responses, while the second requires more complex query-time processing but minimizes preprocessing.

---

## What hosting considerations should I keep in mind for medical applications?

For medical applications, especially in European contexts like the Netherlands, you'll likely need to host models on your own hardware or on-premises at hospitals. This requires selecting models that can run efficiently on your available hardware while meeting your latency requirements. Consider models that can be fully self-hosted without external API dependencies, and ensure your architecture complies with relevant healthcare data regulations.

---

## How should we approach evaluation data collection for RAG systems?

One participant was struggling with exporting conversation data from Langsmith for evaluation purposes. This highlights a common challenge with many tracing tools - they're often better at collecting data than exporting it in useful formats.

When Langsmith or similar tools create export difficulties, I recommend two alternative approaches:

1. Direct database storage: Instead of relying on tracing software, consider saving queries directly to your database as the application runs.
   "This is something we do all the time - we just write the question, answer pairs, or chunks to Postgres. That way, we can build UI on top of that database rather than trying to export data out of tools like Langsmith."
1. Create a simple, wide database table that includes:
   - Session ID
   - User ID
   - Query text
   - Retrieved chunks
   - Generated answer

This approach gives you direct access to your data without depending on third-party export functionality, which can be unreliable. It's like building your own analytics system rather than trying to export from something like Data Dog for analysis.

**_Key Takeaway:_** While tracing tools like Langsmith and Log Fire are valuable for telemetry, consider implementing your own database storage for evaluation data to avoid export headaches and gain more control over your analysis process.

!!! success "Key Takeaway"
While tracing tools like Langsmith and Log Fire are valuable for telemetry, consider implementing your own database storage for evaluation data to avoid export headaches and gain more control over your analysis process.

---

## Which models should we use for different RAG applications?

When choosing between models like GPT-4, GPT-4 Turbo, or GPT-3.5, I've observed different selection patterns based on the task's importance and time constraints:

For high-value applications where accuracy is critical (like financial due diligence with 44 data rooms generating reports for clients paying $200,000 annually), companies often default to GPT-4 because "if it is just 2% better, it'll be worth it."

For applications requiring speed, GPT-3.5 or GPT-4 are common choices.

Many developers are now using Gemini for RAG applications because its large context window allows for less precision in retrieval: "You can just be really frivolous with how much context you use."

The decision often comes down to the stakes involved rather than technical benchmarks. For example, when helping sales teams craft follow-up emails containing offers, we use GPT-4 because the potential revenue impact justifies the additional cost.

**_Key Takeaway:_** Model selection should be driven by business value rather than technical specifications alone. For high-stakes applications where even small improvements matter, use the most capable model available. For less critical applications, prioritize speed and cost-efficiency.

!!! success "Key Takeaway"
Model selection should be driven by business value rather than technical specifications alone. For high-stakes applications where even small improvements matter, use the most capable model available. For less critical applications, prioritize speed and cost-efficiency.

---

## How can we enhance report generation with visual elements?

One exciting development in RAG applications is the integration of visual elements into generated reports. I'm currently working with a company on two key improvements:

1. Supporting mermaid diagrams in reports to visualize relationships and processes
1. Intelligently adding relevant images to reports

For example, in a construction permitting application, this could mean automatically including screenshots of potential errors in blueprints with accompanying explanations: "If in a report of predicted potential errors that you should pay attention to on your project, it would actually take a screenshot of the error in the PDF of the blueprint, and then have a narrative around it."

This approach dramatically increases the value of generated reports by combining visual and textual information, making complex issues immediately understandable to users.

**_Key Takeaway:_** The next frontier in RAG applications involves intelligently incorporating visual elements like diagrams and contextual images to enhance understanding and provide more comprehensive analysis.

!!! success "Key Takeaway"
The next frontier in RAG applications involves intelligently incorporating visual elements like diagrams and contextual images to enhance understanding and provide more comprehensive analysis.

---

## How should we manage expectations around AI capabilities?

Managing expectations is one of the biggest challenges when implementing AI systems, especially with clients who have either unrealistic expectations or excessive skepticism.

For construction applications, one participant described their approach: "We try to explain to people that ultimately in our field, you're an architect or a structural engineer. It's your stamp on the docs. You're making the call. We're just here to provide suggestions and things to look out for."

This aligns with my experience working with large enterprises, where much of my consulting work involves "dealing with the personality of the CEO" who might want AI to be a major theme at the next sales conference without understanding the practical limitations.

The most effective approach is focusing on how AI can augment human decision-making rather than replace it. For example, having the LLM run simulations and help humans interpret the results is more realistic than promising fully autonomous systems.

**_Key Takeaway:_** Set clear boundaries around AI capabilities by positioning your system as a decision support tool rather than an autonomous decision-maker. Be explicit about where human judgment remains essential, especially in high-stakes domains like construction or finance.

!!! success "Key Takeaway"
Set clear boundaries around AI capabilities by positioning your system as a decision support tool rather than an autonomous decision-maker. Be explicit about where human judgment remains essential, especially in high-stakes domains like construction or finance.

---

## What's your vision for building open-source AI tools?

When asked about my vision for building AI tools, I explained that my approach differs from the typical venture-backed startup model:

"Before it was okay, consulting can drive revenue that allows us to do open source work. The open source projects don't need to raise venture capital or figure out how to monetize, which changes the nature of the code."

This model allows me to create a portfolio of small, useful tools without worrying about monetization. The course serves as a way to connect with practitioners across different industries and identify common challenges:

"The most I ever did was like 7 clients in a month, and that was kind of a hazy period of my life where I have no memory of what happened. Whereas with the course, I can do these office hours - 10 people show up, great. I can understand how this permitting thing goes, maybe some architectural things, some construction things, some supply chain stuff."

This broader exposure helps me identify patterns across industries, like the common need for better report generation or specialized table parsing, which informs both my consulting work and open-source development.

**_Key Takeaway:_** By funding open-source development through consulting and courses rather than venture capital, I can focus on building genuinely useful tools without the pressure to monetize every component, leading to more sustainable and practical solutions.

!!! success "Key Takeaway"
By funding open-source development through consulting and courses rather than venture capital, I can focus on building genuinely useful tools without the pressure to monetize every component, leading to more sustainable and practical solutions.

---

## How should we think about pricing and value capture for AI systems?

One of the most exciting developments I see in AI is the evolution of pricing models away from usage-based metrics toward outcome-based pricing:

"I'm personally curious about pricing the work that LLMs do. A lot of systems right now are being priced on usage. I'm really excited about what it would mean to have a system that has so much accountability that you can price on the outcome it delivers."

I shared an example of a company that uses voice AI to make calls to car owners on behalf of dealerships. Under a usage-based model, the calls that make the most money are often those that waste time with confusion and errors. But with an outcome-based model, the incentives change dramatically:

"If you change the model to say, 'We want to take 3% of the mechanic's cost,' then it becomes, 'What if we had systems that are intelligently doing upsells? What if we intelligently figure out the right time and try to load balance the mechanic?'"

This shift changes the fundamental question from "How much am I willing to pay to process one PDF file?" (maybe 30 cents) to "Under what circumstances would I be willing to pay $20 to process a PDF?" The answer depends on the business value created.

**_Key Takeaway:_** The future of AI pricing will likely move from usage-based models (tokens, API calls) to outcome-based models where vendors are compensated based on the business value they create. This will drive investment in higher-quality systems that optimize for results rather than minimizing usage.

!!! success "Key Takeaway"
The future of AI pricing will likely move from usage-based models (tokens, API calls) to outcome-based models where vendors are compensated based on the business value they create. This will drive investment in higher-quality systems that optimize for results rather than minimizing usage.

---

## Will AI capabilities eventually be built into platforms or remain in applications?

When asked whether AI capabilities will eventually be absorbed into platforms rather than remaining in applications, I suggested it depends on the time horizon:

"On any reasonable time horizon, it will probably just be the applications. The limiting factor is that for any specific application, we don't actually have the training data to bake this back into the model."

I referenced the "bitter lesson" in AI, which shows that when you have enough data and compute, general approaches tend to outperform specialized ones. However, we first need applications to generate the necessary data:

"We still have to build these applications as sort of sensors to create this data. And then, once we do, we can kind of sidestep the next innovation."

This is similar to how speech recognition evolved from complex phoneme-based systems to end-to-end models, but only after platforms like YouTube created enough data to make this possible.

"We had to build YouTube to produce enough data to get to a world where now we can train the GPT-4 model. So we still have to build these applications as sensors to create this data."

**_Key Takeaway:_** While AI capabilities will eventually be absorbed into platforms, we first need to build applications that generate the necessary training data. This creates a cycle where applications serve as data collection mechanisms that eventually enable more general-purpose AI systems.

!!! success "Key Takeaway"
While AI capabilities will eventually be absorbed into platforms, we first need to build applications that generate the necessary training data. This creates a cycle where applications serve as data collection mechanisms that eventually enable more general-purpose AI systems.

---

## How might AI transform business models and value chains?

I believe AI will fundamentally change how businesses capture value, potentially shifting from software-as-a-service models to more integrated approaches:

"Everything stops becoming SaaS budget and it's all headcount budget. If you absorb this entire 'dealership calls car owner to get them in the mechanic' thing, at some point you're just a sales guy."

This could lead to companies expanding vertically to capture more of the value chain:

"Why don't you just own the entire value chain? Because then you can really price on the outcome that you're trying to deliver rather than just tokens."

While this approach means taking on additional complexity (like owning car mechanics with "all the pros and cons"), it allows for capturing more of the value created. This is similar to how I view the difference between writers who charge by word versus those who are paid based on qualified leads that convert.

"If there was an agent that's like, 'We'll just take all your phone calls and turn them into blog posts, and we only get charged a commission of course sales,' I would probably be really happy with that."

**_Key Takeaway:_** AI may drive a shift from software companies selling tools to companies that own entire value chains and are compensated based on business outcomes. This will require building systems that connect previously separate data streams to create end-to-end accountability.

!!! success "Key Takeaway"
AI may drive a shift from software companies selling tools to companies that own entire value chains and are compensated based on business outcomes. This will require building systems that connect previously separate data streams to create end-to-end accountability.

---

## What's the most valuable data for future AI development?

The most valuable data for AI development has evolved over time:

"When I started, it was physics. And then it's like, 'Well, we're running out of sensors, but the next sensor is going to cost us 10 billion dollars.' So I went to Facebook - what's every post and comment and Facebook group and the social graph?"

Now, I believe the most valuable data will be how humans interact with AI:

"How humans use AI will be the most interesting dataset. And then in 10 years, it'll be how AI talks to AI. Most of the data produced will just be AI talking to AI."

This is why I'm particularly interested in working with companies that have large proprietary datasets in specialized domains:

"Someone was like, 'Oh, we have the last 40 years of investment decisions.' I was like, 'What?' Now I'm willing to pay so much to process this. Let's actually think about what the schemas look like and how to design this system."

These unique datasets offer opportunities to create specialized tools that can extract insights that general models can't access without the proper context and structure.

**_Key Takeaway:_** The most valuable data is shifting from general internet content to human-AI interactions and eventually AI-to-AI interactions. Companies with large proprietary datasets in specialized domains are particularly well-positioned to create value with AI systems tailored to their unique information.

---

FAQs

!!! success "Key Takeaway"
The most valuable data is shifting from general internet content to human-AI interactions and eventually AI-to-AI interactions. Companies with large proprietary datasets in specialized domains are particularly well-positioned to create value with AI systems tailored to their unique information.

---

## What tools are recommended for tracing and evaluations in AI applications?

While Langsmith is commonly used, some users experience technical issues with data exports. Alternative options include Brain Trust for evaluations and Log Fire for tracing. The choice often depends on your specific needs and existing partnerships. For simpler implementations, consider storing question-answer pairs directly in a database rather than relying on third-party tracing software, which gives you more control and easier access to your data.

---

## How should I approach data collection for evaluating my AI application?

Start by creating an evaluation dataset from real user interactions. This can be done by exporting traces from tools like Langsmith or by directly storing question-answer pairs in your database. Once you have real data, you can generate synthetic questions to expand your test set. Focus on collecting both the user queries and your system's responses, along with any relevant context like retrieved document chunks, to enable comprehensive evaluation.

---

## Which language models are best for RAG (Retrieval-Augmented Generation) applications?

The choice depends on your specific requirements. GPT-4 is commonly used for standard implementations, while GPT-3.5 may be sufficient for applications where speed is critical. Gemini is popular for RAG applications due to its large context window, allowing you to include more retrieved content without worrying about token limits. For high-stakes applications where accuracy is paramount, GPT-3.5 is sometimes preferred despite being older, as it can be more reliable for certain use cases.

---

## How should I approach improving my AI application's performance?

Focus on systematic evaluation before making changes. Create a representative dataset of real user queries, then establish metrics that align with your business goals. Prioritize experiments based on potential impact and resource constraints—you can only run a limited number of experiments in a given timeframe. Remember that improving AI performance is an iterative process requiring continuous testing and refinement rather than a one-time fix.

---

## What are effective ways to manage expectations when implementing AI solutions?

Be transparent about both capabilities and limitations. Help stakeholders understand that AI implementation is an iterative process requiring ongoing refinement rather than a one-time deployment. Clearly define the role of AI as a tool to assist humans rather than replace them completely. For specialized fields like architecture or engineering, emphasize that professionals still need to make the final decisions, with AI serving as a support system that provides suggestions and identifies potential issues.

---

## How can I integrate visuals and diagrams into AI-generated reports?

This is an emerging area with promising developments. Consider implementing systems that can intelligently select and incorporate relevant images from your existing resources. For technical applications like construction or engineering, the ability to include screenshots of blueprints with annotations highlighting specific areas of concern can significantly enhance the value of AI-generated reports. Libraries like Mermaid for diagram generation are becoming more widely supported and can be integrated into AI workflows.

---

## How should AI applications be priced to capture appropriate value?

Consider moving beyond usage-based pricing (like per-token or per-user) toward outcome-based models that align with the actual business value delivered. For example, charging per resolved customer support ticket rather than per API call creates better alignment between your pricing and the value customers receive. This shift requires building systems with sufficient accountability and measurement capabilities to track outcomes reliably. The most innovative pricing approaches treat AI capabilities as replacements for headcount rather than as traditional software tools.

---

## What's the relationship between data collection and future AI capabilities?

Every AI application serves as a sensor that generates valuable data. The applications built today create the datasets that will enable more advanced AI capabilities tomorrow. Proprietary datasets from specialized industries (like investment decisions, supply chain operations, or construction projects) are particularly valuable for building domain-specific AI capabilities. The most interesting future developments will likely come from analyzing how humans interact with AI systems, creating a feedback loop of continuous improvement.

---

## How should I approach dynamic data visualization in AI-generated reports?

When creating AI-generated reports with dynamic visualizations, there are several approaches to consider depending on your specific needs.

For deep research-style reports (like those from Gemini, Claude, or OpenAI), the LLM typically decides on a set of subtasks and executes them sequentially. These reports often don't include charts or visualizations by default, though OpenAI's deep research does incorporate images.

For more structured reports with visualizations, I see three main approaches:

1. Post-hoc image addition: You can have the LLM identify places where supplementary images would enhance the text, then add them afterward.
1. Image citations during research: Treat images as another citation source that the LLM can reference while generating text. For example, with a client yesterday, the LLM decided to include an org chart in a leadership report because it had access to an org chart JPEG file during generation.
1. Mermaid diagrams: These are particularly useful for creating dynamic visualizations directly in Markdown. The key challenge is validation - if Claude generates an incorrect Mermaid diagram, it simply fails to render. You need a validation loop or external server to check the diagram code, report errors, and iterate to fix them.

For standard data visualizations, most companies use JavaScript libraries like Recharts, which allow you to pass data as props and generate visualizations.

The approach depends on whether your report format is flexible or fixed. If fixed, each header might have its own RAG workflow - for example, every competitor analysis might need a leadership team section, which triggers a subtask to find the leadership team of the target company.

---

## How can we handle styling challenges in professional reports?

One of the biggest challenges in AI report generation is matching the exact styling expectations of professional reports. I work with companies that sell to consultants like McKinsey, and the hardest part isn't generating the content - it's making the slides and plots look exactly like McKinsey-branded material.

While it's easy to plug in matplotlib or Recharts, it's extremely difficult to match the precise styling requirements of professional consulting firms. Some clients are literally saying, "We're not going to pay you any of that $80,000 unless you can make it look like we actually made this."

These firms often use specialized software from the early 2000s for plot generation, with very specific requirements about legend shapes, marker styles (X's versus T's), and other formatting details. The styling is so challenging that we're considering using computer vision to train systems to use PowerPoint and implement styling changes based on feedback comments.

I believe there's a significant market opportunity here - you could easily sell software that generates McKinsey-style plots for $100,000 to an analyst team. The last 5% of styling is what makes the difference between something that looks AI-generated versus professionally produced.

**_Key Takeaway:_** The styling challenge represents a major opportunity for AI tools that can match the exact visual requirements of professional consulting firms. The technical content generation is often easier than matching the precise styling expectations that make reports look professionally produced.

!!! success "Key Takeaway"
The styling challenge represents a major opportunity for AI tools that can match the exact visual requirements of professional consulting firms. The technical content generation is often easier than matching the precise styling expectations that make reports look professionally produced.

---

## How should I approach analyzing unstructured customer feedback data?

For a project like Netflix's customer feedback analysis, where you're collecting unstructured data through a "report a problem" feature, I recommend a hybrid approach combining semantic search with structured analysis.

First, consider doing hierarchical clustering to build a taxonomy of error categories. This gives you a structured way to analyze the data beyond just semantic search. By tagging all feedback with these hierarchical categories, you can provide accurate counts and faceted navigation.

When a user asks "What are members saying about Seinfeld's aspect ratio?", you might return 10-20 semantically relevant results, but also show facets like "200 comments in this category, 80 in that category" to help them understand the distribution of issues.

This approach allows users to traverse the data in interesting ways - they might start with audio issues, discover that 20% of complaints are about Seinfeld, then dig into which season has the most problems. The goal is giving users a portfolio of tools to explore the hierarchy rather than just semantic search alone.

For quantitative questions like "How many audio sync issues were reported in Brazil last month?", you need structured data. The LLM will hallucinate counts if you rely solely on semantic search. By building lightweight classifiers for common issues, you can provide accurate counts while still allowing semantic exploration of the unstructured text.

I worked with a company called Interpret that built something similar - a chatbot that could talk to customer feedback and give realistic counts by combining semantic understanding with structured analysis.

**_Key Takeaway:_** The most effective approach combines semantic search with structured analysis through hierarchical clustering and classification. This gives users both the flexibility to explore feedback semantically and the accuracy of structured data for quantitative questions.

!!! success "Key Takeaway"
The most effective approach combines semantic search with structured analysis through hierarchical clustering and classification. This gives users both the flexibility to explore feedback semantically and the accuracy of structured data for quantitative questions.

---

## What's the best way to build fast classifiers for unstructured data?

When you need to quickly classify unstructured data, there are several approaches depending on your requirements.

One approach is using embedding-based classification. As Jan mentioned, OpenAI's documentation describes a simple technique where you embed category descriptions and then classify items by finding the closest category embedding. This works well for straightforward classification tasks and is extremely fast to implement.

In my previous work, we used a matrix-based approach where we'd embed all products in a matrix, then learn another matrix to multiply by the product embeddings whenever we needed to build a classifier. This allowed us to label about 1,000 examples, learn the weights, and then multiply the entire product space by that vector to get predictions for every product. It was very fast but typically achieved around 85% accuracy.

For Netflix's feedback analysis, you might want to combine pre-defined categories from domain experts with data-driven clusters discovered through analysis. There will be common issues like rendering problems or audio sync issues that domain experts can define, plus a longer tail of soft clusters that emerge from the data.

The key is building a system that can quickly create and apply these classifiers as new issues emerge. When a new feature launches, you want to detect feedback about it immediately, even if it wasn't in your training data.

**_Key Takeaway:_** Fast classifier development is essential for responsive feedback analysis. Combining embedding-based approaches with domain expertise allows you to quickly identify both known issues and emerging patterns in user feedback.

!!! success "Key Takeaway"
Fast classifier development is essential for responsive feedback analysis. Combining embedding-based approaches with domain expertise allows you to quickly identify both known issues and emerging patterns in user feedback.

---

## How should we think about tool-based approaches versus semantic search?

I believe we're moving toward a world where many RAG applications will use tool-based approaches rather than pure semantic search, especially for structured data.

In the coming weeks, we'll have talks from teams building coding agents that use a portfolio of tools rather than semantic search. Their thesis is that for structured data, the right way to prepare context isn't one semantic search request, but an agent using multiple tools to build context incrementally.

Think about how you debug an error message - you see the error came from a specific file, so you load that file, then you find the function causing the issue, load that file, and traverse the file tree building context before solving the problem. Coding agents are implementing this approach rather than embedding all code.

You can implement this with simple tools like "ls" (list files), "read_file", and "grep". The agent uses these tools to navigate the data, building context as it goes. This approach might cost more at query time but requires less preprocessing of data.

I'm curious if this approach would work for traversing complex documents like 1,000-page PDFs. Instead of embedding everything, you could provide tools like "list_table_of_contents", "grep", "show_page", and "show_page_as_image". The agent could navigate the document naturally, finding references and following them just as a human would.

**_Key Takeaway:_** Semantic search is most valuable when the producer and consumer of data don't share vocabulary. For structured data or documents with clear organization, a tool-based approach that mimics human navigation may be more effective and require less preprocessing.

!!! success "Key Takeaway"
Semantic search is most valuable when the producer and consumer of data don't share vocabulary. For structured data or documents with clear organization, a tool-based approach that mimics human navigation may be more effective and require less preprocessing.

---

## What are you working on with your Cura project?

We're making progress on building out Cura, which is an open-source project (not quite a product yet) focused on analyzing conversation data. In the next few days, we'll be benchmarking it on about a thousand conversations to see what patterns we discover.

The core of the project involves hierarchical clustering, explaining clusters, and generating names for these clusters. We're planning to download every open-source chat conversation dataset and run our analysis on it to see what we find.

My philosophy with any product I build is that it should function as a sensor that generates data. I want to "trick" users into labeling data for me. If I don't know which chart type works best, I'll generate three options and ask users to delete the ones they don't want. My messaging is that it's important for them to review the data, but I'm actually collecting valuable feedback on what visualizations work best.

We apply the same approach to citations in paragraphs - users can mouse over citations to see the source data and delete or regenerate citations they don't trust. This creates a feedback loop that continuously improves the system.

**_Key Takeaway:_** Building products that function as data collection sensors is a powerful approach. By giving users options and tracking their choices, you can gather valuable feedback that improves your system while providing a better user experience.

!!! success "Key Takeaway"
Building products that function as data collection sensors is a powerful approach. By giving users options and tracking their choices, you can gather valuable feedback that improves your system while providing a better user experience.

---

## What upcoming content are you excited about in the course?

I'm particularly excited about the second half of the course where we'll dive deeper into data analysis and explore the portfolio of tools approach.

In the coming weeks, we'll have talks from Reducto, one of the best PDF parsing libraries available right now. They have contracts with companies like Vanta and government agencies and have achieved impressive results.

We'll also be inviting teams building coding agents, including the Augment team and the Klein team. These companies are focusing less on RAG with semantic search and more on RAG using a portfolio of tools. Their thesis is that for structured data like code, the right approach isn't one semantic search request but an agent using multiple tools to build context.

Beyond the course, I'm organizing a speaker series with guests from OpenAI's memory team and possibly Claude Code. My goal is to bring in the most interesting speakers in the field to share their insights.

**_Key Takeaway:_** The future of RAG systems, especially for structured data like code, may involve less semantic search and more tool-based approaches where agents navigate information using a portfolio of tools to build context incrementally.

---

IF you want to get discounts and 6 day email source on the topic make sure to subscribe to

<script async data-uid="010fd9b52b" src="https://fivesixseven.kit.com/010fd9b52b/index.js"></script>

!!! success "Key Takeaway"
The future of RAG systems, especially for structured data like code, may involve less semantic search and more tool-based approaches where agents navigate information using a portfolio of tools to build context incrementally.

---

## How effective is fine-tuning for improving citation accuracy?

When working with citation requirements, fine-tuning can dramatically reduce error rates. In one project, we used OpenAI's fine-tuning API with about 1,000 examples to improve our marketing content generation system.

The results were impressive - our error rates dropped from around 4% to essentially 0% on our test set of 200 examples. We didn't need complex frameworks like Fluoro since we weren't hosting local models, just using OpenAI's API directly.

The key was having evaluators validate our offline data, filtering out incorrectly formatted examples before using them in the fine-tuning process. This approach worked particularly well because we weren't trying to change the model's knowledge - just its formatting behavior.

When determining how much data you need, I recommend experimenting with different sample sizes:

"What I would often do is try to use a subset of my data for fine-tuning, then increase the sample size and figure out what that curve looks like. It's going to be performance versus volume."

Different models will have different learning curves - a 1.3 billion parameter model might flatten out at 10,000 data points, while larger models might show different patterns. Adjusting learning rates can also affect these curves.

**_Key Takeaway:_** Fine-tuning can be remarkably effective for formatting tasks like citation, often requiring less data than you might expect. Start with small batches, measure performance, and increase data volume until you reach your desired accuracy level.

!!! success "Key Takeaway"
Fine-tuning can be remarkably effective for formatting tasks like citation, often requiring less data than you might expect. Start with small batches, measure performance, and increase data volume until you reach your desired accuracy level.

---

## Should we shuffle citation sources during fine-tuning?

When fine-tuning models to cite sources correctly, shuffling the order of retrieved sources can be beneficial to prevent position bias. This approach makes the model invariant to the order of sources, which is particularly important if you're not sorting by relevance.

However, if you are sorting by relevance, maintaining the original order might actually be preferable: "Maybe it is important for the model to know that the first text chunk is the most relevant text chunk."

The need for shuffling may also depend on the context length of your model. With older, smaller context models (like 4K token models), position bias was more pronounced due to the "lost in the middle" effect. Newer models with better attention mechanisms have improved recall across their context window.

"If you look at the newer models, they just have way better lost-in-the-middle sensitivity in general, and I would expect that when you fine-tune these things, they also preserve some of that ability to attend over long contexts."

The real challenge that remains is reasoning over multiple "needles" of information scattered throughout a document - connecting facts from different sections remains difficult for most models.

**_Key Takeaway:_** Consider shuffling citation sources during fine-tuning if you want position-invariant citations, but if you're sorting by relevance, maintaining order may be beneficial. Newer models have better attention across their context window, reducing the need for this technique.

!!! success "Key Takeaway"
Consider shuffling citation sources during fine-tuning if you want position-invariant citations, but if you're sorting by relevance, maintaining order may be beneficial. Newer models have better attention across their context window, reducing the need for this technique.

---

## How should we approach tool design for specialized retrieval tasks?

When designing tools for retrieval systems, focus on creating a portfolio of specialized tools rather than just distinguishing between semantic and structured data. The key question isn't "Am I searching semantic or structured data?" but rather "What is the portfolio of tools I want to expose to my system?"

For example, in a construction use case, we implemented several specialized tools:

- Generic document search that searches everything
- Contact search for finding people
- RFI (Request for Information) search that takes specific RFI codes
- Contract search that returns not just text chunks but also responsible parties

The implementation details (whether it's semantic search or structured data) matter less than how you present these tools to the language model. Your focus should be on making sure the model understands what tool to use and when.

For evaluating tool selection, I recommend having the model "write a plan of all the tools it might want to use" for a given query, then evaluating that plan first. You can even present this plan to users for approval before execution, which creates valuable training data based on acceptance rates.

"That gets you a pretty good dataset in terms of customer plan acceptance rates, and then you can look at the ones that are not accepted and figure out what you need to do afterwards."

The naming of tools significantly impacts how models use them. In coding agents, for example, providing a specific "grep" tool versus just mentioning grep in the command line instructions can change execution patterns by 2% in evaluations.

**_Key Takeaway:_** Design a portfolio of specialized tools based on specific use cases rather than general data types. Focus on clear tool descriptions and evaluate how well the model selects the appropriate tools for different queries.

!!! success "Key Takeaway"
Design a portfolio of specialized tools based on specific use cases rather than general data types. Focus on clear tool descriptions and evaluate how well the model selects the appropriate tools for different queries.

---

## How can we handle temporal reasoning in medical data?

One of the most challenging aspects of working with medical data is reasoning about information across a timeline. When retrieving documents about medications, for example, you might get 20 documents all describing medications, but understanding what changed over time requires special handling.

"You might want to know what changed over time, or you have to always see it in the context of time. And you also need to find relationships like 'there's this medication and the patient became worse' or 'this medication went up' - that all needs to be conceived in the system."

For presenting temporal data effectively to models, I recommend structuring it as a markdown table whenever possible. In our testing, markdown tables performed 12% better than CSV, JSON, or YAML formats for complex lookup tasks across large datasets.

"We've done tests where I put like 6,000 rows, 50 columns as CSV, as markdown, as JSON, as YAML - and markdown tables is like 12% better in terms of identifying on row X where the value is Y, find me the row that's one above and one to the left."

The ordering of temporal data also matters significantly. You might get different results if you order events in ascending versus descending time. This affects how the model scans and reasons about cause and effect relationships.

For building better temporal reasoning capabilities, consider:

1. Ordering retrieved documents chronologically

2. Presenting data in markdown table format with clear timestamps

3. Having the model first extract and reorganize relevant information before reasoning about it

4. Mining reasoning chains from expert users to create training data

**_Key Takeaway:_** For temporal reasoning, structure data chronologically in markdown tables and implement a two-stage approach where the model first extracts and organizes relevant timeline information before reasoning about it.

!!! success "Key Takeaway"
For temporal reasoning, structure data chronologically in markdown tables and implement a two-stage approach where the model first extracts and organizes relevant timeline information before reasoning about it.

---

## What's the difference between multi-agent and single-agent approaches?

The debate between multi-agent and single-agent systems often comes down to context coordination challenges. For coding tasks, Devin (from Cognition) chose a single-threaded approach because coordinating between agents modifying different parts of a codebase is extremely difficult.

"If one agent modifies one directory and another agent modifies another directory, that communication channel is sort of not well defined yet."

In contrast, Claude's Deep Research uses multiple agents, but they're all read-only - they don't need to coordinate changes because they're just retrieving information that will later be combined:

"In that multi-agent system, the agents are all read-only, so they don't need to manage that communication overhead because they're all going to be reduced. If I search about who I am, one agent searches childhood, one agent searches career, and once they bring all the information back, they can be reduced."

The primary benefit of multi-agent systems appears to be token efficiency - you can use more tokens across multiple agents than with a single agent. "The performance just increases with the amount of tokens each sub-agent is able to consume. If you have 10 sub-agents, you can use more tokens, and your research quality is better."

For medical data applications that are primarily read-only, a multi-agent approach might work, but the challenge remains in ensuring no context is missed when combining information from different agents.

**_Key Takeaway:_** Choose multi-agent approaches for read-only tasks where you need to process more tokens than a single context window allows. For tasks requiring coordination of changes, single-agent approaches remain more practical until better coordination mechanisms are developed.

!!! success "Key Takeaway"
Choose multi-agent approaches for read-only tasks where you need to process more tokens than a single context window allows. For tasks requiring coordination of changes, single-agent approaches remain more practical until better coordination mechanisms are developed.

---

## How can we use document summarization to improve retrieval?

Generating summaries during document ingestion can be a cost-effective approach to improving retrieval. Summaries function as a form of compression and can be particularly valuable when working with smaller context window models.

"In general, this is a good idea because that's almost in some ways just a more cost-effective way of doing this contextual retrieval stuff. Summary is just compression."

The key is designing your summarization prompt based on the specific tasks your system needs to perform. For example, with architectural blueprints, we knew users would ask about room counts and dimensions, so we created summaries that explicitly counted and listed these elements:

"Because we know that our tasks involve things like extracting the names of rooms and counting things, if our language model can have a summary that counts everything, then it becomes much easier to think about 'the place with 4 bedrooms and 2 bathrooms.'"

We implemented this as a separate document search tool that only hits the summaries. Through iteration and evaluation, we improved our summary generation from 16% recall to 85% recall in just a few days.

For implementation, you can:

1. Create a separate "search summaries" tool

2. Design summary prompts that extract the specific types of information users will query

3. Evaluate and iterate on summary quality using test queries

4. Use summaries as synthetic text chunks that supplement your existing text chunks

This approach works particularly well for documents like financial reports, where structured information can be extracted, or for multimedia content where describing images or videos in text makes them searchable.

**_Key Takeaway:_** Document summarization during ingestion creates valuable synthetic text chunks that can dramatically improve retrieval performance. Design summary prompts based on the specific information needs of your application and iterate based on evaluation results.

!!! success "Key Takeaway"
Document summarization during ingestion creates valuable synthetic text chunks that can dramatically improve retrieval performance. Design summary prompts based on the specific information needs of your application and iterate based on evaluation results.

---

## How can we implement price quote generation using RAG?

One practical application we've built is an automated price quote system for sales teams. After multiple calls with a prospect, the system generates personalized pricing options and potential upsells.

The process works like this:

1. We have 16 pages of pricing information (per-seat pricing, volume discounts, prepayment options)

2. We have transcripts from 6 phone calls with the prospect

3. We ask the language model to:

- Read the transcripts and list all relevant variables
- Extract the values of those variables
- Reason about the pricing document
- Propose options and upsells
- Write an email to the prospect

"The email's like 'Great talking to you, Tim. It sounds like for a company your size, you can probably commit to 15 seats. This will get you a 20% discount. If you don't use it, we'll move it to next year, and if you pay upfront, we can give you another 20-25% discount because I know that's something your CTO really values.'"

Our evaluation method is simple but effective - we have salespeople review the generated emails before sending them, and we track whether they make edits. When edits are needed, we analyze what went wrong in the reasoning step.

This approach of extracting variables, reasoning about them, and then generating output could be applied to medical data as well. For example, if a patient shows drowsiness, the system could first extract all timeline information about drowsiness, then reason about potential causes.

**_Key Takeaway:_** For complex reasoning tasks, implement a multi-step process where the model first extracts and organizes relevant information, then reasons about it, and finally generates output. This structured approach makes the reasoning more transparent and easier to evaluate.

!!! success "Key Takeaway"
For complex reasoning tasks, implement a multi-step process where the model first extracts and organizes relevant information, then reasons about it, and finally generates output. This structured approach makes the reasoning more transparent and easier to evaluate.

---

## What's the best way to format data for language models?

When presenting structured data to language models, markdown tables consistently outperform other formats like CSV, JSON, or YAML. In our testing, markdown tables were 12% more effective for complex lookup tasks.

"We've done tests where I put like 6,000 rows, 50 columns as CSV, as markdown, as JSON, as YAML - and markdown tables is like 12% better in terms of identifying on row X where the value is Y, find me the row that's one above and one to the left."

The formatting details matter significantly. For example, having spaces between tokens in markdown tables (like "| data |" instead of "|data|") affects how the model processes the information.

"If I search for the word Jason, the token is 'space Jason'. But if it's Jason in JSON, it's actually 'quote Jason' - those are different tokens. And so those things end up affecting the lookup a little bit."

These seemingly minor formatting choices can have meaningful impacts on model performance, especially for tasks requiring precise information retrieval or table navigation.

For temporal data specifically, presenting information in chronological order (either ascending or descending) can significantly affect how models reason about cause and effect. Testing both approaches is worthwhile, as one may work better than the other depending on your specific use case.

Markdown tables consistently outperform other data formats for structured information. Pay attention to spacing and formatting details, as they affect tokenization and retrieval performance. For temporal data, experiment with both chronological and reverse-chronological ordering.

---

## How should we approach end-to-end evaluation of complex RAG systems?

End-to-end evaluation of complex retrieval systems remains challenging, especially when there isn't a single correct answer or when the system needs to perform multi-step reasoning.

"The end-to-end evaluation of these kinds of things are still pretty challenging, unless it really is the case that there are just certain text chunks that we're trying to achieve or certain answers we already know ahead of time."

For tool selection, one effective approach is evaluating the system's planning capabilities:

1. Ask the model to write a plan of which tools it would use for a query

2. Evaluate the plan before executing it

3. Allow users to approve or reject the plan

4. Track plan acceptance rates and analyze rejected plans

For reasoning tasks, breaking evaluation into steps can be helpful:

1. Evaluate information extraction (did the system find the relevant information?)

2. Evaluate reasoning (given the correct information, did it reach valid conclusions?)

3. Evaluate output generation (was the final response clear and actionable?)

In some domains like coding, the evaluation metrics are clearer - does the code pass tests? In other domains like medical reasoning, evaluation may require expert review or comparison to known outcomes.

For systems like our price quote generator, we use a practical metric - do salespeople edit the generated emails before sending them? This real-world usage metric helps us identify where the system's reasoning falls short.

**_Key Takeaway:_** Break evaluation into component parts rather than relying solely on end-to-end metrics. Incorporate user feedback into your evaluation process, and track how often outputs require human editing or intervention.

!!! success "Key Takeaway"
Break evaluation into component parts rather than relying solely on end-to-end metrics. Incorporate user feedback into your evaluation process, and track how often outputs require human editing or intervention.

---

## How does fine-tuning improve citation accuracy in LLMs?

Fine-tuning can dramatically reduce error rates when teaching models to properly cite sources. In one example, fine-tuning reduced citation errors from 4% to nearly 0% for marketing content generation. The process involves collecting properly formatted examples, validating them, filtering out incorrect formats, and using them in the fine-tuning process.

---

## How many examples are typically needed for effective fine-tuning?

Around 1,000 high-quality examples can be sufficient for format-related fine-tuning tasks. However, the exact number depends on your specific use case. It's recommended to experiment with increasing sample sizes to determine the optimal amount for your needs. Start with a smaller subset and gradually increase to identify where performance improvements begin to plateau.

---

## Should I shuffle the order of retrieved sources in my fine-tuning dataset?

Shuffling retrieved sources can be beneficial to make your model invariant to the order of information. This approach helps prevent the model from developing biases toward information presented first. However, if your retrieval system sorts by relevance, maintaining that order might be important as the first chunk would genuinely contain the most relevant information.

---

## How should I approach tool selection for my LLM application?

Focus on developing a portfolio of specialized tools rather than simply categorizing between semantic and structured data searches. Consider what specific capabilities would benefit your use case, such as date-range filtering, categorical filters, or metadata tag filtering. The implementation details (whether semantic or structured) matter less than ensuring your model understands when to use each tool.

---

## What's an effective way to evaluate tool selection by the model?

A practical approach is to have the model write a plan listing all tools it would use for a given query, then evaluate that plan before execution. You can present this plan to users for approval or rejection, which generates valuable feedback data. Analyzing rejected plans helps identify improvements needed in your tool selection and routing logic.

---

## How do coding agents approach tool integration?

Coding agents have made significant progress with tool integration. One key insight is that providing named tools for specific functions (rather than general capabilities) significantly changes how frequently these functions are used. For example, providing a dedicated "grep" tool versus expecting the model to remember to use grep through a general command line interface can improve performance by several percentage points.

---

## How should I organize timeline-based data for LLM processing?

For timeline data, consider presenting information in a markdown table format, which models tend to process effectively. Order the data chronologically (either ascending or descending) and include clear date markers. This organization helps the model understand temporal relationships and reason about cause and effect. Testing both ascending and descending time orders may yield different results depending on your use case.

---

## Why are markdown tables particularly effective for structured data?

Markdown tables have shown superior performance (approximately 12% better) compared to other formats like CSV, JSON, or YAML when models need to perform lookup tasks or understand relationships between data points. The spacing between tokens in markdown tables appears to be particularly well-suited to how models process information.

---

## How can I help models reason across complex information?

For complex reasoning tasks, consider implementing a two-step approach: first have the model extract and reorganize all relevant information from different sources, then reason about this reorganized information. This approach works well for tasks requiring synthesis across multiple data points, such as analyzing medical timelines or generating pricing quotes based on multiple conversations.

---

## Is it beneficial to generate summaries during data ingestion?

Creating summaries during data ingestion can be very effective, especially for longer documents. Summaries act as compressed versions of your data that can be more efficiently processed. For specific use cases like blueprints or financial documents, you can design summarization prompts that extract the most relevant information (like room counts or key financial figures) to make subsequent queries more efficient.

---

## How can I handle reasoning across multiple documents?

For reasoning across multiple documents, consider having the model first extract all relevant information related to the query, reorganize it (possibly chronologically or thematically), and then reason about the reorganized information. This approach helps manage context limitations and focuses the model's attention on the most pertinent details.

---

## What's the best way to handle long context windows?

Newer models with improved attention mechanisms handle long contexts better than older models. However, for complex reasoning tasks involving multiple "needles" of information spread throughout a document, consider using tools that first organize the relevant information before reasoning about it. This approach remains effective even with models that have long context windows.

---

IF you want to get discounts and 6 day email source on the topic make sure to subscribe to

<script async data-uid="010fd9b52b" src="https://fivesixseven.kit.com/010fd9b52b/index.js"></script>

---

## How should I approach dynamically generating and handling metadata for documents?

When dealing with the need to extract new metadata from existing documents, the architectural approach depends largely on your current infrastructure. Most companies I work with already have some existing setup, so we're rarely building from scratch.

In essence, this is just like any ETL (Extract, Transform, Load) job where a process creates a new database artifact. The key question is: what makes backfilling this data challenging in your specific context? Is it the cost of reprocessing millions of documents? Is it the unpredictability of expenses?

For cost estimation, I recommend calculating the token volume of your data. We had a task to summarize a million conversations, and we made sure to calculate the expected input and output tokens. This allowed us to make informed decisions about model selection - for instance, we discovered that using open source models was only 8 times cheaper than using OpenAI's API.

"I was really disappointed to realize that the open source models are only 8 times cheaper. We're putting all this effort to save $60. And that was for a million conversations - it cost $60 to summarize a million conversations. These models are just so cheap now."

For specialized extraction tasks, consider using smaller, purpose-built models. At Stitch Fix, we built a suite of small models doing specific extractions. For example, we realized we were selling belts with pants that had no belt loops, so we created a simple computer vision model to detect belt loops. This approach was efficient and solved a specific business problem worth millions of dollars.

**_Key Takeaway:_** Calculate token volumes and costs before deciding on your extraction approach. Sometimes the cost difference between APIs and self-hosted models is smaller than expected, making the engineering effort to switch questionable. For specialized extractions, consider purpose-built models that solve specific business problems rather than trying to do everything with one large model.

!!! success "Key Takeaway"
Calculate token volumes and costs before deciding on your extraction approach. Sometimes the cost difference between APIs and self-hosted models is smaller than expected, making the engineering effort to switch questionable. For specialized extractions, consider purpose-built models that solve specific business problems rather than trying to do everything with one large model.

---

## What are the challenges with extracting multiple attributes in a single API call?

When extracting multiple attributes from documents, be aware that prompts for some attributes can affect the extraction of other attributes. We found this when processing transcripts - when we asked for shorter action items, the summaries would also get shorter.

To address this, we split our extraction into separate jobs: one for action items and another for summary and memo generation. This separation gave us better control over each component. We made this approach cost-effective by leveraging prompt caching - the transcript only needed to be processed once, with multiple outputs generated from that single input.

**_Key Takeaway:_** Be cautious about extracting too many attributes in a single API call, as they can influence each other in unexpected ways. Consider splitting extractions into separate jobs with specific focuses, and use techniques like prompt caching to maintain cost efficiency.

!!! success "Key Takeaway"
Be cautious about extracting too many attributes in a single API call, as they can influence each other in unexpected ways. Consider splitting extractions into separate jobs with specific focuses, and use techniques like prompt caching to maintain cost efficiency.

---

## How should I approach recommendation systems with LLMs?

For recommendation systems like predicting product purchases, I wouldn't use an LLM directly in the recommendation system. Companies like Stitch Fix and YouTube use LLMs primarily to create better embeddings, not for the core recommendation logic.

The approach I'd recommend is building item embeddings using historical data, where the inputs might include product images, descriptions, user comments, and checkout rates. Similarly, user embeddings would incorporate their feedback, fit comments, and other behavioral signals.

One valuable application of LLMs is creating synthetic users to run simulations, particularly for addressing cold-start problems. When a new item appears, there's no transaction or impression data to train on. An LLM can simulate transaction data and returns, helping predict success rates for the first orders.

"At Stitch Fix we needed about 400 shipments of a single SKU before we had a good embedding for it. So our only job was: how do we get to a world where we either can simulate the SKUs or need less data?"

We addressed this by building a "Tinder for clothes" where users could swipe left or right on clothing items. This generated 6,000 labels much faster than waiting for 400 actual shipments, as users would label 30 items a day versus receiving only 5 items a month.

**_Key Takeaway:_** Rather than using LLMs directly for recommendations, use them to generate better embeddings and synthetic data to address cold-start problems. Consider creative ways to gather user preferences at scale, as the velocity of data collection is often the limiting factor in recommendation quality.

!!! success "Key Takeaway"
Rather than using LLMs directly for recommendations, use them to generate better embeddings and synthetic data to address cold-start problems. Consider creative ways to gather user preferences at scale, as the velocity of data collection is often the limiting factor in recommendation quality.

---

## How can I blend traditional ML with unstructured data from LLMs?

The most promising approach I've seen is using LLMs for synthetic data generation and feature engineering. The challenge with many recommendation systems is the low velocity of data - unlike Spotify or Netflix where users consume content quickly, physical product recommendations might take weeks to validate through purchases and returns.

Our focus at Stitch Fix was making each sample more efficient. Instead of building general-purpose computer vision models, we created specialized models for specific attributes (like detecting belt loops). These targeted models were more data-efficient and could directly drive business decisions (like upselling belts with pants that have belt loops).

The workflow we found effective was:

1. Use smaller, data-efficient models for specific extractions
2. Use these models to generate simulations and synthetic data
3. Feed this expanded dataset into larger, more powerful models

"Can we use LLMs for feature engineering and then use traditional models because they're gonna absorb the data faster? And then, once those cap out, how can we use the traditional models to create more data for the larger models to take in more capacity?"

This approach recognizes that different models have different data efficiency profiles, and leveraging their strengths in combination yields better results than trying to solve everything with a single approach.

**_Key Takeaway:_** Blend traditional ML with LLMs by using LLMs for feature engineering and synthetic data generation. Build specialized, data-efficient models for specific attributes, then use these to feed larger models. This creates a virtuous cycle where each type of model enhances the capabilities of the others.

!!! success "Key Takeaway"
Blend traditional ML with LLMs by using LLMs for feature engineering and synthetic data generation. Build specialized, data-efficient models for specific attributes, then use these to feed larger models. This creates a virtuous cycle where each type of model enhances the capabilities of the others.

---

## Are there good tools for data engineering in the LLM ecosystem?

The data engineering landscape for LLMs is still developing, with most early-stage companies using relatively simple approaches like "data to JSON" pipelines. One company worth looking at is Tensor Lake, which provides sophisticated data processing for tensors.

A critical area that's often overlooked is managing evaluation datasets. Many companies have inconsistent approaches where individual team members export data in ad-hoc ways:

"Almost every company I work with has datasets for evals, but they're all kind of like one guy wrote a SQL query to export things, saved it as a CSV file on their laptop and started working with it. And then they wrote this to Brain Trust, and that's what they're working on. But the other guy on a different team is using a different dataset."

This creates problems when metrics improve - does anyone trust the results? Was the test data recent or old? Did it cover multiple organizations or just one customer? Proper data engineering for evaluation is a substantial undertaking that requires careful planning and coordination across teams.

At Facebook, defining a new table for newsfeed views would involve a data engineer interviewing 20 teams, designing columns to support various query patterns, and ensuring everyone could write consistent SQL queries against the database. This level of rigor is often missing in LLM evaluation setups.

**_Key Takeaway:_** The data engineering ecosystem for LLMs is still maturing. Pay special attention to how you organize evaluation datasets, as inconsistent approaches lead to unreliable metrics. Consider investing in proper data engineering for your evaluation pipeline, similar to how established companies handle critical data infrastructure.

!!! success "Key Takeaway"
The data engineering ecosystem for LLMs is still maturing. Pay special attention to how you organize evaluation datasets, as inconsistent approaches lead to unreliable metrics. Consider investing in proper data engineering for your evaluation pipeline, similar to how established companies handle critical data infrastructure.

---

## What's your approach to topic modeling and specialized indices?

For topic modeling and specialized indices, we've been developing tools like Kora, which helps with topic extraction from documents. This approach is becoming increasingly valuable as managing knowledge bases becomes more complex.

The fundamental issue is that embeddings alone aren't sufficient for many complex queries. If someone asks "Who is the best basketball player under 25 years old from Europe?", embeddings might not find a direct answer unless that exact information exists in a paragraph somewhere.

This is why we need to build a portfolio of tools rather than relying solely on embeddings. For the basketball player example, you might need:

1. A structured player database with extracted attributes
2. Specialized extractors that pull out statements about people
3. Tools that can perform semantic search combined with structured filtering

"It's not that the tools are one-to-one with the retriever. It's actually gonna be the case that we probably have multiple tools hitting the same index."

This is similar to how command-line tools interact with a file system - you have commands like "list directories" and "view files," but also more specialized commands like "list files sorted by last modified" or "list files by editor." A smart model can learn to use these various tools rather than trying to build one mega-search tool that works for all cases.

**_Key Takeaway:_** Don't rely solely on embeddings for complex information retrieval. Build a portfolio of specialized tools that can work with your data in different ways. This approach is gaining traction in code generation and will likely become standard across other domains as well.

!!! success "Key Takeaway"
Don't rely solely on embeddings for complex information retrieval. Build a portfolio of specialized tools that can work with your data in different ways. This approach is gaining traction in code generation and will likely become standard across other domains as well.

---

## Will reasoning models eliminate the need for specialized indices?

Even with advanced reasoning models that can perform multi-step thinking, I don't believe they'll eliminate the need for specialized indices and tools. Instead, the focus should be on exposing a wide range of tools that these models can leverage.

The key insight is that tools aren't necessarily one-to-one with retrievers. You might have multiple tools hitting the same index, similar to how command-line tools interact with a file system. For example, you might have tools for listing directories, viewing files, sorting by modification date, or filtering by editor.

"A smart enough model might just be able to reason about how to use all five tools rather than trying to build a mega search tool that will work in all cases."

This is the direction that code generation tools are taking - they're finding that embedding your codebase isn't the right approach. Instead, they're building portfolios of tools, and I believe this pattern will spread to other domains as well.

**_Key Takeaway:_** Even with advanced reasoning capabilities, models benefit from having access to specialized tools rather than trying to do everything through a single approach. The future lies in building portfolios of tools that models can intelligently select and combine, not in creating a single universal solution.

!!! success "Key Takeaway"
Even with advanced reasoning capabilities, models benefit from having access to specialized tools rather than trying to do everything through a single approach. The future lies in building portfolios of tools that models can intelligently select and combine, not in creating a single universal solution.

---

## How do you approach cost calculations for AI processing?

When calculating costs for AI processing, focus on understanding your token volumes. For any extraction or processing task, calculate the expected input and output tokens to make informed decisions about model selection.

We had a surprising discovery when comparing OpenAI's API to open source models for summarizing a million conversations. The open source approach was only 8 times cheaper, saving just $60 total. While it was 26 times faster, the absolute cost was so low that it wasn't worth the engineering effort to switch.

"I was gonna write a blog post on how to use open source models to do the data extraction. I was like, 'Oh, it's not worth writing the blog post because 8 times cheaper for $60? Well, unless I'm doing this a hundred times, I don't need to save $50.'"

These calculations help you make rational decisions about where to invest your engineering time. Sometimes the cost difference between approaches is so small that it's not worth optimizing further, especially when the absolute costs are already low.

**_Key Takeaway:_** Calculate token volumes and costs before investing in optimization. Modern AI models are often surprisingly affordable at scale, making some optimizations unnecessary. Focus your engineering efforts where they'll have meaningful impact rather than chasing small percentage improvements.

!!! success "Key Takeaway"
Calculate token volumes and costs before investing in optimization. Modern AI models are often surprisingly affordable at scale, making some optimizations unnecessary. Focus your engineering efforts where they'll have meaningful impact rather than chasing small percentage improvements.

---

## How should I approach dynamically generating and handling metadata for documents?

When building metadata extraction systems that need to evolve over time, consider treating each extraction as a separate ETL (Extract, Transform, Load) job. This approach allows you to add new extraction tasks without redoing everything. Before implementing, calculate the token volume to estimate costs - you might find that even with millions of records, the cost is surprisingly manageable (often just tens of dollars). For specialized extractions, consider using smaller, focused models rather than trying to extract everything in a single pass, as this can provide better control over individual attributes.

---

## Is it worth using open source models for data extraction tasks?

It depends on your specific needs. In many cases, the cost difference between using open source models versus API models like GPT-4 may be smaller than expected - sometimes only 8x cheaper. For a job that costs $60 with an API model, saving $50 might not justify the engineering effort required to implement an open source solution. Always calculate the token volume and expected costs before making this decision, and consider factors beyond cost such as latency and maintenance requirements.

---

## How can I estimate the cost of running extraction jobs on large datasets?

Create a table that tracks input token counts for your documents and calculate the expected costs based on current API pricing. This simple exercise can provide valuable insights that inform your architecture decisions. For many extraction tasks, you might find that using models like GPT-4 Mini or similar smaller models is cost-effective enough, especially for straightforward extraction tasks.

---

## Should I extract multiple attributes in a single API call or separate them?

It's often better to separate extraction tasks into multiple focused API calls rather than trying to extract everything at once. When multiple attributes are extracted in a single prompt, changes to one attribute's extraction can unintentionally affect others. For example, requesting shorter action items might inadvertently make summaries shorter as well. Breaking these into separate jobs gives you better control, and techniques like prompt caching can help manage costs by avoiding redundant processing of the same input text.

---

## How can I blend traditional ML with LLMs for recommendation systems?

Rather than using LLMs directly in recommendation systems, consider using them to:

1. Generate better embeddings for items and users
2. Create synthetic data to help with cold-start problems
3. Simulate user behavior for new items that lack transaction data
4. Extract structured attributes that can feed into traditional recommendation models

At companies like Stitch Fix, the approach has been to use a cascade of models (vision, text, feedback, factorization) that build different scores, then blend these scores into a final probability-of-sale model.

---

## What are effective strategies for specialized indices versus general embeddings?

For complex queries like "Who is the best European basketball player under 25 years old?", general embeddings often fall short. Instead, consider:

1. Building structured data extractors that pull out specific attributes (age, nationality, sport)
2. Creating a portfolio of specialized tools rather than relying on a single embedding approach
3. Using different representations for different types of data
4. Exposing multiple tools that might access the same index in different ways

The trend is moving toward having multiple specialized tools rather than trying to build a single "mega search tool" that works for all cases.

---

## How are companies handling data engineering for LLM applications?

Data engineering remains a significant challenge. Many companies are still figuring out best practices for:

1. Creating and maintaining evaluation datasets
2. Building extraction pipelines that can be easily updated
3. Managing backfills when new attributes need to be extracted
4. Ensuring consistency across teams using the same data

For companies exploring this space, tools like Tensor Lake might be worth investigating, as they're designed for tensor-based data processing at scale.

---

## Will better reasoning models eliminate the need for specialized indices?

Not entirely. Even as models improve at reasoning, having a portfolio of specialized tools remains valuable. The approach is shifting toward giving models access to multiple tools that can retrieve and process data in different ways, rather than expecting a single model to handle everything. For example, instead of one mega-search tool, you might have tools for listing directories, viewing files, filtering by metadata, semantic search, and full-text search - all potentially accessing the same underlying data but in different ways.
