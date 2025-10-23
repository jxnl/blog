---
title: "How Extend Achieves 95%+ Document Automation (Lessons from Eli Badgio)"
speaker: Eli Badgio, Extend
cohort: 3
description: Insights from Eli Badgio, CTO of Extend, on mapping document workflows, building task-specific evaluations, and implementing partial automation with human-in-the-loop approaches for 95%+ extraction accuracy.
tags: [document automation, extraction, human-in-the-loop, evaluation, Extend, workflow]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# How Extend Achieves 95%+ Document Automation (Lessons from Eli Badgio)

I hosted a special session with Eli Badgio, CTO of Extend, to discuss AI-native document processing in the cloud. Extend helps companies achieve 95%+ extraction accuracy for customers like Brex and other Fortune 500s. This session covered mapping document workflows, building task-specific evaluations, and implementing partial automation with human-in-the-loop approaches.

<!-- more -->

[▶️ Learn How Extend Hits 95%+ Accuracy](https://maven.com/p/da0487){: .md-button .md-button--primary}

## What are the key challenges in document automation?

Document processing is an incredibly broad field, from ingestion (RAG context for agents, data mining) to back-office processing (where documents are systems of record) to in-product experiences (traditional OCR).

The most common failure case is companies trying to "one-shot" automation—attempting to replace an entire manual process with AI in a single step. This almost never works, even when extraction accuracy seems high in initial tests.

> "In practice, it will never work, even if the use case is not that complex and the accuracy on the extraction is going to be close to perfect. It's extraordinarily difficult to just swap out a manual process for an automated process." — Eli Badgio

This one-shot approach sets unrealistic expectations for business stakeholders and product teams. Instead, successful document automation requires a more methodical, step-by-step approach.

**Key Takeaway:** Don't try to replace entire document workflows in one go. Start with partial automation and gradually expand as you build confidence in the system and gain stakeholder buy-in.

## How should companies approach understanding their document data?

The first critical step is developing a deep understanding of both your documents and the existing manual processes around them. In most companies, there's an enormous amount of tacit knowledge hidden in people's heads—whether in engineering, operations, or domain experts.

One client Extend worked with took a fascinating approach to this challenge. They were trying to automate software contract ingestion but initially struggled with accuracy issues. Their solution was four-fold:

- Implemented a human-in-the-loop flow where AI-processed documents were still routed to humans for verification, allowing them to collect robust production data
- Brought in domain experts from within the company who had previously done this work manually
- Created a series of extractors that characterized normalized attributes (supplier, layout type, pricing terminology) rather than trying to extract actionable data
- Ran this workflow on approximately 150,000-200,000 documents (nearly a million pages) to develop an accurate representation of their historical data

This approach allowed them to identify blind spots in their understanding—problematic suppliers, pricing terms that weren't being extracted correctly, and document types they weren't properly accounting for.

> "Take some kind of initial first pass that is entirely focused on understanding the data, not actually trying to get the data out." — Eli Badgio

**Key Takeaway:** Invest time in understanding your documents and existing processes before attempting automation. Consider running a data characterization phase where you classify document attributes to identify patterns and edge cases.

## Why are task-specific evaluations critical for document automation?

Generic benchmarks like "Gemini Flash is better than GPT-X" aren't particularly useful for document automation. What matters is how well a system performs on your specific documents and use cases.

A healthcare vertical AI team Extend worked with discovered this when automating EHR entry of referral orders. They were dealing with 100+ page scanned PDFs containing multiple referrals mixed with patient history and provider notes.

Their solution was to have their AI engineers collaborate directly with in-house nurses and medical technicians to build comprehensive, fine-grained evaluation sets across a variety of document examples. The domain experts helped optimize schemas and extraction rules to properly interpret medical jargon.

This approach created a competitive advantage—proprietary evaluation data that allowed them to quickly test new models and capabilities against their specific needs. They maintained this advantage by continuing to review a percentage of documents to understand how real-world production data changes over time.

> "You really need to invest the evals at every step of a flow when you're trying to automate an end-to-end document process." — Eli Badgio

**Key Takeaway:** Create detailed, domain-specific evaluation sets with help from subject matter experts. These evaluations should test each step of your pipeline and reflect the real-world complexity of your documents.

## How should companies think about partial automation versus full automation?

Rather than aiming for 100% automation from the start, successful companies focus on what Eli called "true automation rate"—how high of an accuracy can you get where the end-to-end pipeline works 100% of the time, and inaccuracies are caught 100% of the time?

A dental billing automation company took this approach when processing explanation of benefits (EOB) documents. They implemented:

- A multi-step process that segmented the problem, limiting what each module needed to handle
- Configuration workflows for different providers with known edge cases
- Data validations and guardrails that could declaratively identify when a document needed human review

This approach recognized that 85% true automation (where you know with certainty which 15% need human review) is more valuable than 98% accuracy where you can't identify the problematic 2%.

> "In most cases, for these critical systems of records ingestion use cases, that's strictly worse than if you can get to like 85% true automation rate, where the 15% of the time that's not going to properly handle the document, you can catch that declaratively." — Eli Badgio

**Key Takeaway:** Focus on "automate when possible, augment otherwise" rather than full automation. Design systems that can confidently identify which documents need human review rather than trying to automate everything.

## How should companies redesign processes around automation?

Rather than trying to replicate existing manual processes with automation, successful implementations rethink the entire workflow with automation in mind.

This might involve:

- Breaking document processing into multiple pipeline steps (parsing, classification, splitting, extraction, semantic chunking)
- Creating declarative validation rules to identify when automation might fail
- Designing human-in-the-loop workflows that efficiently handle exceptions

When working with clients, Extend often starts by asking them to walk through their current process end-to-end. This helps identify opportunities to redesign workflows rather than simply automating existing inefficient processes.

> "It can be very difficult to just full swap out something that's been done over many years among many different stakeholders and just make that automated as opposed to really understanding as an engineer what is the end-to-end process." — Eli Badgio

**Key Takeaway:** Don't try to replicate manual processes with automation. Instead, redesign workflows from first principles with automation in mind, focusing on validation and exception handling.

## How should companies balance cost, speed, and accuracy in document processing?

Document processing involves multiple trade-offs between cost, speed, and accuracy. For back-office workflows, accuracy should generally take priority over speed.

Eli recommended several approaches to manage these trade-offs:

- Use model distillation to create smaller, faster models for specific tasks like chunking
- Implement pre-filtering steps with lightweight classifiers to avoid running expensive operations on all documents
- For back-office flows, design processes that remove latency as a consideration

> "If it's a back-office flow, I would encourage everyone not to think about latency as a problem. In fact, you should think about designing a process where you can effectively remove latency as being a consideration." — Eli Badgio

He also noted that deterministic code-based approaches are often preferable to LLM-based solutions for certain extraction tasks:

> "If you can solve it with code... you should do the code-based approach because then you can actually guarantee it's going to behave how you want." — Eli Badgio

**Key Takeaway:** For back-office document processing, prioritize accuracy over speed. Use lightweight models for initial classification and filtering, and consider deterministic code-based approaches where possible to reduce uncertainty.

## What role should domain experts play in document automation?

One of the most overlooked aspects of document automation is the critical role of domain experts. These are the people who understand the tacit knowledge embedded in documents and processes—nurses who know how to interpret medical terminology, financial analysts who understand billing codes, or operations staff who have been processing these documents manually.

Eli emphasized that involving these experts early in the process creates a significant competitive advantage:

> "If you're an engineer and you're tasked with this kind of problem... and you don't feel like you actually understand this process, someone on your team has to. If you're doing this currently and you're in industry, someone understands this." — Eli Badgio

The most successful implementations Extend has seen involve close collaboration between AI engineers and domain experts to:

- Design appropriate schemas and extraction rules
- Create comprehensive evaluation datasets
- Develop validation rules to identify edge cases
- Interpret domain-specific terminology and formats

**Key Takeaway:** Involve domain experts early in your document automation projects. Their tacit knowledge is essential for understanding document semantics, designing appropriate schemas, and creating effective evaluation datasets.

## How should companies approach change management for document automation?

Implementing document automation requires careful change management. Eli recommends starting with augmentation rather than full automation:

> "Most companies are much more willing to roll something out and deal with the change management if you focus on augmentation at start and then turn augmentation into automation." — Eli Badgio

When working with clients, Extend often leads with building a human-in-the-loop system first, allowing companies to:

- Collect real-world data about their documents
- Build confidence in the system gradually
- Identify edge cases and failure modes
- Manage stakeholder expectations

This approach aligns with their mantra: "Automate when possible, augment otherwise."

**Key Takeaway:** Start with augmentation rather than full automation to ease change management. Build human-in-the-loop systems that gradually increase automation levels as confidence grows.

## Final thoughts on document automation

Document automation is a complex field that requires deep understanding of both technical capabilities and domain-specific knowledge. The most successful implementations I've seen follow these principles:

- Understand your data and existing manual processes thoroughly
- Invest early in tailored evaluations specific to your domain
- Break processing into multiple pipeline steps
- Don't aim for 100% automation initially
- Redesign processes around automation rather than trying to replicate manual workflows

As AI capabilities continue to advance, the companies that will benefit most are those that take a thoughtful, systematic approach to document automation rather than rushing to replace human processes overnight.

---

## FAQs

**What is document automation and why is it important?**

Document automation uses AI to process and extract information from documents, reducing manual effort and errors. This is particularly crucial for enterprises where manual document workflows consume significant resources. For example, a single building construction project can require processing a million documents. Effective document automation can achieve 95%+ extraction accuracy, streamlining operations across industries from finance to healthcare.

**What are the main types of document processing use cases?**

There are three broad categories of document processing:

- Ingestion: Including RAG context for agents and data mining
- Back office processing: When documents serve as systems of record (contracts, deeds, etc.)
- In-product experiences: Traditional OCR use cases like uploading an invoice to extract data

The most challenging and often overlooked category is back office processing, where documents serve as critical systems of record with zero tolerance for errors.

**What's the most common mistake when implementing document automation?**

The most common failure is attempting to "one-shot" the automation—trying to replace an entire manual process with automation in a single step. This approach almost never works, even for relatively simple use cases. It sets unrealistic expectations and doesn't account for the complex change management required when transitioning from manual to automated processes.

**How should I approach understanding my document data?**

Take time to thoroughly understand both your documents and the existing manual processes around them. Many companies have enormous amounts of tacit knowledge hidden in people's heads—whether in engineering, operations, or domain experts. This knowledge is critical for successful automation.

One effective approach is to implement a human-in-the-loop flow where AI-processed documents are still routed to humans for review. This helps collect robust production data separate from your evaluation sets. Also consider creating extractors that characterize normalized attributes of your documents (supplier types, layout patterns, terminology variations) to help cluster and understand your document landscape.

**Why are tailored evaluations so important for document automation?**

Generic benchmarks don't translate well to specific document automation tasks. You need evaluations tailored to your domain, data, and processes. Invest early in creating comprehensive, fine-grained evaluation sets across a variety of document examples.

The best approach is to involve domain experts (like nurses for healthcare documents or billing specialists for financial documents) to help build robust evaluation sets and optimize extraction schemas. This creates a competitive advantage as you can quickly test and confidently roll out improvements when new models become available.

**Should I aim for 100% automation from the start?**

No. It's much more effective to start with partial automation and gradually increase automation rates. Focus on what's called the "true automation rate"—not just accuracy on extracted data, but how often the end-to-end pipeline works perfectly and you can catch errors 100% of the time.

For example, a system with 85% true automation rate where you can reliably identify the 15% that needs human review is far better than a system with 98% accuracy but no way to identify which 2% contains errors.

**How should I think about redesigning processes for automation?**

Rather than trying to create a one-to-one replacement of an existing manual process, rethink the process from scratch with automation in mind. This might involve:

- Breaking complex workflows into multiple steps
- Creating deterministic routing based on document classifications
- Implementing validation checks and guardrails
- Designing human review processes for edge cases

When possible, design the process around asynchronous processing rather than optimizing for latency, especially for back-office workflows where accuracy is more important than speed.

**How can I reduce costs for document processing?**

Several strategies can help manage costs:

- Use model distillation to create smaller, faster models for specific tasks
- Implement lightweight classifiers as an initial step to route documents appropriately
- Use pre-filtering to only apply expensive processing (like semantic chunking) to documents that require it
- Break processing into multiple steps with specialized models for each task

For back-office workflows, prioritize accuracy over latency and design processes that accommodate asynchronous processing.

**How should I involve domain experts in document automation?**

Domain experts are crucial for successful document automation. Involve them in:

- Tailoring classifications and schema design to match industry jargon
- Building comprehensive evaluation sets
- Optimizing extraction rules to properly interpret domain-specific terminology
- Designing validation checks based on their knowledge of the data

Teams that effectively incorporate domain experts gain a significant competitive advantage in document automation.

**What's the best way to start automating a document workflow?**

Start by identifying a single, high-priority use case rather than attempting to automate multiple workflows simultaneously. Focus on understanding the data and existing process thoroughly before designing automation.

Consider these steps:

- Implement a human-in-the-loop flow to collect production data
- Involve domain experts to understand tacit knowledge
- Create robust evaluation sets for each step in the process
- Start with augmentation before moving to automation
- Design the process around automation rather than trying to replicate the manual process

This approach delivers business value faster while building organizational comfort with automation.

---

--8<--
"snippets/enrollment-button.md"
--8<--

---
