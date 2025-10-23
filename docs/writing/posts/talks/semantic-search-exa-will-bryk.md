---
title: Why Google Search Sucks for AI (Will Bryk, Exa)
speaker: Will Bryk
cohort: 3
description: How AI is changing search requirements and the technical challenges of building a semantic search engine designed for AI applications rather than human users.
tags: [semantic search, AI search, embeddings, web search, Exa]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Why Google Search Sucks for AI (Will Bryk, Exa)

I hosted a session with Will Bryk from Exa who shared insights about the evolution of search technology, how AI is changing search requirements, and the technical challenges of building a semantic search engine. This session explores how traditional search engines like Google differ from next-generation semantic search systems designed for AI applications rather than human users.

<!-- more -->

[▶️ Watch How Exa Rebuilt Search for AI](https://maven.com/p/18711e){: .md-button .md-button--primary}

## Why is traditional search inadequate for the AI era?

The fundamental problem with traditional search engines like Google is that they were built for humans, not AI systems. This creates a significant mismatch in capabilities and requirements.

Humans and AI systems interact with search in fundamentally different ways. Humans typically use simple keyword queries because they're "lazy" and can't type full sentences. They generally want just a few high-quality links since they have limited capacity to process information. This is why Google optimized for keyword-based algorithms that return a handful of results.

AI systems, by contrast, can instantly generate complex, precise queries that specify exactly what they want. They can consume and analyze massive amounts of information without getting overwhelmed. When an AI asks for "startups working on something huge like Bell Labs," it doesn't want Reddit discussions - it wants comprehensive, structured information about actual startups.

As Will explained: "It would kind of be insane if the same search engine that was optimal for humans would also be optimal for this very different creature." This insight is still not widely understood in the industry, even as everyone recognizes that combining search with LLMs is powerful.

**_Key Takeaway:_** Traditional search engines were optimized for human behavior patterns (simple keywords, few results), while AI systems need search engines that can handle complex queries and return comprehensive, precisely targeted information.

## How do AI search needs differ from human search needs?

AI systems have several distinct requirements that traditional search engines weren't designed to address:

1. Precise, controllable information: AIs need search engines that respect exactly what they ask for, rather than optimizing for what humans typically click on. If an AI is searching for "startups working on something huge," it needs a list of actual startups, not Reddit discussions about the topic.

1. Context-rich queries: AIs often have extensive context from user interactions that should inform their searches. Traditional search engines have keyword limits and can't handle paragraph-length queries, forcing the AI to convert rich context into a few keywords, which loses tremendous information.

1. Comprehensiveness: Unlike humans who want a few links, AIs can process thousands of results. If an AI is asked to analyze "every YC-funded AI startup," it needs a search engine that can deliver comprehensive results rather than just the top 10 most popular pages.

Will used a powerful visual metaphor, showing the space of possible search queries as a vast gray zone, with traditional search engines only covering a small blue bubble within it. As he explained: "Google has trained us to only think about this keyword bubble... But there's actually many different types of queries that people might want to make that go way beyond what Google can handle."

**_Key Takeaway:_** AI systems need search engines that can handle precise queries, incorporate rich context, and deliver comprehensive results - capabilities that fall outside the design parameters of traditional search engines built for humans.

## How does Exa's approach to search differ from traditional search engines?

Exa takes a fundamentally different approach to search compared to traditional engines like Google. While Google's original PageRank algorithm from 1998 focused on analyzing the web's link structure and matching keywords, Exa uses an embedding-based neural approach that understands the semantic meaning of content.

The core technical difference is that Exa processes documents into embedding vectors that capture their meaning, rather than just indexing keywords. When a query comes in, Exa embeds it in the same vector space and finds documents with similar meaning, regardless of whether they share the exact keywords.

This approach allows Exa to handle queries that would be impossible with traditional search engines:

- Long, contextual queries (like pasting an entire research paper and asking for similar papers)
- Semantic queries ("people in SF who know assembly language")
- Complex analytical queries ("find every article that argues X and not Y from author Z")

Will emphasized that Exa's philosophy is to give users complete control over their search experience: "The philosophy here is we want to give users full control. Give the AI system full control to get what information they want." This includes the ability to filter by date ranges, domains, and content categories, and even specify what sources they consider authoritative.

This approach reflects a deeper philosophical stance: "If you give full control to the user to specify what they want, you are freeing them from whatever ideology that previous search engines had."

**_Key Takeaway:_** Exa uses neural embedding technology rather than keywords to understand query meaning, enabling it to handle complex, contextual searches that traditional engines can't process. Their philosophy emphasizes giving users complete control over their search parameters.

## What technical challenges arise when building a semantic search engine?

Building a web-scale semantic search engine involves numerous technical challenges, particularly around efficiency and scale. Will walked through several key components of Exa's system:

1. Crawling and storage: The process begins with gathering URLs to crawl, building distributed crawling systems that can handle different formats (like PDFs), and storing petabytes of data in formats that enable efficient batch processing.

1. Embedding generation: Documents are processed through embedding models that convert text into vector representations capturing their meaning. This is computationally intensive at web scale.

1. Vector database optimization: The most significant challenge is efficiently searching billions of embedding vectors. A naive approach would be prohibitively expensive and slow.

To make this practical, Exa employs several optimization techniques:

- Matryoshka embeddings: Training models to create embeddings where smaller subsets of the vector still represent the full meaning, allowing for dimension reduction
- Clustering: Grouping similar embeddings so searches only need to examine the most relevant clusters
- Binary compression: Converting floating-point embeddings to boolean values for faster processing
- Assembly-level optimizations: Using SIMD operations and low-level CPU optimizations

As Will explained: "When you're doing over billions of documents, billions of binary compressed embeddings using clustering, it's still too slow. A lot of the advances or speed-ups we got were from going into the actual assembly and the SIMD operations on the low-level stuff on the CPU."

Even with these optimizations, some complex queries require what Will calls "test-time compute" - searches that might take minutes or hours rather than milliseconds: "Perfect search requires test-time compute... your search could sometimes take half a second, but sometimes it could take a minute or 10 minutes, or an hour or a day for super complex things."

**Key Takeaway:** Building semantic search at web scale requires sophisticated optimizations at every level, from embedding generation to vector database design. Some complex queries fundamentally require more computation time, creating a new paradigm of "test-time compute" search.

## How does Exa position itself in the AI ecosystem?

Exa positions itself as search infrastructure rather than a consumer application. In the current AI ecosystem, there are search infrastructure providers (Google, Bing, Exa) that crawl and index the web, and AI applications that build on top of them (like Gemini using Google or Search GPT using Bing).

Will explained: "Exa is trying to be the search infrastructure, and we want to be able to handle all these possible queries. That's our goal." When an AI application needs information from the web, it forms a query, sends it to Exa, and Exa returns the most relevant information, which the application can then use in its processing.

This infrastructure approach differs from consumer-facing products like Perplexity. While those products use search under the hood, Exa aims to be the underlying search engine that powers all types of AI applications, with an API optimized for AI rather than human users.

The business model also creates different incentives compared to traditional search engines. While Google makes money from ads, Exa charges per query: "Our incentive is to make people like the search as much as possible, get the highest quality information so that they use it more. Whereas Google's incentive is making them click on ads."

This creates what Will calls "pristine incentives" where Exa's mission aligns with its financial interests: "Because we have these very pristine incentives, our mission is very aligned with our financial incentives. So it's a very beautiful thing."

**_Key Takeaway:_** Exa positions itself as search infrastructure optimized for AI applications rather than human users, with a business model based on query volume rather than advertising, creating incentives aligned with delivering high-quality search results.

## What does "perfect search" look like?

Will's vision for "perfect search" extends far beyond current capabilities, enabling queries that most people don't even think to try because they know current tools can't handle them.

Examples of perfect search capabilities include:

- Finding people with specific expertise: "I'm creating a Discord of best prompting practices. Find me anyone who's ever thought deeply about this on the web."
- Location-specific expertise: "Who in Berlin has written about new search algorithms?"
- Multimodal search: "Find images of shirts without stripes that have a cool mix of colors like a Jackson Pollock"
- Curated media: "Find me Hans Zimmer music with a fast beat similar to the song Supermarine"
- Complex analysis: "Show me analyses of this topic by liberal authors, then by conservative authors, then by conservative authors who used to be liberal"

Will believes that perfect search would fundamentally transform our relationship with information: "People don't realize how much more the world's knowledge would actually be at your fingertips."

However, he acknowledges that achieving this vision will take time: "I would say like 2028 search will be amazing, like magical. And we'll look back on 2025, and we'll be like, 'Oh my God! They didn't know anything about the world.'" Even then, he believes there will still be many types of searches that remain impossible.

Like AI itself, search is a domain where there's always room for improvement: "No matter how good your LLM is, you could always do better. I think similarly, no matter how good your search is, you could always do better."

**_Key Takeaway:_** Perfect search would enable queries that most people don't even consider trying today, fundamentally transforming our access to information. While significant progress will be made in the coming years, search will remain an open-ended problem with continuous room for improvement.

## How can developers build effective search systems for specific domains?

For developers building search systems over specific domains (like medical records or legal documents), Will offered several practical insights:

The search problem becomes easier at smaller scales. When you're dealing with millions rather than billions of documents, you don't need the same sophisticated techniques required for web-scale search.

For most domain-specific applications, a hybrid approach combining keyword methods and embedding space methods works well. The optimal approach depends on your query distribution - if users primarily make simple queries, simpler systems may suffice, but complex semantic queries require more sophisticated models.

Query expansion (taking a query and expanding it into hundreds of related terms) can be effective for improving recall, though it won't match the capabilities of true semantic search for complex queries.

When building these systems, developers should focus on understanding what their users actually need: "You have to think about their query distribution - are your queries simple ones like 'GPT-3 paper,' or complex ones like 'a paper where people have this experiment setup that feels like this other setup'?"

For teams with limited resources (3-6 months to build something), Will suggested focusing on hybrid approaches that combine the strengths of keyword and embedding-based systems, as this provides a good balance of capabilities without requiring the development of custom models.

**_Key Takeaway:_** Domain-specific search systems can use simpler approaches than web-scale engines, with hybrid keyword and embedding methods working well for most applications. Understanding your users' query patterns should guide your technical approach.

## How will search evolve in the coming years?

Will believes we're at the beginning of a fundamental transformation in search technology. He used the metaphor of San Francisco during an earthquake to describe the current state of the industry: "The whole software world is going through this tectonic shift. Because the way we get information seemed to be radically changing."

Several trends are driving this transformation:

1. The limitations of LLMs: Despite their capabilities, LLMs haven't memorized the entire web. Will explained: "The LLM simply cannot memorize the entire web... The web is gigantic. It's really, really big." This creates an inherent need for retrieval systems.

1. The expansion of query types: As search tools improve, people will discover entirely new types of queries they never thought to try before. Will believes there are "many, many types of queries that go beyond the ones listed here that we haven't even thought of, because our tools can't handle it."

1. Test-time compute: Complex queries fundamentally require more computation time. Future search engines will need to handle queries that take minutes, hours, or even days to complete for particularly complex analyses.

1. Multimodal search: Future search will extend beyond text to include sophisticated image, audio, and video search capabilities.

Will sees the search market fragmenting rather than being dominated by a single player: "The space of possible searches is so broad that it's actually really hard for one company to be perfect at everything... It's bifurcating in all these ways. It's splintering."

This creates opportunities for specialized search providers focused on particular capabilities or domains: "I think the search space is big enough where there are lots of winners."

**_Key Takeaway:_** Search is undergoing a fundamental transformation driven by AI capabilities, with the market likely to fragment into specialized providers rather than being dominated by a single approach. Future search will handle query types and modalities that we can't even imagine today.

---

FAQs:

## What is Exa and how is it different from traditional search engines?

Exa is a semantic search engine built specifically for AI systems rather than humans. Unlike traditional search engines like Google that use keyword-based algorithms optimized for human users, Exa uses neural embedding-based algorithms that understand the meaning and context of queries. This allows Exa to handle complex, lengthy queries and return precisely relevant results rather than just matching keywords.

## Why do AI systems need a different kind of search engine than humans?

AI systems interact with search engines very differently than humans do. While humans typically use simple keyword queries and only want a few results, AI systems can formulate complex, detailed queries instantly and can process thousands of results at once. Traditional search engines were designed around human limitations and preferences, making them suboptimal for AI applications that need comprehensive, precise information retrieval.

## How does Exa's search technology work?

Exa processes web documents through embedding models that convert text into vectors (lists of numbers) that capture the meaning of the content. When a query comes in, it's also converted to an embedding, and Exa finds the most semantically similar documents. To make this process efficient at scale, Exa uses several techniques including Matryoshka embeddings (nested representations of different sizes), clustering (grouping similar documents), binary compression, and low-level optimizations to handle billions of documents quickly.

## What kinds of queries can Exa handle that traditional search engines cannot?

Exa can handle several types of queries that traditional search engines struggle with:

- Long, contextual queries (entire paragraphs or code snippets)
- Semantic queries (e.g., "people in SF who know assembly language")
- Complex, multi-condition queries (e.g., "Find every article that argues X and not Y from author Z")
- Queries with very specific information needs that require precise understanding of language

## How does Exa fit into the AI application ecosystem?

Exa positions itself as search infrastructure for AI applications. When an AI application needs information from the web, it sends a query to Exa, which returns the most relevant information. This is similar to how AI applications like Google's Gemini or OpenAI's ChatGPT use Google and Bing respectively as their search infrastructure. Exa aims to provide a more powerful and flexible API specifically designed for AI needs.

## What is "test time compute" search and why is it important?

Test time compute search refers to search operations that may take longer than traditional search (from seconds to minutes or even hours) because they involve more complex processing. This approach is necessary for truly complex search queries that require deeper analysis. Similar to how complex AI tasks might require more powerful models, complex search queries require more computational resources. Exa's approach acknowledges that some valuable search capabilities simply can't be delivered in milliseconds.

## What is "perfect search" and how is Exa working toward it?

Perfect search is Exa's vision of a search system that can handle any type of query across any type of content. This includes finding people with specific expertise, searching for multimodal content with precise attributes, curating content based on complex criteria, and performing sophisticated analyses across different perspectives. Exa is working toward this by building a search infrastructure that understands language deeply and can be customized to handle increasingly complex information needs.

## What is Exa's business model?

Unlike traditional search engines that make money from advertising, Exa charges on a usage basis (per query). This creates an incentive structure where Exa benefits from providing the highest quality search results possible so that customers will use the service more, rather than optimizing for ad clicks.

## Does Exa handle content behind paywalls?

No, Exa only searches content that is publicly accessible and not behind paywalls.

## How does Exa handle SEO manipulation?

Exa's neural embedding-based approach makes it inherently more resistant to traditional SEO manipulation techniques that work on keyword-based algorithms. Additionally, since Exa is focused on providing high-quality information rather than generating ad revenue, it has stronger incentives to filter out low-quality SEO-optimized content.

## How does Exa handle document size and chunking?

Exa works with web documents which naturally have a structure that makes them manageable for embedding. While there are limits to document size, Exa can handle most web content effectively. The company is exploring chunking strategies for longer documents but has found that the natural structure of web content often provides reasonable document boundaries.

--8<--
"snippets/enrollment-button.md"
--8<--
