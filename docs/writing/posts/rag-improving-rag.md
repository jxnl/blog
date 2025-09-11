---
authors:
  - jxnl
categories:
  - RAG
comments: true
date: 2024-05-22
description: Discover systematic strategies to enhance your Retrieval-Augmented Generation
  (RAG) systems for better performance and user experience.
draft: false
tags:
  - RAG
  - AI
  - Machine Learning
  - Data Retrieval
  - Performance Optimization
---

# Systematically Improving Your RAG

This article explains how to make Retrieval-Augmented Generation (RAG) systems better. It's based on a talk I had with [Hamel](https://hamel.dev) and builds on other articles I've written about RAG. For a comprehensive understanding of RAG fundamentals, see my guide on [what RAG is](./rag-what-is-rag.md).

In [RAG is More Than Just Embeddings](../posts/rag.md), I talk about how RAG is more than just vector embeddings. This helps you understand RAG better. I also wrote [How to Build a Terrible RAG System](../posts/rag-inverted.md), where I show what not to do, which can help you learn good practices.

If you want to learn about how complex RAG systems can be, check out [Levels of RAG Complexity](../posts/rag-levels-of-rag.md). This article breaks down RAG into smaller parts, making it easier to understand. For quick tips on making your RAG system better, read [Low Hanging Fruit in RAG](../posts/rag-low-hanging-fruit.md).

I also wrote about what I think will happen with RAG in the future in [Predictions for the Future of RAG](../posts/rag-plusplus.md). This article talks about how RAG might be used to create reports in the future.

All these articles work together to give you a full guide on how to make RAG systems better. They offer useful tips for developers and companies who want to improve their systems. For additional improvement strategies, check out my [six tips for improving RAG](./rag-six-tips-improving.md) and insights on [RAG anti-patterns](./rag-anti-patterns-skylar.md). If you're interested in AI engineering in general, you might enjoy my talk at the [AI Engineer Summit](../posts/aisummit-2023.md). In this talk, I explain how tools like Pydantic can help with prompt engineering, which is useful for building RAG systems.

Through all these articles, I try to give you a complete view of RAG systems. I cover everything from basic ideas to advanced uses and future predictions. This should help you understand and do well in this fast-changing field.

By the end of this post, you'll understand my step-by-step approach to making RAG applications better for the companies I work with. We'll look at important areas like:

- Making fake questions and answers to quickly test how well your system works
- Using both full-text search and vector search together for the best results
- Setting up the right ways to get feedback from users about what you want to study
- Using grouping to find sets of questions that have problems, sorted by topics and abilities
- Building specific systems to improve abilities
- Constantly checking and testing as you get more real-world data

Through this step-by-step runbook, you'll gain practical knowledge on how to incrementally enhance the performance and utility of your RAG applications, unlocking their full potential to deliver exceptional user experiences and drive business value. Let's dive in and explore how to systematically improve your RAG systems together!

<!-- more -->

## Start with Synthetic Data

I think the biggest mistake around improving the system is that most people are spending too much time on the actual synthesis without actually understanding whether or not the data is being retrieved correctly. To avoid this:

- Create synthetic questions for each text chunk in your database
- Use these questions to test your retrieval system
- Calculate precision and recall scores to establish a baseline
- Identify areas for improvement based on the baseline scores

What we should be finding with synthetic data is that synthetic data should just be around 97% recall precision. And synthetic data might just look like something very simple to begin with.

We might just say, for every text chunk, I want it to synthetically generate a set of questions that this text chunk answers. For those questions, can we retrieve those text chunks? And you might think the answer is always going to be yes. But I found in practice that when I was doing tests against essays, full text search and embeddings basically performed the same, except full text search was about 10 times faster. This approach is part of my broader [RAG flywheel strategy](./rag-flywheel.md).

Whereas when I did the same experiment on pulling issues from a repository, it was the case that full text search got around 55% recall, and then embedding search got around 65% recall. And just knowing how challenging these questions are on the baseline is super important to figure out what kind of experimentation you need to perform better.
This will give you a baseline to work with and help you identify areas for improvement. For a detailed breakdown of evaluation metrics, see my guide on [the only 6 RAG evaluations you need](./rag-only-6-evals.md).

## Utilize Metadata

