---
authors:
  - jxnl
categories:
  - Software Engineering
comments: true
date: 2024-01-19
description: Explore key tips for developing probabilistic software and improving
  decision-making under uncertainty for junior engineers.
draft: false
slug: tips-probabilistic-software
tags:
  - probabilistic software
  - machine learning
  - junior developers
  - decision making
  - experiment design
---

# Tips for probabilistic software

This writing stems from my experience advising a few startups, particularly smaller ones with plenty of junior software engineers trying to transition into machine learning and related fields. From this work, I've noticed three topics that I want to address. My aim is that, by the end of this article, these younger developers will be equipped with key questions they can ask themselves to improve their ability to make decisions under uncertainty.

1. Could an experiment just answer my questions?
2. What specific improvements am I measuring?
3. How will the result help me make a decision?
4. Under what conditions will I reevaluate if results are not positive?
5. Can I use the results to update my mental model and plan future work?

<!-- more -->

## Who am I?

I really want to highlight the difference between software and science. In college, I studied physics and computational mathematics, where I worked on research in computational social science and epidemiology. I've worked at Facebook to build models that can detect and priotitize content moderation work flows, and I've built probabilistic systems at Stitchfix with vision models, product search, embeddings, and recommendation systems. However, I've never considered myself a software engineer.

If you want to learn about my consulting practice check out my [services](../../services.md) page. If you're interested in working together please reach out to me via [email](mailto:jason+hire@jxnl.co)

Why? None of these are things that I would consider software, in the classical sense. None of these things are features that could have been built on some kind of sprint: instead, these are all probabilistic systems that require significant exploration and experimentation to build.

Nowadays, I'm a technical advisor working on software teams, helping them level up their machine learning capabilities while coaching and mentoring junior engineers to think more probabilistically. As I've been doing this, I've noticed a few common pitfalls that folks are running into, and I want to call them out.

## What is probabilistic software?

When I say "probabilistic software", what I'm really talking about is a broad category of _systems that use machine learning_. These systems look at probabilities and distributions rather than discrete interactions, like an API call from one server to another.

In ML systems, we perform very distinct operations: we rank things, sort them, group them in a fuzzy manner in order to build features like recommendation systems and retrieval applications. These same fundamental tasks underlie hot topics like agents powered by LLMs.

## Edge cases and long tails

> You can think your way into solving a deterministic system, but you cannot think your way into solving a probabilistic system.

The first thing that I want to call out is that **deterministic software has edge cases, while probabilistic software has long tails.**

I find that a lot of junior folks try to really think hard about edge cases around probabilistic systems, and truthfully, it doesn't really make sense. It's unlikely that we can fully enumerate and count issues ahead of time: we can only work in percentages and probabilities.

Instead, you should be focusing your efforts on segmenting and clustering the distribution of inputs and solving these problems locally _before_ coming up with a hypothesis on how the global system might work.

Before deliberating with your whole team on what to do next, ask yourself this: if we set up an experiment and measure improvements to some metric, do we actually know what we want to measure, especially given long-tailed distributions?

Additionally, consider the acceptable tolerance that your team has with these systems. Instead of asking if the experiment will or won't work, focus on laying out thresholds for metrics like precision and recall.

## Designing experiments and metrics

> All metrics are wrong, some are useful.

All of the effort spent deliberating on edge cases and long tails stems from the fact that **many junior devs are not actually thinking hard enough about what the experiment should be, and what the metrics should look like.**

The goal of building out these probabilistic software systems is not a milestone or a feature. Instead, what we're looking for are outcomes, measurements, and metrics that we can use to make decisions. We are not looking for some notion of test coverage. Instead, we're looking at the trade-offs between precision and recall, whether accuracy is a good metric for an imbalanced dataset, or whether we can improve our evaluations effectively under some other constraints.

