---
title: "Two Experiments We Need to Run on AI Agent Compaction"
description: "If in-context learning is gradient descent, then compaction is momentum. Here are two research directions that could transform how we understand and optimize agentic systems."
date: 2025-08-30
slug: "context-engineering-compaction"
tags:
  - Context Engineering
  - Agents
  - Research
  - Compaction
---

# What Experiments Should We Run on AI Agent Compaction?

**Two core insights:**

1. If in-context learning is gradient descent, then compaction is momentum.
2. We can use compaction as a compression system to understand how agents actually behave at scale.

_This is part of the [Context Engineering series](./context-engineering-index.md). I'm focusing on compaction because it's where theory meets practice—and where we desperately need empirical research._

<!-- more -->

Through my [consulting work](https://jxnl.co/services/), I help companies build better AI systems and I've been thinking about compaction and how it connects to the research showing that [in-context learning is gradient descent](https://arxiv.org/abs/2212.07677). This theoretical foundation provides a framework for understanding how context management affects agent learning trajectories. If that's true, then compaction is basically a momentum term. And if compaction is momentum, there are two experiments I desperately want to see someone run.

This builds on the foundational concepts I've explored in [context engineering](./context-engineering-tool-response.md), where the structure of information flow becomes as critical as the information itself.

## What Do These Compaction Terms Mean?

**Compaction**: Automatic summarization of conversation history when context windows approach limits, preserving essential information while freeing memory space.

**Agent Trajectory**: The complete sequence of tool calls, reasoning steps, and responses an agent takes to complete a task. (basically the message array)

**Context Pollution**: When valuable reasoning context gets flooded with irrelevant information, degrading agent performance. I've written extensively about how this affects AI systems in [my analysis of slash commands versus subagents](./context-engineering-slash-commands-subagents.md).

**Momentum**: In gradient descent optimization, a component that accelerates convergence by incorporating the direction of previous updates to smooth out oscillations.

<!-- more -->

## Why Is Compaction Like Momentum?

Traditional gradient descent with momentum:

```
θ_{t+1} = θ_t - α∇L(θ_t) + β(θ_t - θ_{t-1})
```

Conversational learning with compaction:

```
context_{new} = compact(context_full) + β(learning_trajectory)
```

Compaction isn't just storing facts—it's preserving the _learned optimization path_. When you compact "I tried X, it failed, then Y worked because Z," you're maintaining the gradient direction that led to success.

This got me thinking: what if we could actually test this? What if we could run experiments that treat compaction as momentum and see what happens?

## Experiment 1: Compaction as Momentum for Long-Running Tasks

The first experiment is about momentum. If compaction preserves learning trajectories, then timing should matter for success rates.

**The setup**: Run million-token agent trajectories on complex coding tasks. Test compaction at 50% vs 75% completion vs natural boundaries vs agent-controlled timing.

**The problem**: Public benchmarks generally run tasks that are very short and don't burn 700,000 tokens. You need those massive trajectories that only companies like Cursor, Claude Code, or GitHub actually have access to.

**A practical workaround**: The [rapid prototyping methodology](./context-engineering-agent-prototyping.md) using Claude Code lets you generate long trajectories for testing. Complex multi-step tasks naturally burn through context as they iterate on tool calls and file modifications. You can study compaction behavior in these prototyping sessions before building production systems.

This connects to broader challenges in [AI engineering communication](./ai-engineering-communication.md)—how do you measure and report progress on systems where the unit of work isn't a feature but a learning trajectory?

But we do have examples of long trajectories. Take the [Claude plays Pokemon](https://www.lesswrong.com/posts/HyD3khBjnBhvsp8Gb/so-how-well-is-claude-playing-pokemon) experiment—it generates "enormous amounts of conversation history, far exceeding Claude's 200k context window," so they use sophisticated summarization when the conversation history exceeds limits. That's exactly the kind of trajectory where compaction timing would matter.

**Key Metrics**:

- Task completion success rate
- Time to completion
- Number of backtracking steps after compaction
- Quality of final deliverable

**Research Questions**:

- Does compaction timing affect success rates?
- Can agents learn to self-compact at optimal moments?
- How does compaction quality correlate with momentum preservation?

Does compaction timing affect how well agents maintain their learning trajectory? Can agents learn to self-compact at optimal moments?

## Experiment 2: Compaction for Trajectory Observability and Population-Level Analysis

The second experiment is more tractable: can we use specialized compaction prompts to understand what's actually happening in agent trajectories?

Basically, design different compaction prompts for different kinds of analysis:

**1. Failure Mode Detection**

```
Compact this trajectory focusing on: loops, linter conflicts,
recently-deleted code recreation, subprocess errors, and user frustration signals.
```

**2. Language Switching Analysis**

```
Compact focusing on: language transitions, framework switches,
cross-language debugging, and polyglot development patterns.
```

**3. User Feedback Clustering**

```
Compact emphasizing: correction requests, preference statements,
workflow interruptions, and satisfaction indicators.
```

### What Do We Expect to Discover?

I suspect we'd find things like:

- 6% of coding trajectories get stuck with linters (I see this constantly in Cursor)
- A bunch of agents recreate code that was just deleted
- Excessive subprocess cycling when language servers act up
- Patterns around when users start giving lots of corrective feedback

These failure modes mirror the [common anti-patterns in RAG systems](./rag-anti-patterns-skylar.md) but at the trajectory level rather than the retrieval level.

Here's why this matters: [Clio](https://www.anthropic.com/research/clio) found that 10% of Claude conversations are coding-related, which probably influenced building Claude Code. But agent trajectories are totally different from chat conversations. What patterns would we find if we did Clio-style analysis specifically on agent behavior?

This type of systematic analysis aligns with the [data flywheel approaches](./data-flywheel.md) that help AI systems improve through user feedback loops—but applied to multi-step reasoning rather than single predictions.

### How Would the Clustering Approach Work?

1. **Compact trajectories** using specialized prompts
2. **Cluster compacted summaries** using embedding similarity
3. **Identify patterns** across user bases and use cases
4. **Build diagnostic tools** for common failure modes

This is trajectory-level observability. Instead of just knowing "agents do coding tasks," we could understand "agents get stuck in linter loops" or "agents perform better when users give feedback in this specific way."

It's similar to the systematic improvement approaches I cover in [RAG system optimization](./rag-flywheel.md), but focused on agent behavior patterns rather than search relevance.

## What Infrastructure Is Missing?

Context windows keep getting bigger, but we still hit limits on complex tasks. More importantly, we have no systematic understanding of how agents actually learn and fail over long interactions.

This connects to fundamental questions about [how AI engineering teams should run standups](./ai-engineering-standup.md)—when your "product" is a learning system, traditional software metrics don't capture what matters.

Companies building agents could figure out why some trajectories work and others don't. Researchers could connect theory to practice. The field could move beyond single-turn benchmarks toward understanding actual agentic learning.

## How Do We Get Started?

The momentum experiment realistically needs a company already running coding agents at scale. The observability experiment could work for anyone with substantial agent usage data.

Both need access to long trajectories and willingness to run controlled experiments.

## Who Should Collaborate on This?

If you're working with agents at scale and want to explore these directions, [I'd love to collaborate](https://jxnl.co/services/). These sit at the intersection of ML theory and practical deployment—exactly where the most interesting problems live.

The future isn't just about better models. It's about understanding how agents actually learn and optimize over time. Compaction might be the key.

---

\_This post is part of the [Context Engineering Series](./context-engineering-index.md). For foundational concepts, start with [Beyond Chunks: Context Engineering Tool Response](./context-engineering-tool-response.md). To understand how context pollution affects agent performance, read [Slash Commands vs Subagents](./context-engineering-slash-commands-subagents.md).

For related concepts on AI system evaluation and improvement, explore [RAG system optimization techniques](./rag-flywheel.md) and [systematic approaches to AI monitoring](./systematically-improving-rag-raindrop.md).\_