Ensuring relevant metadata (e.g., date ranges, file names, ownership) is extracted and searchable is crucial for improving search results.

- Extract relevant metadata from your documents
- Include metadata in your search indexes
- Use query understanding to extract metadata from user queries
- Expand search queries with relevant metadata to improve results

For example, if someone asks, "What is the latest x, y, and z?" Text search will never get that answer. Semantic search will never get that answer.

You need to perform query understanding to extract date ranges. There will be some prompt engineering that needs to happen. For enterprise implementations, see my guide on [RAG enterprise process](./rag-enterprise-process.md). That's the metadata, and being aware that there will be questions that people aren't answering because those filters can never be caught by full text search and semantic search.

And what this looks like in practice is if you ask the question, what are recent developments in the field, the search query is now expanded out to more terms. There's a date range where the language model has reasoned about what recent looks like for the research, and it's also decided that you should only be searching specific sources. If you don't do this, then you may not get trusted sources. You may be unable to figure out what recent means.

You'll need to do some query understanding to extract date ranges and include metadata in your search.

## Use Both Full-Text Search and Vector Search

Utilize both full-text search and vector search (embeddings) for retrieving relevant documents. Ideally, you should use a single database system to avoid synchronization issues.

- Implement both full-text search and vector search
- Test the performance of each method on your specific use case
- Consider using a single database system to store both types of data
- Evaluate the trade-offs between speed and recall for your application

In my experience, full-text search can be faster, but vector search can provide better recall.

What ended up being very complicated was if you have a single knowledge base, maybe that complexity is fine, because you have more configuration of each one.

But one of my clients who was doing construction data, they had to create separate indices per project, and now they just had this exploding array of different data sources that get in or out of sync. Like, maybe the database has an outage, and now the data is not in the database, but it's in another system. So if the embedding gets pulled up, then text is missing.

And this complex configuration becomes a huge pain. And so, for example, some tools are able to do all 3 in a single object. And so even if you had a lot of partitioned data sources, you can do full text search, embedding search, and write SQL against a single data object. And that has been really helpful, especially when you think about these examples where you want to find the latest. Now you can just do a full text search query and then order by date and have a between clause.

Test both and see what works best for your use case.

## Implement Clear User Feedback Mechanisms

Implementing clear user feedback systems (e.g., thumbs up/down) is essential for gathering data on your system's performance and identifying areas for improvement.

- Add user feedback mechanisms to your application
- Make sure the copy for these mechanisms clearly describes what you're measuring
- Ask specific questions like "Did we answer the question correctly?" instead of general ones like "How did we do?"
- Use the feedback data to identify areas for improvement and prioritize fixes

I find that it's important to build out these feedback mechanisms as soon as possible. And making sure that the copy of these feedback mechanisms explicitly describe what you're worried about.

Sometimes, we'll get a thumbs down even if the answer is correct, but they didn't like the tone. Or the answer was correct, but the latency was too high. Or it took too many hops.

This means we couldn't actually produce an evaluation dataset just by figuring out what was a thumbs up and a thumbs down. It was a lot of confounding variables. We had to change the copy to just "Did we answer the question correctly? Yes or no." We need to recognize that improvements in tone and improvements in latency will come eventually. But we needed the user feedback to build us that evaluation dataset.

Make sure the copy for these feedback mechanisms explicitly describes what you're worried about. This will help you isolate the specific issues users are facing.

## Cluster and Model Topics

Analyze user queries and feedback to identify topic clusters, capabilities, and areas of user dissatisfaction. This will help you prioritize improvements.

Why should we do this? Let me give you an example. I once worked with a company that provided a technical documentation search system. By clustering user queries, we identified two main issues:

1. Topic Clusters: A significant portion of user queries were related to a specific product feature that had recently been updated. However, our system was not retrieving the most up-to-date documentation for this feature, leading to confusion and frustration among users.

2. Capability Gaps: Another cluster of queries revealed that users were frequently asking for troubleshooting steps and error code explanations. While our system could retrieve relevant documentation, it struggled to provide direct, actionable answers to these types of questions.

Based on these insights, we prioritized updating the product feature documentation and implementing a feature to extract step-by-step instructions and error code explanations. These targeted improvements led to higher user satisfaction and reduced support requests.

Look for patterns like:

