---
title: Why Your AI Is Failing in Production (Ben & Sidhant)
speakers: [Ben Hylak, Sidhant Bendre]
cohort: 3
description: AI monitoring, production testing, and data analysis frameworks for identifying issues in AI systems and implementing structured monitoring.
tags: [monitoring, evaluation, production, AI systems, debugging]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Why Your AI Is Failing in Production (Ben & Sidhant)

I hosted a lightning lesson featuring Ben from Raindrop and Sid from Oleve to discuss AI monitoring, production testing, and data analysis frameworks. This session explored how to effectively identify issues in AI systems, implement structured monitoring, and develop frameworks for improving AI products based on real user data.

<!-- more -->

[▶️ Get the Production Monitoring Playbook](https://maven.com/p/285276){: .md-button .md-button--primary}

## What are the fundamentals of AI monitoring and why are traditional approaches insufficient?

The foundation of AI monitoring begins with evals, which function similarly to unit tests in traditional software development. An eval consists of an input (either a single message or conversation) and an expected output from the model.

While evals are useful for offline testing, they have significant limitations when applied to production environments:

"The naive solution that people reach for is to run evals on some small percentage of production traffic," Ben explained. "But this can be extremely expensive, especially if you're using larger models as judges."

Beyond cost concerns, there are deeper issues with relying solely on LLM judges for evaluation:

- They're difficult to set up accurately and require detailed definitions of what constitutes "good" or "bad" performance
- They only evaluate what you already know to look for, missing novel failure modes
- They struggle to identify emerging problem patterns

I've seen this challenge firsthand with clients who implement sophisticated eval systems but still miss critical issues that only emerge in production. The fundamental problem is that in AI applications, unlike traditional software, there's often no exception being thrown when something goes wrong - the model simply produces an inadequate response.

**Key Takeaway:** Traditional error monitoring tools like Sentry don't work for AI products because there's no explicit error message when an AI system fails. Instead, we need specialized approaches that can identify problematic patterns in model outputs and user interactions.

## How do we effectively identify issues in AI systems?

Ben introduced what he calls "the anatomy of an AI issue," which consists of two main components: signals and intents.

Signals come in two varieties:

1. Implicit signals - Signs from the data itself that something is wrong:

- User frustration ("Wait, no, you should be able to do that")
- Task failures (when the model says it can't do something)
- NSFW content (users trying to hack the system)
- Laziness (model not completing requested tasks)
- Forgetting (model losing context of previous interactions)

2. Explicit signals - Trackable user actions that indicate satisfaction or dissatisfaction:

- Thumbs up/down ratings
- Regeneration requests (suggesting the first response was inadequate)
- Search abandonment
- Code errors (especially valuable for coding assistants)
- Content copying or sharing (positive signals)

"You really need this sort of constant IV of your app's data," Ben emphasized. "There's nothing right now where you can just hit 'go' and the thing is going to constantly improve itself for your customers. That tool doesn't exist yet."

For smaller applications with fewer than 500 daily events, Ben recommends piping every user interaction into a Slack channel where you can manually review them. This helps you discover not just where the model is wrong, but what's confusing about your product and what features users expect but don't yet exist.

**_Key Takeaway:_** Effective AI monitoring requires tracking both implicit signals (patterns in user and model language that suggest problems) and explicit signals (user actions that indicate satisfaction or dissatisfaction), then exploring these signals to identify recurring issues.

## What framework can help organize and prioritize AI improvements?

Sid introduced the Trellis framework (Targeted Refinement of Emergent LLM Intelligence through Structured Segmentation), which his team at Oleve uses to manage AI products that reach millions of users within weeks of launch.

The framework has three core axioms:

1. Discretization - Converting the infinite plane of possible AI outputs into specific, mutually exclusive buckets (like "math homework help" or "history assignment assistance")

1. Prioritization - Scoring mechanisms to rank which buckets matter most based on metrics like sentiment, conversion, retention, and strategic priorities

1. Recursive refinement - Continuously organizing within buckets to find more structure within the chaos of outputs

"The idea in general with Trellis is to break down your infinite output space into mutually exclusive buckets, figure out what buckets matter to you, and keep recurring down until you've solved your entire space of what matters for your users," Sid explained.

The implementation follows six steps:

1. Initialize your output space by launching a minimal but generally capable MVP

1. Cluster user interactions by specific intents

1. Convert clusters into semi-deterministic workflows

1. Prioritize workflows based on company KPIs

1. Analyze workflows to discover sub-intents or misclassified intents

1. Recursively apply the process to refine each workflow

For prioritization, Sid recommends going beyond simple volume metrics: "A very naive approach is pretty much volume only... This could generally be useful, but it can be misleading if you're getting a lot of traffic on something you're already good at."

Instead, he suggests a formula: Volume × Negative Sentiment × Achievable Delta × Strategic Relevance. This helps identify areas where improvements will have the greatest impact with reasonable effort.

**_Key Takeaway:_** The Trellis framework provides a structured approach to taming the chaos of AI outputs by categorizing user intents, creating specialized workflows for each intent, and prioritizing improvements based on a combination of volume, sentiment, achievability, and strategic importance.

## How can we fix issues once we've identified them?

Once you've identified and categorized issues, Ben outlined several approaches to fixing them:

1. Prompt changes - Often the first and simplest solution

1. Offloading to tools - Routing problematic intents to specialized tools or more capable models

1. RAG pipeline adjustments - Modifying storage, memory descriptions, or retrieval methods

1. Fine-tuning - Using identified issues as training data for model improvements

Sid shared a real example from Oleve's product Unstuck, where they noticed recurring alerts from Raindrop about summary quality issues. Because they had already organized their product around the Trellis framework, they knew exactly which workflow needed improvement.

"We decided to prioritize that. The good thing is, we had summaries already aligned to our summarize workflow, so we knew it was just one workflow to fix instead of a bunch of others," Sid explained.

After implementing changes, they saw an immediate decrease in alerts and received direct user feedback confirming the improvement: "One of my co-founders got a text from one of our users who said that whatever I pushed the night before had suddenly helped him get better summaries for his Spanish class."

This case study demonstrates the value of having "self-contained, blameable pieces of your infrastructure" that allow you to identify, isolate, and fix specific issues without affecting the entire system.

**_Key Takeaway:_** Fixing AI issues requires a portfolio of approaches from simple prompt changes to sophisticated fine-tuning. The key is having a structured system that allows you to attribute problems to specific workflows and measure the impact of your improvements.

## What are some notable examples of AI failures in production?

Ben shared several examples of high-profile AI failures that traditional testing might have missed:

- Virgin Money's chatbot threatening users because they kept using the word "Virgin" (the company's name)
- Grok responding to unrelated questions with statements about "white genocide in South Africa"
- Google Gemini Cloud Console misinterpreting basic questions about account credits
- OpenAI's model encouraging harmful user behaviors after being optimized too heavily on user preferences

What's particularly telling is OpenAI's admission that "our evals didn't catch it" and their statement that "evals won't catch everything. Real world use helps us spot problems and understand what matters most to users."

These examples highlight why production monitoring is essential - the real world introduces edge cases and user behaviors that even the most comprehensive testing regimes will miss.

**_Key Takeaway:_** Even the largest AI companies with sophisticated testing infrastructure experience unexpected failures in production. This underscores the importance of robust monitoring systems that can detect novel issues as they emerge in real-world usage.

## How long does it take to implement effective AI monitoring?

When I asked Sid about the timeline for implementing the Trellis framework, he described a gradual process that began before public launch:

"We launched it to a private beta of people like a month and a half before our public launch. This was about 10 to 15 students out in NYU."

They integrated Raindrop on day one of their public launch, which then tracked their growth from a few thousand users in the first week to 500,000 by the first month, and then a million the month after.

The process of refining their workflows and monitoring was continuous: "For those first few months it was a lot of me just looking at the data, understanding what made sense, understanding if we're routing to the right workflows, understanding if we had the right clusters, and then tuning those workflows."

Sid noted that they only reached stability about four months after launch: "We only really started hitting stability towards December. But it was a continuous loop in terms of looking at data, trying things out, looking at data, trying things out."

**_Key Takeaway:_** Implementing effective AI monitoring is not a one-time setup but an iterative process that begins before launch and continues throughout a product's lifecycle. Even with sophisticated tools, the human element of analyzing data and refining systems remains essential.

## What unexpected insights can emerge from AI monitoring?

One of the most valuable aspects of comprehensive monitoring is discovering unexpected user behaviors that wouldn't be apparent otherwise.

Sid shared an interesting example from Unstuck: "Even though we have a side pane with a transcript available to you when you upload a lecture, for some reason people still wanted the transcript in chat."

This insight revealed that users wanted to engage with transcripts differently than the team had anticipated, despite having built what they thought was an intuitive interface for accessing this information.

I've had similar experiences with clients whose products suddenly went viral in unexpected regions: "We'll launch a product and all of a sudden our evals start struggling, and then we come back and say, 'Oh, we just went viral in Turkey, and a lot of our prompts are in English.'"

These types of insights are nearly impossible to anticipate through traditional testing but become immediately apparent with proper monitoring systems.

**_Key Takeaway:_** Comprehensive AI monitoring often reveals unexpected user behaviors and preferences that wouldn't be discovered through traditional testing. These insights can drive product improvements that better align with how users actually interact with your system.

## How do we ultimately make AI products better?

When I asked what question we should have covered, Ben highlighted the fundamental challenge: "How do you actually make things better? Is it just changing a word in a prompt? Is it actually fine-tuning something? What is the actual tool that's going to make your product better?"

The answer varies significantly depending on the specific product and issue. As I explained, it's about having a portfolio of tools at your disposal:

"People are asking, 'Do we build agents? Should we use RAG?' But really it's about having a portfolio of tools at your disposal. Are there tools that are underutilized? Are there tools that are not performant? Are there tools that need to be expanded? Or are they just tools that don't exist that we need to invest in?"

Effective monitoring and analysis frameworks like those presented by Ben and Sid allow teams to inspect this portfolio and make better decisions about resource allocation and technical investments.

**Key Takeaway:** There's no one-size-fits-all solution for improving AI products. Success requires a diverse toolkit of approaches, from prompt engineering to fine-tuning, combined with monitoring systems that help you determine which tools will have the greatest impact on your specific challenges.

---

FAQs

## What are evals in AI monitoring?

Evals are similar to unit tests in traditional software engineering. They consist of an input (either a single message or an entire conversation) and an expected output from the model. Evals can provide a binary pass/fail result or a score, and they're primarily used for offline testing to iterate on prompts and ensure your AI system performs as expected.

## How do offline evals differ from production monitoring?

Offline evals are run locally or in CI/CD pipelines to test specific scenarios and prevent regressions. They're useful for iterating on prompts and ensuring changes don't break existing functionality. Production monitoring, however, involves analyzing real user interactions to identify issues that may not have been anticipated during development, providing insights into how your AI system performs in the real world.

## What are LLM judges and why should I be cautious about them?

LLM judges are language models used to evaluate outputs from other models. While they can be useful for assessing subjective qualities (like whether a joke is funny), they can be misleading if not set up properly. The main concerns are that they're expensive to run at scale, difficult to configure accurately, and may not detect novel problems outside their evaluation criteria. It's best to use LLM judges sparingly and primarily for binary decisions with well-defined conditions.

## What signals should I look for to identify AI issues in production?

There are two types of signals to monitor: implicit and explicit. Implicit signals come from the data itself, such as user frustration expressions, task failures, or NSFW content. Explicit signals are actions users take that indicate satisfaction or dissatisfaction, like thumbs up/down, regenerating responses, abandoning searches, or copying/sharing content. Both types of signals help identify patterns of issues in your AI system.

## How can I effectively explore and categorize AI issues?

Start by breaking down issues by metadata (like browser type, model used, or user plan) to identify patterns. Analyze keywords associated with problematic interactions and examine the intersection of user intents and issue types. Use tools like semantic search to find similar issues and cluster them. This exploration helps you understand the scope and impact of different problems.

## Why is it important to maintain a constant flow of production data?

Without continuous monitoring of production data, you'll miss emerging issues and user frustration patterns. For high-volume applications, use tools that summarize patterns and notify you of significant issues. For lower-volume applications (less than 500 events daily), consider reviewing every user interaction to understand what's confusing about your product and what features users expect but don't yet exist.

## What is the Trellis framework?

Trellis (Targeted Refinement of Emergent LLM Intelligence through Structured Segmentation) is an operating framework for designing reliable AI experiences. It helps organize the "infinite chaos" of AI outputs into controllable, structured segments so you can prioritize engineering efforts on what matters most. The framework has three core axioms: discretization, prioritization, and recursive refinement.

## How do I implement the Trellis framework?

Start by launching a minimal viable product to gather real user interactions. Cluster these interactions by intent, then convert the clusters into semi-deterministic workflows with an intent router that directs user requests to the appropriate workflow. Prioritize workflows based on metrics relevant to your business goals, then recursively analyze each workflow to identify sub-intents or misclassified intents that could become new workflows.

## How should I prioritize which AI issues to fix first?

While volume (how many users experience an issue) is important, it shouldn't be your only consideration. A more effective approach is to multiply volume by negative sentiment score and then by an estimated achievable delta (how much you can realistically improve the experience). This helps you focus on issues that affect many users, cause significant frustration, and can be fixed relatively easily.

## What are the main approaches to fixing issues in AI systems?

There are several approaches to improving AI performance: prompt changes (usually the first and simplest solution), offloading problematic intents to more capable models or specialized tools, improving your RAG (Retrieval-Augmented Generation) pipeline for memory-related issues, and fine-tuning models using supervised or reinforcement learning techniques based on the ground truth signals you've collected.

## Why is it important to make AI improvements attributable and testable?

When building AI systems, you want your improvements to be engineered, repeatable, testable, and attributable—not accidental. By organizing your system into discrete workflows, you can identify exactly which component is causing an issue and fix it without affecting other parts of the system. This makes your improvements more reliable and your system easier to maintain.

## How can I validate that my AI improvements are working?

Monitor your system before and after making changes to see if the frequency of related issues decreases. Look for positive user feedback that specifically mentions the improved experience. The most reliable validation comes from seeing a measurable reduction in the issues you were targeting, combined with positive user sentiment about the specific improvements you made.

---

--8<--
"snippets/enrollment-button.md"
--8<--

---
