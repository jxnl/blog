---
authors:
  - jxnl
categories:
  - Applied AI
comments: true
date: 2024-06-29
description: Explore the significance of topics and capabilities in enhancing RAG
  data applications and search functionalities across industries.
draft: false
tags:
  - RAG
  - Data Analysis
  - Search Functionality
  - Capabilities
  - Topics
---

# Art of Looking at RAG Data

In the past year, I've done a lot of consulting on helping companies improve their RAG applications. One of the biggest things I want to call out is the idea of topics and capabilities.

I use this distinction to train teams to identify and look at the data we have to figure out what we need to build next.

<!-- more -->

## Analyzing User Queries

When building or refining a search system, one of the most valuable practices is to **analyze the questions people are asking**. This isn't limited to traditional search engines; it applies to a wide range of industries, from streaming services to food delivery platforms. By examining these queries, we can identify patterns and clusters that reveal what users are truly seeking.

These clusters, whether identified manually or through sophisticated language models, fall into two main categories:

1. Topics
2. Capabilities

Let's explore what these mean and how they impact search functionality.

## Understanding Topics and Capabilities

**Topics**, in essence, are about _content coverage_. They answer the question:

> Do we have the information users are looking for?

For instance, if someone searches for a privacy policy but your database lacks any documents on privacy, that's a topic gap. No matter how advanced your search algorithm is, it can't provide information that doesn't exist in your system.

**Capabilities**, on the other hand, are about _how effectively you can find and present the information you do have_. This involves having the right metadata and indexing systems in place. You might have the content users want, but without the proper capabilities, your search system may struggle to surface it effectively.

## Industry Examples

Let's look at how some industry giants apply these concepts:

### Netflix

Netflix constantly analyzes viewer searches to identify topic gaps. Imagine they notice a surge in searches for "Adam Sandler Basketball movie." If they lack content in this specific area, they might consider producing a film to fill this topic gap.

But Netflix doesn't stop at content creation. They also enhance their capabilities by adding metadata. Imagine you realize that your embedding-based clustering model is trying to recommend Oscar-winning or Oscar-nominated films. If you're just using an LLM, "Oscar-nominated" might be a hallucination. So, if you want 100% accuracy on some of these capabilities, you need to add that additional metadata.

It might cost you some extra money, but it's definitely worth it to minimize hallucinations. Another simple example could be Christmas movies. You could either use embedding models to figure out what could or could not be a Christmas movie, or you can just spend the money and effort to get the metadata and be on with your day.

### Food Delivery Services

Even in the food delivery sector, we see this principle at work. Services like DoorDash might:

1. Identify a lack of certain cuisines in specific areas – a _topic gap_.
2. Actively seek partnerships with restaurants offering those cuisines to fill the gap.
3. Enhance their _capabilities_ by implementing filters like "open now," making it easier for users to find available options, or realise they might want to also serve groceries

## Key Takeaways

The key takeaway is that improving a search system is an ongoing process of addressing both topic and capability issues. It's about:

1. Ensuring you have the content users are looking for (topics)
2. Providing the tools to help them find it efficiently (capabilities)

Whether you're running a small e-commerce site or a large-scale information service, regularly assessing and improving in these two areas can significantly enhance your search functionality.