- Topic clusters: Are users asking about specific topics more than others? This could indicate a need for more content in those areas or better retrieval of existing content. I explore this concept further in my post on [RAG decomposition](./rag-decomposition.md) and [topics and capabilities](./topics_and_capabilities.md).

- Capabilities: Are there types of questions your system categorically cannot answer? This could indicate a need for new features or capabilities, such as direct answer extraction, multi-document summarization, or domain-specific reasoning.

By continuously analyzing topic clusters and capability gaps, you can identify high-impact areas for improvement and allocate your resources more effectively. This data-driven approach to prioritization ensures that you're always working on the most critical issues affecting your users.

Once you have this in place, once you have these topics and these clusters, you can talk to domain experts for a couple of weeks to figure out what these categories are explicitly. Then, you can build out systems to tag that as data comes in.

In the same way that when you open up ChatGPT and make a conversation, it creates an automatic title in the corner. You can now do that for every question. As part of that capability, you can add the classification, such as what are the topics and what are the capabilities. Capabilities could include ownership and responsibility, fetching tables, fetching images, fetching documents only, no synthesis, compare and contrast, deadlines, and so on. For more on selecting the right tools and capabilities, see my post on [trade-offs in tool selection](./trade-off-tool-selection.md).

You can then put this information into a tool like Amplitude or Sentry. This will give you a running stream of the types of queries people are asking, which can help you understand how to prioritize these capabilities and topics.

## Continuously Monitor and Experiment

Continuously monitor your system's performance and run experiments to test improvements.

- Set up monitoring and logging to track system performance over time
- Regularly review the data to identify trends and issues
- Design and run experiments to test potential improvements
- Measure the impact of changes on precision, recall, and other relevant metrics
- Implement changes that show significant improvements

This could include tweaking search parameters, adding metadata, or trying different embedding models. Measure the impact on precision and recall to see if the changes are worthwhile.

Once you now have these questions in place, you have your synthetic data set and a bunch of user data with ratings. This is where the real work begins when it comes to systematically improving your RAG.

The system will be running many clusters of topic modeling around the questions, modeling that against the thumbs up and thumbs down ratings to figure out what clusters are underperforming. It will then determine the count and probability of user dissatisfaction for each cluster.

The system will be doing this on a regular cadence, figuring out for what volume of questions and user satisfaction levels it should focus on improving these specific use cases.

What might happen is you onboard a new organization, and all of a sudden, those distributions shift because their use cases are different. That's when you can go in and say, "We onboarded these new clients, and they very much care about deadlines. We knew we decided not to service deadlines, but now we know this is a priority, as it went from 2% of questions asking about deadlines to 80%." You can then determine what kind of education or improvements can be done around that.

## Balance Latency and Performance

Finally, make informed decisions about trade-offs between system latency and search performance based on your specific use case and user requirements.

- Understand the latency and performance requirements for your application
- Measure the impact of different configurations on latency and performance
- Make trade-offs based on what's most important for your users
- Consider different requirements for different use cases (e.g., medical diagnosis vs. general search)

Here, this is where having the synthetic questions that test against will effectively answer that question. Because what we'll do is we'll run the query with and without this parent document retriever, and we will have a recall with and without that feature and the latency improvement of that feature.

And so now we'll be able to say, okay. Well, recall doubles. The latency increases by 20%, then a conversation can happen. Or, is that worth the investment? But if latency goes up double and the recall goes up 1%, again, it depends on, okay.

Well, if this is a medical diagnostic, maybe I do care that the 1% is included because the stakes are so high. But if it's for a doc page, maybe the increased latency will reduce in churn.

If you can improve recall by 1%, and the results are too complex, it's not worth deploying it in the future as well.

For example, if you're building a medical diagnostic tool, a slight increase in latency might be worth it for better recall. But if you're building a general-purpose search tool, faster results might be more important.

## Wrapping Up

This is was written based off of a 30 conversation with a client, so I know I'm skipping over many details and implementation details. Leave a comment and let me know and we can get into specifics.

## Want to learn more?

This was based on a 30-minute conversation, so I'm definitely skipping implementation details. The real breakthrough happens when you stop random improvements and start measuring what actually moves the needle:

[Free 6-Week RAG Email Course](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }
[Full Course Breakdown](./rag-course-breakdown.md){ .md-button } [RAG FAQ](./rag-faq.md){ .md-button }