Well, it is obviously important to deliberate over database schemas and API contracts early in the process. When we're building probabilistic systems like a recommendation system or a RAG application, it's very important to also focus on what kind of outcomes we're trying to drive. Even if we don't have some business outcome
(like churn or conversion), it's still valuable to have local, smaller, short-term outcomes like model accuracy or some LLM Evaluation and know that our goal is to prepare a suite of experiments in order to move and change this metric. Does model performance correlate with business outcomes? Maybe, maybe not. But at least we have a metric that we can use to drive decision-making.

!!! tip "Try to focus on what the experiment is going to be and which metric we're going to move and why those metrics are important in the first place. We want to improve AUC because it leads to conversion. We want to improve precision because it leads to a better user experience, and churn, etc."

## Make decisions, improve focus

Making decisions should not increase the scope of your project. Get into a habit of using these metrics to drive decision-making that cuts off other possibilities. **Once you've measured something, it should give you focus on your immediate next move.**

!!! note "Etymology of the word 'decision'"

    The word “decision” actually has Latin roots. The meaning of the word “decide” comes from the Latin word  _decidere_, which is a combination of two words: de = 'OFF' + caedere = 'CUT'.

Once you develop the habit of planning experiments that drive metric improvements, the next skill to focus on is recommending decisions and actions based on these metrics.

Consider this example: we, a group of data scientists, are analyzing the various types of queries received by a retrieval application. We've classified the queries using a classification model, and we've aggregated data to determine the volume and quality of each query type.

| Query                | Count | Quality |
| -------------------- | ----- | ------- |
| Personal Data        | 420   | 70%     |
| Scheduling Questions | 90    | 83%     |
| Internet Searches    | 20    | 9%      |

Here are some examples of recommendations that we can make based on this data:

1. Our performance in internet searches is clearly underwhelming, but the count is quite low.
2. In the meantime, we can disable this feature, knowing that it won't significantly impact our users.
3. Personal data queries have a very high volume, but the quality is lacking.
4. We should focus on building experiments that improve the quality of personal data queries.
5. Since we can't run a backtest on users thumbs up and thumbs down ratings, we should consider a different metric like embedding reranking scores
6. If we can show that changing our retrieval system can improve re-ranking scores, we should go and verify whether or not re-ranking scores correlate with quality and be able to iterate confidently knowing that we might be able to improve the final outcome.

## Negative results are still results

We're not in academia. A negative result is still a result. The goal isn't to publish novel research, the goal is to figure out how to prioritize our limited resources. Remember that to make a decision is to cut off. If we get a negative result or a neutral result, then the outcome is the same, we have made a decision. We have made a decision to cut off this line of inquiry, maybe not forever, but at least for now.

That being said, it's also important to trust your judgment. Even if you're going to cut off a line of reasoning for now, it's still good to write up a little memo to explain what happened and write down other things you may not have considered, keeping this key question in mind: _"Under what conditions would we revisit this line of inquiry?"_

## Final Takeaways

Many people transitioning from classical software engineering to machine learning are often surprised by the empirical nature of the results we obtain. Instead of executing discrete unit tests, we sample from the distribution of potential inputs and build a internal model of how this system operates.

I hope that this article has helped you understand the importance of focusing on outcomes, metrics, and experiments instead of trying to think our way through edge cases and long tails. Additionally, I encourage you to develop the habit of making decisions and eliminating other possibilities. Lastly, I hope you will cultivate the practice of documenting your results and sharing them with your team, fostering a collective learning experience.

As you're building these probabilistic systems, ask yourself:

1. Could an experiment just answer my questions?
2. What specific improvements am I measuring?
3. How will the result help me make a decision?
4. Under what conditions will I reevaluate if results are not positive?
5. Can I use the results to update my mental model and plan future work?

## One more thing

This is a great point that a friend of mine called out. Set due dates for your experimentation. And if you cannot get a result by the due date, that is the result. **Write that down, explain why it takes longer than we expected, and move on.** For now, that is the negative result.
