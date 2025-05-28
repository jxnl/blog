---
title: "Running Effective AI Standups"
description: "Learn how to enhance AI engineering processes through rigorous and insightful updates, focusing on hypotheses, interventions, results, and trade-offs."
categories:
  - "Applied AI"
  - "Software Engineering"
  - "Writing and Communication"
tags:
  - "AI Engineering"
  - "Communication"
  - "Project Management"
date: 2024-10-25
comments: true
authors:
  - jxnl
---

# SWE vs AI Engineering Standups

When I talk to engineering leaders struggling with their AI teams, I often hear the same frustration: "Why is everything taking so long? Why can't we just ship features like our other teams?"

This frustration stems from a fundamental misunderstanding: AI development isn't just engineering - it's applied research. And this changes everything about how we need to think about progress, goals, and team management. In a previous article I wrote about [communication](./ai-engineering-communication.md) for AI teams. Today I want to talk about standups specifically.

The ticket is not the feature, the ticket is the experiment, the outcome is learning.

<!-- more -->

!!! "note" "Who am I?"
I'm an AI engineering consultant specializing in process improvement for rapidly growing startups. With a background as a staff machine learning engineer, I've spent the past year collaborating with numerous AI startups. This experience has given me unique insights into common pitfalls and best practices in the field. My goal is to help engineering teams avoid recurring mistakes and implement more effective, data-driven processes for AI development and deployment.

## The Fundamental Difference

Traditional software development is deterministic: if you want to build a rate-limiting feature, you know exactly what success looks like. The path might be complex, but it's knowable. The question isn't "if" but "how."

AI development exists in a different realm. When we say we want to "improve accuracy" or "reduce hallucinations," we're not just implementing a known solution - we're investigating if a solution is even possible. It's more akin to scientific research than traditional engineering.

Consider these two scenarios:

**Engineering Task:**

> "Implement OAuth2 authentication for our API"

- Clear requirements
- Known best practices
- Deterministic outcome
- Success is binary
- Timeline is predictable

**AI Research Task:**

> "Reduce hallucinations in our model's outputs"

- Unknown if fully solvable
- Multiple competing approaches
- Probabilistic outcomes
- Success is a spectrum
- Timeline is uncertain

## Why This Matters for Leadership

This fundamental difference means we need to radically rethink how we measure progress and set goals. Here's why:

1. **Progress Isn't Linear**
   In traditional engineering, 50% through the timeline often means 50% done. In research, you might spend weeks making no progress and then have a breakthrough. Or worse, prove your entire approach won't work.

2. **Success Isn't Guaranteed**
   Sometimes the science itself simply won't support our product goals. No amount of engineering excellence can change the underlying mathematics or limitations of our current approaches.

3. **Speed of Learning > Speed of Development**
   The key metric isn't how fast we can implement solutions - it's how quickly we can test hypotheses and learn from the results.

This fundamental difference means we need to radically rethink how we measure progress and setting goals

## Aside, Leading vs Lagging Indicators

Before diving into AI-specific metrics, let's revisit the concept of leading and lagging indicators, which I've discussed in detail in my [article on setting goals](./getting-goals.md). This concept is crucial for understanding how to measure progress in AI development effectively.

### Leading vs Lagging Indicators: A Fitness Analogy

Imagine you're trying to lose weight. Your weight on the scale is a lagging indicator - it's the ultimate metric you care about, but not something you can directly control. In contrast, the number of workouts you complete or the calories you consume are leading indicators. These are metrics you can directly influence, which in turn affect your weight.

- **Lagging Indicator**: Weight on the scale
- **Leading Indicators**: Workouts completed, calories consumed

### Applying This to AI Development

In AI development, we can draw a similar parallel:

- **Lagging Indicator**: Model accuracy, reduction in hallucinations
- **Leading Indicators**: Number of experiments run, hypotheses tested, data quality improvements

