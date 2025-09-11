---
authors:
  - jxnl
categories:
  - RAG
comments: true
date: 2024-08-19
description: Discover a systematic approach to enhance Retrieval-Augmented Generation
  (RAG) systems for improved performance and user satisfaction.
draft: false
slug: rag-flywheel
tags:
  - RAG
  - Data Optimization
  - User Feedback
  - Continuous Improvement
  - Machine Learning
---

# The RAG Playbook

When it comes to building and improving Retrieval-Augmented Generation (RAG) systems, too many teams focus on the wrong things. They obsess over generation before nailing search, implement RAG without understanding user needs, or get lost in complex improvements without clear metrics. I've seen this pattern repeat across startups of all sizes and industries.

But it doesn't have to be this way. After years of building recommendation systems, instrumenting them, and more recently consulting on RAG applications, I've developed a systematic approach that works. It's not just about what to do, but understanding why each step matters in the broader context of your business.

Here's the flywheel I use to continually infer and improve RAG systems:

1. Initial Implementation
2. Synthetic Data Generation
3. Fast Evaluations
4. Real-World Data Collection
5. Classification and Analysis
6. System Improvements
7. Production Monitoring
8. User Feedback Integration
9. Iteration

Let's break this down step-by-step:

<!-- more -->

If you want to learn more about I systematically improve RAG applications check out my free 6 email improving rag crash course

[Check out the free email course here](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }

## 1. Start with Synthetic Data

The biggest mistake I see teams make is spending too much time on complex generation before understanding if their retrieval even works. Synthetic data is your secret weapon here.

Generate synthetic questions for each chunk of text in your database. Use these to test your retrieval system and calculate precision and recall scores. This gives you a baseline to work from and helps identify low-hanging fruit for improvement.

Why is this so powerful?

- It helps you select the right embedding models and methods
- Enables lightning-fast evaluations (milliseconds vs. seconds per question)
- Allows rapid iteration and testing of ideas
- Can be done before you have any real user data
- Forces clarity on product goals and non-goals

!!! note "Improving Stand-ups"

    When you have concrete metrics like precision and recall, your stand-ups become far more productive. Instead of vague progress reports, you can say things like: "We improved recall by 5% by tweaking our chunking strategy." This focuses the team and gives leadership clear indicators of progress.

## 2. Focus on Leading Metrics

Here's a crucial mindset shift: stop obsessing over lagging metrics like overall application quality. They're important, but hard to directly improve. Instead, focus on leading metrics that predict improvements and are easier to act on.

For example:

- Number of retrieval experiments run per week
- Precision/recall improvements on synthetic data
- Time to run evaluation suite

It's like weight loss. Stepping on the scale (lagging metric) doesn't directly cause change. But tracking your workouts and diet (leading metrics) predicts weight changes and gives you clear actions to take.

## 3. Fast, Unit Test-Like Evaluations

Before you even think about complex generation, nail your retrieval with fast, unit test-style evaluations:

1. Take a search query
2. Find a list of relevant text chunks
3. Check if the desired chunk is in the results

This process should be blazing fast, allowing you to rapidly test changes in how you represent and index your text chunks. It's also great for verifying data recovery across different content types (tables, images, etc.).

!!! warning "Crawl Before You Walk"

    I've seen teams jump straight to end-to-end evaluations with LLM-generated responses. This is a mistake. Get your retrieval working first. It's easier to measure, usually the weak link, and sets a strong foundation for everything else.

## 4. Real-World Data and Clustering

Once you have some real user data, things get interesting. You'll quickly realize that real-world questions are often stranger and more idiosyncratic than your synthetic ones. They may not even have clear answers within your system.

This is where clustering becomes powerful:

1. Use unsupervised learning to identify question topics and patterns
2. Work with domain experts to refine and label these clusters
3. Build few-shot classifiers to generate topic distributions for new questions

Now you can analyze:

- Types and frequency of questions per topic
- Cosine similarity scores within clusters
- Customer satisfaction and feedback per topic

This segmentation is crucial. Just like Google eventually specialized into Maps, Images, and Shopping, you'll likely need to build targeted solutions for different question types.

## 5. Continuous Improvement Loop

Remember, RAG systems are never "done." Set up a continuous improvement cycle:

1. Monitor production data in real-time, classifying questions by topic
2. Identify changes in question patterns or new user needs
3. Regularly communicate with customers to validate quantitative findings
4. Prioritize improvements based on business impact and user satisfaction
5. Run targeted experiments to address specific topic or capability gaps
6. Iterate and refine your synthetic data generation based on new insights

!!! note "Detecting Concept Drift"

    One powerful technique is to include an "Other" category in your topic classification. Monitor the percentage of "Other" questions over time. If it starts growing unexpectedly, it's a strong signal that user behavior is shifting or you're onboarding customers with different needs.

## The Bigger Picture

This systematic approach does more than just improve your RAG system. It fundamentally changes how you operate:

- Stand-ups become focused on concrete experiments and metrics
- You build intuition for what actually moves the needle
- Product decisions are driven by data, not guesswork
- You can detect and adapt to changing user needs much faster

Remember, the goal isn't to have a perfect system on day one. It's to build a flywheel of continuous improvement that compounds over time. Start simple, measure relentlessly, and iterate based on real-world feedback. That's how you build RAG applications that truly deliver value.

## Want to learn more?

Ready to build your own data flywheel? The teams that nail this create systems that get better every day instead of slowly degrading. Need help getting started? I work with teams on this all the time:

[Consulting Services](../../services.md){ .md-button .md-button--primary }
[Free 6-Week RAG Email Course](https://dub.link/6wk-rag-email){ .md-button }
