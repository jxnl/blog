---
title: "10 Foot Guns in Fine-Tuning and Few-Shots"
description: "Common pitfalls in few-shot learning and how to avoid them."
date: 2025-01-22
categories:
  - Prompting
authors:
  - jxnl
  - cyrus
  - amir
comments: true
---

# 10 “Foot Guns" for Fine-Tuning and Few-Shots

Let me share a story that might sound familiar.

A few months back, I was helping a Series A startup with their LLM deployment. Their CTO pulled me aside and said, "Jason, we're burning through our OpenAI credits like crazy, and our responses are still inconsistent. We thought fine-tuning would solve everything, but now we're knee-deep in training data issues."

Fast forward to today, and I’ve been diving deep into these challenges as an advisor to Zenbase, a production level version of DSPY. We’re on a mission to help companies get the most out of their AI investments. Think of them as your AI optimization guides, they've been through the trenches, made the mistakes, and now we’re here to help you avoid them.

In this post, I’ll walk you through some of the biggest pitfalls. I’ll share real stories, practical solutions, and lessons learned from working with dozens of companies.

<!-- more -->

## Common "Foot Guns" in AI Experimentation

As you embark on optimizing your AI models, be aware of these common pitfalls that we’ve identified:

- Not aligning your LLM as a Judge
- Statistical testing and confidence that the improvements were real
- Wasting time and computations
- Smaller datasets for smaller models
- Overfitting and Misleading Accuracy
- API Rate Limits for finetuning
- Expensive API Calls
- Building out Experimental Harnesses
- Moving finetuning infra to open source models
- Managing Dynamic vs. Static Few-Shot Prompts
- Ensembling and Aggregating Results
- Systems Without Human Oversight
- Loss of Results Due to bad Implementations

These challenges can sometimes overlap, so I’ve consolidated and merged where it makes sense, focusing on the core issues and what you can do about them.

---

### 1. Misaligned Model Evaluation (Not aligning your LLM as a Judge)

**The Problem:**

Relying on an LLM as a "judge" without proper alignment leads to skewed evaluations. If your model’s internal judge doesn’t reflect human preferences, you’ll end up optimizing the wrong things. Then what ends up happening is building a system that is 80% or 90% accurate, doing experiments, and realizing that these things were just random noise to begin with.

**The Fix:**

