---
authors:
  - jxnl
categories:
  - Applied AI
comments: true
date: 2024-11-18
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

# Decomposing RAG Systems to Identify Bottlenecks

There's a reason Google has separate interfaces for Maps, Images, News, and Shopping. The same reason explains why many RAG systems today are hitting a performance ceiling. After working with dozens of companies implementing RAG, I've discovered that most teams focus on optimizing embeddings while missing two fundamental dimensions that matter far more: Topics and Capabilities.

<!-- more -->

If you're interested in learning more about how to systematically improve RAG systems, you can sign up for the free email course here:

[Sign up for the Free Email Course](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }

Now, let's dive into some frequently asked questions from the course:

## A Tale of Unmet Expectations

Let me share a recent case study that illustrates this perfectly:

A construction company implemented a state-of-the-art RAG system for their technical documentation. Despite using the latest embedding models and spending weeks optimizing their prompts, user satisfaction stayed stubbornly around 50%. When we analyzed their query logs, we discovered something fascinating: 20% of queries were simply counting objects in blueprints ("How many doors are on the 15th floor?").

No amount of embedding optimization would help here. By adding a simple object detection model for blueprints, satisfaction for those queries jumped to 87% in just one week.

## The Two Dimensions That Actually Matter

After analyzing millions of queries across various industries, I've identified two fundamental dimensions that determine RAG system success:

1. **Topics**: Do we have the information users want?
2. **Capabilities**: Can we effectively access and process that information?

Let's dive deep into each dimension.

## Topics: Content Coverage

Topics represent your system's knowledge inventory. Think of this like a store's product catalog - you can't sell what you don't have.

### Examples of Topic Gaps:

- Missing documentation sections
- Lack of data for specific time periods
- Absence of particular use cases or scenarios
- Missing specific types of content (images, videos, tables)

### Real World Example: Netflix

When Netflix notices users searching for "Adam Sandler basketball movies", that's a topic gap - they simply don't have that content. No amount of better search or recommendations will help if the content doesn't exist.

## Capabilities: Processing Power

Capabilities represent your system's ability to manipulate and retrieve information in specific ways. This is where most RAG systems fall short.

### Common Capability Requirements:

1. **Temporal Understanding**

   - "What changed last week?"
   - "Show me the latest updates"
   - Understanding fiscal vs calendar years

2. **Numerical Processing**

   - Counting objects in documents
   - Calculating trends or changes
   - Aggregating data across sources

3. **Entity Resolution**
   - Connecting related documents
   - Understanding document hierarchies
   - Mapping aliases and references

### Real World Example: DoorDash

When DoorDash notices orders dropping after 9 PM, adding more restaurants won't help. They need a capability to filter for "open now" restaurants. No amount of inventory helps if users can't find what's actually available.

## The Impact on User Experience

Consider how these dimensions affect real user interactions:

1. **Topic Failures**:

   - "Zero results found"
   - Completely irrelevant responses
   - Missing critical information

2. **Capability Failures**:
   - Partially correct answers
   - Unable to process time-based queries
   - Can't compare or contrast information

## Building a Systematic Approach

Here's how to implement this framework in your RAG system:

1. **Analyze Query Patterns**

   - Categorize failed queries into topic vs capability gaps
   - Identify clusters of similar issues
   - Track frequency and impact of each gap

2. **Measure Impact**

   - Query volume (how often does this come up?)
   - Success rate (how often do we fail?)
   - Business impact (what does failing cost us?)

3. **Prioritize Improvements**
   - Focus on high-volume, low-success-rate queries
   - Balance implementation cost against potential impact
   - Build capabilities that can be reused across topics

## Best Practices for Implementation

1. **Start with Data Collection**

   - Log all queries and their success rates
   - Track which capabilities are used for each query
   - Monitor topic coverage over time

2. **Build Modular Systems**

   - Separate topic management from capability implementation
   - Allow for easy addition of new capabilities
   - Enable A/B testing of different approaches

3. **Measure Everything**
   - Track success rates by topic and capability
   - Monitor usage patterns of different capabilities
   - Calculate ROI of topic expansions

## Looking Forward

The future of RAG isn't just about better embeddings or larger context windows. It's about:

- Building specialized indices for different query types
- Developing robust capability routing systems
- Creating feedback loops for continuous improvement

## Conclusion

Stop focusing solely on embedding optimization. Start analyzing your queries through the lens of topics and capabilities. This framework will help you:

- Identify the real bottlenecks in your system
- Make strategic decisions about improvements
- Build a more effective and scalable RAG application

Remember: The goal isn't to build a perfect system. It's to build a system that gets better every day at solving real user problems.

---

_If you're working on a RAG system right now, try this: Take your last 20 failed queries and sort them into topic vs capability issues. You might be surprised by what patterns emerge._

If you're interested in learning more about how to systematically improve RAG systems, you can sign up for the free email course here:

[Sign up for the Free Email Course](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }
