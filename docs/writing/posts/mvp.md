---
draft: False
date: 2024-02-13
slug: mvp
categories:
  - Personal
authors:
  - jxnl
---

# Leveraging the Pareto Principle in AI Application Development

Embarking on the journey of launching a new AI application is an exciting venture. I encourage you to pause and reflect on the essence of the Pareto Principle and how it applies to your application. Consider the critical questions: What does achieving 80% signify in your context? Who are the primary user segments you can effectively cater to? Does your application carve out a unique niche for itself? Is there an opportunity to focus intensively on the segments you excel in, manage expectations for the areas where you're less strong, and launch earlier to gather invaluable user feedback?

## Understanding the MVP Concept

An MVP, or Minimum Viable Product, is essentially the most basic version of your product that still offers enough value for early adopters to use and provide feedback. This feedback becomes the cornerstone for future enhancements and iterations of your product.

This concept, while straightforward in traditional product development, takes on a nuanced complexity when applied to AI applications.

## The 80/20 Rule Reimagined for AI

Traditionally, when we talk about something being 80% done or 80% ready, we usually refer to the classical machine learning sense. In this context, each component is deterministic, so 80% likely means that 8 out of 10 features are complete. Once we have the remaining 2 features, we can ship the product. IF we want to follow the 80/20 rule, we might be able to ship the product with 80% of the features and then add the remaining 20% later, like a car without a radio or air conditioning.
However, in the realm of AI-powered applications, the interpretation of "80%" can be much more fluid and less straightforward.

### The Pitfalls of Relying Solely on Summary Statistics

![](https://upload.wikimedia.org/wikipedia/commons/e/ec/Anscombe%27s_quartet_3.svg)

The illustration above, known as Anscombe's quartet, starkly demonstrates the limitations of relying solely on summary statistics. Despite sharing nearly identical statistical summaries, these datasets have vastly different distributions. This serves as a potent reminder of the risks of oversimplification.

Consider a hypothetical scenario with the following performance scores:

| Query_id | score |
| -------- | ----- |
| 1        | 0.9   |
| 2        | 0.8   |
| 3        | 0.9   |
| 4        | 0.9   |
| 5        | 0.0   |
| 6        | 0.0   |

At a glance, the average score of 0.58 might not seem impressive. However, a closer inspection might reveal excellence in serving a majority of the queries, underscoring the importance of segment analysis.

!!! note "Admitting what you're bad at"

    Acknowledging and transparently communicating the limitations of your application can significantly enhance user trust. If your system can identify its weaknesses and set clear expectations, it may be well-positioned for a successful launch, despite its imperfections.

The behavior of a probabilistic system could also be very different, consider the following example:

| Query_id | score |
| -------- | ----- |
| 1        | .59   |
| 2        | .58   |
| 3        | .59   |
| 4        | .57   |

In contrast, a system like this also has the same average score of 0.58, but it's not as easy to reject any subset of requests...

It is very important to understand the limitations of your system and to be able to confidently understand the charactersitics in your system beyond summary statistics.

### The Art of Declining Gracefully

Consider an application that struggles with specific query types, such as timeline-based queries. If these are known limitations, it might be more strategic to focus on strengths and manage user expectations for these weaker areas.

| Query_id | score   | query_type   |
| -------- | ------- | ------------ |
| 1        | 0.9     | text search  |
| 2        | 0.8     | text search  |
| 3        | 0.9     | news search  |
| 4        | 0.9     | news search  |
| 5        | **0.0** | **timeline** |
| 6        | **0.0** | **timeline** |

If we're in a pinch to ship, we could simply build a classification model that detects whether or not these questions are timeline questions and throw a warning. Instead of constantly trying to push the algorithm to do better, we can simply educate the user and educate them by changing the way that we might design the product.

So by identifying and classifying queries, you can guide users away from less reliable functionalities and towards the strengths of your application, enhancing overall user satisfaction.

!!! note "Detecting segments"

    Detecting these segments could be accomplished in various ways. We could construct a classifier or employ a language model to categorize them. Additionally, we can utilize clustering algorithms with the embeddings to identify common groups and potentially analyze the mean scores within each group. The sole objective is to identify segments that can enhance our understanding of the activities within specific subgroups.

By changing the design of our application and understanding the limitations, we can have conditionally better performance if we know what kind of work we can turn down. If you are able can put this segment data into some kind of In-System Observability, you'll be able to safely monitor what proportion of questions you're turning down, and prioritize your work to maximize coverage.

One of the worst things you can do is to spend months building out a feature that only increases your productivity by a little while ignoring some more important segment of your user base.

### The Strategic Value of Focusing on a Niche

A common pitfall I've observed in the startup ecosystem is the assumption that just having AI technology means it's inherently useful across the board. This mindset often leads to the development of broad, unfocused applications that lack a clear purpose or target.

I strongly believe that startups, especially those venturing into AI, should concentrate their efforts on a few key areas where they can truly excel. By identifying and committing to a specific niche, your application can stand out by doing a few things exceptionally well. This focused approach not only makes it easier to attract and engage a dedicated user base—ranging from a few dozen to a couple hundred early adopters—but also facilitates rapid collection of targeted feedback.

An application that tries to be a jack-of-all-trades often ends up being master of none, leading to a forgettable user experience and difficulty in fostering repeat engagement. While broad appeal might initially attract a surge of interest, sustaining user trust and loyalty becomes a significant challenge.

In the context of leveraging advanced tools like GPT-4 for predictive functionalities, the speed at which you can gather and act on user feedback becomes crucial. Swift feedback loops enable rapid iterations, allowing for continuous improvement and refinement of your product. This agility is key to developing a more effective and user-centric application.

## Final Thoughts

In sum, crafting an MVP for an AI-driven application transcends the simplistic notion of launching with a subset of features. It demands a nuanced understanding of your user base, a strategic focus on areas of strength, and a commitment to transparency about limitations. By embracing these principles, you can foster a more engaging and valuable product, paving the way for rapid iteration and sustained improvement.