Test your judging prompts against human feedback. Make sure that when the LLM says something is “good,” it aligns with what a human would say. You may need to refine criteria or include a human-in-the-loop step until the judge is trustworthy. It's a common practice and a big one. If you want to learn more, check out Hamel's post on [LLM Judges](https://hamel.dev/blog/posts/llm-judge/).

---

### 2. Missing Statistical Rigor (Statistical testing and confidence)

**The Problem:**

Running experiments only once and assuming the results are definitive is a fast track to chasing ghosts. You might see a supposed improvement that’s just a statistical fluke.

**The Fix:**

Run multiple trials. Use bootstrapping and significance tests to confirm that your improvement is real. This will ensure you’re not tweaking knobs based on random noise. So much of this has actually been lost as many software engineers are transitioning to AI engineering. Even Anthropic came out with a post on [statistical significance](https://www.anthropic.com/research/statistical-approach-to-model-evals)

---

### 3. Runaway Experiment Costs (Merging “Wasting time and computations” + “Expensive API Calls”)

**The Problem:**

Experimentation can quickly become a black hole for both time and money. Without caching results or pruning dead ends, you’ll find yourself buried under skyrocketing OpenAI bills and endless wait times. You'll be surprised how many times I've joined a team and realized that the test is a single `for` loop with no error handling. They'll come back to me and say, "Alright, I ran something for 20 minutes. We hit a rate limit and now I have to rerun the whole thing."

**The Fix:**

- Implement caching to avoid repeated calls.
- Start with a small subset of data for initial tests.
- Identify promising configurations before scaling up.

This approach keeps both your timeline and your budget under control. - Consider using something like a disk cache in Python to save intermediate results, theres so many ways to avoid this early and do it. I've seen at least 2-3 teams waste 1000s of dollars on OpenAI API calls just running experience where nothign chances, almost every modern evaluation framework has some sort of caching built in now. And if they don't have caching or parallelization, thats a red flag.

---

### 4. Data-Model Mismatch (Smaller datasets for smaller models)

**The Problem:**

Fine-tuning a large model on a tiny dataset or using a small model on a complex task is a quick way to get poor results. The model either overfits or fails to understand the task deeply enough.

**The Fix:**

Match the complexity of your data and the scope of your task to the model size. If you have limited data, consider using a smaller model or augmenting your dataset. If you have a rich, complex dataset, invest in a larger model and more thorough fine-tuning. We've even seen situations that show for thousands of examples in fine-tuning, you're going to get better results fine-tuning 4o-mini than 4o. This is due to the same reasons related to model capacity, how many parameters we need to update, etc. Additionally, if you only have 20 to 40 examples, these days you might be better off considering prompt caching too.

The key detail is that you should have a set of evaluations to determine which option is more-effective, rather than just guessing or formulating hypotheses. paying someone like me $1,000 just to tell you that it depends.

---

### 5. Illusory Gains (Overfitting and Misleading Accuracy)

**The Problem:**

Hitting 98% accuracy might feel great—until you realize the model just memorized the training set. High accuracy on a narrow slice of data doesn’t guarantee real-world performance. It is often not the case that you want an evaluation to be 100%. If it’s 100% right now, two things might happen:

- It might be too easy, and you won't be able to tell which model is better.
- When new models come out, you also won't be able to determine what’s better.

Lastly, you have not really understood or enumerated the failure modes that occur with real-world data.

**The Fix:**

Use separate validation and test sets. Continuously update your test sets with fresh, tough examples that represent real-world conditions. If something seems too good to be true, it probably is. Every machine learning intern has at least once come back to their manager with a model that has 99% accuracy just to realize that it was:

1. The wrong metric to use.
2. That it had somehow memorized the dataset or had data leakage.

This is no different than realizing that if you got 100% on an exam, you probably didn't learn anything.

---

### 6. Fine-Tuning Bottlenecks (API Rate Limits)

**The Problem:**

This is likely going to be the case if you're using the OpenAI fine-tuning API. API rate limits for fine-tuning can slow your entire operation. Hit the limit too soon, and you’re stuck waiting, losing valuable iteration cycles.

**The Fix:**

Plan your runs. Don’t fine-tune at every minor tweak. Batch updates and run fewer, more targeted experiments. If rate limits are truly blocking progress, consider negotiating higher quotas or exploring other providers. This is where Zenbase comes in, as they've managed to do most of that for you.

---

### 7. Infrastructure Overload (Building out Experimental Harnesses)

**The Problem:**

Without proper infrastructure, experiment management quickly becomes chaotic. Results get lost, configurations are forgotten, and comparing runs becomes impossible. Teams often start with basic logging, thinking it's sufficient. But as they scale, they realize they need test harnesses, UIs for result comparison, and deeper analysis tools. Soon they find themselves spending more time building infrastructure than running actual experiments. This infrastructure debt compounds, slowing down the entire experimentation process and making it harder to draw meaningful conclusions from their work.

**The Fix:**

Invest early in tooling. Use version control for prompts and code, automate logging and result aggregation, and maintain a consistent process for running and reviewing experiments. Think of it like setting up a proper kitchen before you start cooking complex dishes.

---

### 8. Vendor Lock and Migration Woes (Moving finetuning infra to open source models)

**The Problem:**

Transitioning from OpenAI’s models to open source options like Llama variants isn’t trivial. Your prompts, your evaluation frameworks, and even your data pipelines might need to be rethought. This happens as well with just moving between OpenAI, Anthropic, and Google models too. Small changes in the API can cause massive headaches. While larger frameworks provide other paints that come later on in the systems design process. Keep it simple, but not any simpler.

**The Fix:**

Build a lightweight flexible stack that can switch models without breaking. Use abstraction layers, standardize evaluation metrics, and keep dependencies on any single vendor minimal. This futureproofing will save you a massive headache down the road. Half the engagements I've seen are just trying to get a model to work, and then they're trying to figure out how to get it to work with their system.

---

### 9. Prompt Configuration Chaos (Managing Dynamic vs. Static Few-Shot Prompts)

**The Problem:**

Figuring out whether to use static few-shot examples or dynamically retrieved ones can consume weeks of trial and error. Without a systematic approach, you end up guessing.

**The Fix:**

Benchmark both approaches on a small but representative test set. Compare results and pick a strategy—or a hybrid approach—that best balances accuracy, cost, and complexity. Then standardize it. This is where I've seen the most confusion, and upside, but where someone like [Zenbase](https://zenbase.ai) can help you out.

---

### 10. Aggregation Anxiety (Ensembling and Aggregating Results)

**The Problem:**

When you run multiple models or try multiple prompt strategies, how do you combine the results? Without a plan, you’ll end up confused by contradictory signals. Most cases where result **really** matter, you're going to want to do some kind of ensembling or aggregation.

**The Fix:**

Define your aggregation methods upfront. Consider majority voting, weighted averages, or even a secondary judge model to break ties. Consistency in aggregation makes your results clearer and more actionable.

---

Every one of these foot guns can derail your projects, hike up your costs, and produce mediocre results. But you don’t have to navigate this maze alone. Its been fun collaborating with the teams at Zenbase, we've seen it all and distilled the lessons into proven strategies and best practices.

If you want us to double click on any of these topics reply or [email us](mailto:work+zenbase@jxnl.co) and we'll start writing more about specific topics that interest you.

[Email us](mailto:work+zenbase@jxnl.co){ .md-button .md-button--primary }
[Check out Zenbase](https://zenbase.ai){ .md-button .md-button--secondary }