Just as focusing solely on your weight can be discouraging and uninformative in a fitness journey, fixating only on model performance metrics in AI development can lead to frustration and missed insights.

### Product Metrics vs. Experimental Metrics

This analogy extends to product development as well:

- **Lagging Indicator (Product Metric)**: User engagement, revenue
- **Leading Indicators (Experimental Metrics)**: A/B test velocity, feature iteration speed, user feedback collection rate

By focusing on these leading indicators or experimental metrics, teams can:

1. Maintain motivation and momentum
2. Identify bottlenecks in the development process
3. Make data-driven decisions about resource allocation
4. Foster a culture of continuous learning and improvement

Remember, in both fitness and AI development, the key to long-term success lies in consistently improving your leading indicators. This approach ensures you're making progress even when the lagging indicators (weight or model performance) might not show immediate results.

## The Research Mindset in Practice

Here's what this means for your team:

### 1. Focus on Input Metrics

Instead of asking "Why isn't accuracy improving?", ask:

- How many hypotheses did we test this week?
- What's our experiment velocity?
- Where are we spending time between experiments?
- What's preventing us from running more experiments?

### 2. Build Scientific Intuition

Each experiment, successful or not, should improve the team's intuition about:

- What approaches are likely to work
- What the fundamental limitations might be
- Where the unexplored territories are
- Which paths are dead ends

### 3. Embrace Uncertainty

Leaders need to get comfortable with updates like:

> "We ran 5 experiments this week. All failed, but we've eliminated three major approaches and identified a promising new direction. Our hypothesis space is narrowing."

This is what progress looks like in research.

## Making Better Decisions

When you embrace the research mindset, different questions emerge:

Instead of:

> "When will the accuracy improve?"

Ask:

> "What's preventing us from running more experiments to improve accuracy this quarter?"

Instead of:

> "Why isn't this working yet?"

Ask:

> "What have we learned about what doesn't work and why?"

Instead of:

> "Can we speed this up?"

Ask:

> "What's preventing us from experimenting faster?"

## The Metrics That Matter

Here are the metrics I track that actually help me make decisions:

1. **Experiment Velocity**

   - Number of hypotheses tested per week
   - Average time per experiment

2. **Learning Efficiency**

   - Quality of documentation from failed experiments
   - Growth in team's understanding of the problem space

3. **Infrastructure Health**
   - Time spent waiting for compute/data
   - Reproducibility of experiments
   - Time to test new hypotheses

## A Better Way to Set Goals

Instead of:

> "Improve accuracy by 10% this quarter"

Try:

> "Run 15 experiments per month, with each experiment having clear success/abandon criteria and documented learnings"

This changes the conversation from "Why aren't we succeeding?" to "How can we run more experiments? What's slowing us down? How can we learn faster?"

## When Research Meets Product

The hardest part of AI development is balancing research reality with product needs. Here's how I approach it:

1. **Set Dual Metrics**

   - Research metrics: experiment velocity, learning rate
   - Product metrics: accuracy, latency, cost

2. **Time-box Research Phases**

   - Set clear decision points
   - Define minimum viable improvements
   - Have backup plans for insufficient progress

3. **Maintain Option Value**
   - Keep exploring alternative approaches
   - Build modular systems that can swap approaches
   - Document learnings for future attempts

## Conclusion

The fundamental nature of AI development as research rather than pure engineering isn't a bug - it's a feature. By embracing this reality and adjusting our management approach accordingly, we can:

- Make better resource decisions
- Set more realistic expectations
- Measure progress more effectively
- Build stronger, more capable teams

The key is shifting focus from output metrics ("why isn't accuracy improving?") to input metrics ("how can we run more experiments?"). This not only leads to better decision-making but also helps build the scientific intuition necessary for long-term success in AI development.

Remember: You're not just building features as if you're connecting a react app to a database - you're pushing the boundaries of what's possible as new models are developed.
