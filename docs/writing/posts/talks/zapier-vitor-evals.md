---
title: "How Zapier 4x'd Their AI Feedback Collection (Vitor)"
speaker: Vitor
cohort: 3
description: "Vitor from Zapier shares how they dramatically improved their feedback collection systems for AI products through strategic UX changes and systematic analysis"
tags: [feedback systems, evaluation, user feedback, AI products, Zapier]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# How Zapier 4x'd Their AI Feedback Collection (Vitor)

I hosted a session with Vitor from Zapier to discuss how they dramatically improved their feedback collection systems for AI products. This conversation reveals practical strategies for gathering, analyzing, and implementing user feedback to create a continuous improvement cycle for RAG systems and AI applications.

<!-- more -->

[▶️ See How Zapier 4x'd Their Feedback](https://maven.com/p/ec1439){: .md-button .md-button--primary}

Zapier has been building numerous AI-powered features, with Zapier Central being their newest product - essentially an AI automation platform that connects with third-party apps and keeps data in sync. It functions as both a chat interface for your live data and an automation tool that can be controlled through natural language.

<!-- more -->

Initially, they faced a common challenge with AI products: limited feedback. Despite having users actively engaging with the product, their feedback submission rates were "abysmally low" - around 10 submissions per day. Even worse, the feedback they did receive was almost exclusively negative, coming from frustrated users experiencing errors.

The team realized they needed to be more aggressive and strategic about soliciting feedback. They made a seemingly small change that produced dramatic results - instead of using tiny, muted feedback buttons in the corner of the interface, they added a natural-looking chat message at the end of workflow tests that directly asked: "Did this run do what you expected it to do?"

This simple change, combined with larger, more visible thumbs-up and thumbs-down buttons, increased their feedback submissions from 10 to approximately 40 per day - a 4x improvement. Even more surprising was that they started receiving substantial positive feedback, which had been almost non-existent before.

**_Key Takeaway:_** The positioning, visibility, and wording of feedback requests dramatically impacts response rates. Being more direct and contextual with feedback requests can yield significantly more data, including the often-missing positive feedback that helps you understand what's working well.

## What strategies can you use to mine implicit feedback from user behavior?

Beyond explicit feedback buttons, Vitor shared several clever approaches for mining implicit feedback from user interactions:

1. Workflow activation signals: When a user tests a workflow and then activates it, that's a strong positive signal that the system is working as expected.
2. Tool call validation errors: If a tool call returns a validation error, it likely indicates the LLM made a mistake, which can be treated as negative feedback.
3. Follow-up message analysis: User follow-up messages often contain valuable signals - if they're rephrasing their question or expressing frustration, it suggests the previous response wasn't satisfactory.
4. Hallucination detection: By identifying common patterns in hallucinations (like phrases with "[you can replace]" in square brackets), they could mine for these specific failure cases.

The team implemented a nightly job that fetched runs from their database and analyzed them for these implicit feedback signals, providing additional data beyond what users explicitly submitted.

**_Key Takeaway:_** Look beyond explicit feedback mechanisms and mine your application data for implicit signals. User behaviors like activating workflows, rephrasing questions, or abandoning sessions can provide valuable insights about system performance without requiring direct user input.

## How did Zapier organize and scale their feedback analysis process?

With feedback volumes increasing dramatically, the team needed a systematic approach to process and learn from this data. They built an internal feedback triaging system where all submissions would land by default, providing staff with an optimized view of each run's details.

To scale beyond what one person could handle, they implemented "labeling parties" - weekly team meetings where everyone would review and categorize feedback submissions together. While initially slower than having one person process everything, these sessions built team members' confidence in labeling independently and fostered a "look at your data" mentality throughout the organization.

The team added extensive metadata to each submission, including tools used, context, and entry point (web app, Chrome extension, Slack). This allowed them to filter feedback by specific subsystems or contexts, making it easier for specialized teams to focus on relevant submissions.

From the triaging interface, staff could label feedback with categories corresponding to product capabilities, add notes about findings, and easily create evaluation tests directly from user interactions. This streamlined the process of turning real-world feedback into reproducible tests.

**_Key Takeaway:_** Creating structured processes for feedback analysis and involving the entire team builds a data-driven culture. Regular "labeling parties" not only distribute the workload but also ensure everyone understands user pain points and the value of examining raw data.

## How did feedback collection improve Zapier's product development process?

The improved feedback system transformed Zapier's product development in several ways:

1. Clearer prioritization: They could identify which capabilities were failing most frequently and cross-reference this with usage data to focus on high-traffic areas with low accuracy.
2. Targeted improvements: They discovered that their "AI Actions" tool, which translates natural language into API parameters, was failing in specific ways - like sending Slack DMs to random people instead of asking for clarification about the recipient.
3. Expanded evaluation coverage: They grew from 23 curated evaluations to 383 evaluations based on real user interactions, giving them much greater confidence when making system changes.
4. Better model selection decisions: When GPT-4.0 was released, they had enough evaluation data to determine that it actually regressed performance on some of their use cases, allowing them to delay adoption until they could address these issues with prompt tuning.

The team fed all their labeled data into their analytics platform (Databricks), allowing them to cross-reference feedback with product usage metrics and make more informed decisions about feature development.

**_Key Takeaway:_** A robust feedback system creates a flywheel effect - more feedback leads to better understanding of user needs, which enables more targeted improvements, resulting in better user experiences and ultimately more positive feedback.

## What were the key outcomes of Zapier's feedback improvement initiative?

The initiative produced several valuable outcomes beyond just the immediate product improvements:

1. Cultural shift: Everyone on the team now feels empowered to examine raw data and understands its value. Team discussions became more focused on improving specific capabilities rather than making vague statements about general improvements.
2. Improved decision-making: They could make more informed decisions about model upgrades, like waiting to adopt a new GPT-4.0 snapshot until they had addressed regressions in their evaluations.
3. Business metrics improvement: Activation and retention metrics began trending upward as the product improved based on feedback insights.
4. Positive feedback ratio: The ratio of positive to negative feedback submissions improved, indicating their changes were addressing user pain points.

The team is now looking to further automate their labeling process, potentially using LLM-as-judge approaches to draft initial categorizations for human review, continuing to make their feedback flywheel more efficient.

**_Key Takeaway:_** Investing in feedback systems pays dividends beyond immediate product improvements - it creates a data-driven culture, enables better decision-making, and ultimately drives business metrics like activation and retention.

## How important is the specific wording of feedback requests?

Vitor emphasized that the wording of feedback requests significantly impacts the quality of responses. Initially, they considered using generic language like "How did we do?" but after consulting with Jason, they opted for more specific phrasing: "Did this run do what you expected it to do?"

This specificity guided users toward providing feedback about the workflow's functionality rather than other aspects like speed or interface design. By focusing the question on their primary concern - whether the workflow performed the intended action - they received more actionable feedback.

Different contexts might require different feedback questions. For a RAG system handling complex multi-step workflows, functional correctness might be the priority, while other systems might need to focus on response quality, hallucination rates, or other metrics.

**_Key Takeaway:_** Craft feedback requests that specifically target the dimensions you care most about improving. Generic questions yield generic answers, while specific questions guide users toward providing the most valuable insights for your particular system.

## What's the value of turning feedback into formal evaluations?

Zapier emphasized the importance of converting user feedback into formal evaluations that could be run repeatedly. This approach provided several benefits:

1. Reproducibility: They could reliably test the same scenarios across different model versions or system changes.
2. Regression prevention: By capturing both successful and unsuccessful interactions, they could ensure new changes didn't break previously working functionality.
3. Targeted improvement: They could focus on specific failure modes and measure progress in addressing them.
4. Confidence in changes: With hundreds of evaluations based on real user interactions, they could confidently make system changes knowing they weren't introducing new problems.

The team built tooling to easily create evaluations from feedback submissions, including the ability to mock third-party API calls to simulate production conditions without making actual external requests.

**_Key Takeaway:_** Converting real-world feedback into formal evaluations creates a safety net for future development. This approach transforms one-time user experiences into persistent quality checks that protect against regressions and guide improvements.

## How does feedback collection fit into the broader AI product development cycle?

Vitor described a virtuous cycle for AI product development:

1. Start with a prototype using a strong foundational model
2. Create initial evaluations based on intuition or synthetic data
3. Ship to users and collect real-world feedback
4. Use that feedback to build more comprehensive evaluations
5. Improve the system based on these evaluations
6. Repeat the process, continuously refining both the product and evaluation suite

This cycle becomes particularly valuable when evaluating new model versions. When GPT-4.0 was released, Zapier's evaluation suite revealed that while many capabilities improved, some actually regressed - like the model's ability to recover from tool calls with invalid parameters. Without these evaluations, they might have blindly upgraded and introduced new problems.

## **_Key Takeaway:_** Feedback collection isn't just about fixing immediate issues - it's a critical component of a sustainable AI product development cycle. Each round of feedback strengthens your evaluation suite, which in turn enables more confident decision-making about system changes and model upgrades.

--8<--
"snippets/enrollment-button.md"
--8<--

---
