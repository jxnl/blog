---
title: Why Grep Beat Embeddings in Our SWE-Bench Agent (Lessons from Augment)
speaker: Colin Flaherty
cohort: 3
description: Insights from Colin Flaherty on building autonomous coding agents and how agentic approaches reshape retrieval-augmented generation systems.
tags: [RAG, agents, autonomous coding, agentic systems, retrieval]
date: 2025-09-11
categories: [Speaker Series, RAG, Coding Agent Series]
---

# Why Grep Beat Embeddings in Our SWE-Bench Agent (Lessons from Augment)

I hosted Colin Flaherty, previously a founding engineer at Augment and co-author of Meta's Cicero AI, to discuss autonomous coding agents and retrieval systems. This session explores how agentic approaches are transforming traditional RAG systems, what we can learn from state-of-the-art coding agents, and how these insights might apply to other domains.

<!-- more -->

[▶️ See How Grep Beat Complex Embeddings](https://maven.com/p/5f4d74){: .md-button .md-button--primary}

## Do agents make traditional RAG obsolete?

Colin shared his experience building an agent for SWE-Bench Verified, a canonical AI coding evaluation where agents implement code changes based on problem descriptions. His team's agent reached the top of the leaderboard with a surprising discovery: embedding-based retrieval wasn't the bottleneck they expected.

"We explored adding various embedding-based retrieval tools, but found that for SweeBench tasks this was not the bottleneck - grep and find were sufficient," Colin explained. This initially surprised him, as he expected embedding models to be significantly more powerful.

The evolution of code retrieval complexity has followed a clear progression:

- 2023 (Completions): Simple retrieval with low latency requirements
- 2024 (Chatbots): More complex retrieval across multiple files
- 2025 (Agents): Highly complex retrieval across many parts of codebases

When examining how the agent solved problems, Colin observed it would use simple tools like grep and find persistently, trying different approaches until it found what it needed. The agent's persistence effectively compensated for less sophisticated tools.

**_Key Takeaway:_** Agents don't necessarily make traditional RAG obsolete, but they change how we should think about retrieval systems. The persistence and course-correction capabilities of agents can sometimes overcome limitations in the underlying retrieval tools.

**Benefits of agentic retrieval with simple tools**
Agentic retrieval with grep and find offers several advantages:

1. Iterative retrieval becomes much simpler - instead of complex multi-step embedding processes, agents can simply run multiple searches and refine as they go
2. Token budget management is straightforward - when the agent hits token limits, it can simply truncate old tool calls and rerun them if needed
3. Implementation is low-effort - no need to maintain vector databases, syncing mechanisms, or other infrastructure
4. Course correction happens naturally - if one search approach fails, the agent tries another

However, these simple approaches have clear limitations:

- They don't scale well to large codebases
- They struggle with unstructured natural language content
- They're relatively slow and expensive compared to optimized embedding lookups

The best approach might be combining both worlds - an agentic loop with access to high-quality embedding models as tools.

**How to architect retrieval systems for different needs**
When deciding between traditional RAG, agent+grep/find, or agent+embeddings, Colin recommends considering several factors:

- Quality: How good is the final output?
- Latency: How quickly does the system respond?
- Cost: What are the computational expenses?
- Reliability: Does the system correct itself when it fails?
- Scalability: How well does it handle large indices?
- Maintenance effort: How much engineering work is required?

Traditional RAG offers decent quality with excellent speed, low cost, and high scalability, but lacks course correction. Agent+grep provides excellent quality and reliability but struggles with speed, cost, and scale. Agent+embeddings combines the best of both but remains slow and expensive.

**_Key Takeaway:_** Don't throw away your existing retrieval systems - instead, expose them as tools to agents. This gives you the benefits of both approaches while allowing you to optimize based on your specific constraints. For implementation guidance, see the [Context Engineering approach to tool response design](../context-engineering-tool-response.md), which shows how to structure tool outputs to give agents better peripheral vision of the information landscape.

**Evaluating agentic retrieval systems**
Colin emphasized a "vibe-first" approach to evaluation:

"Start with 5-10 examples and do end-to-end vibe checks before moving to quantitative evaluation. With natural language systems, you can learn so much just from looking at a few examples."

He noted that improving embedding models doesn't necessarily improve end-to-end performance because agents are persistent - they'll eventually find what they need even with suboptimal tools. This makes traditional embedding evaluation metrics less useful for agentic systems.

For those starting from scratch, Colin recommends:

1. Build the simplest possible retrieval tool
2. Put an agent loop on top
3. Iterate based on what causes the most pain for users
4. Only move to quantitative evaluation once you've addressed obvious issues

I found it refreshing that Colin focused on specific examples of queries rather than abstract discussions of model architectures. As he put it, "Being a researcher is actually very similar to being a product person - you're working backwards from use cases and examples."

**When to use embedding models vs. simple search tools**
While grep and find worked well for SWE-Bench's relatively small codebases, Colin identified several scenarios where embedding models become essential:

1. Searching large codebases
2. Retrieving from unstructured content like Slack messages or documentation
3. Searching across third-party code that models haven't memorized
4. Retrieving from non-text media like video recordings of user sessions

"If I was a human working on this use case, and I was a really persistent human that never got tired, would having this other search tool help me? If the answer is yes, then it's probably going to be useful for the agent."

Colin noted that SWE-Bench is somewhat artificial - its repositories are smaller than real-world codebases, and 90% of its problems take less than an hour for a good engineer to solve. In more complex environments, embedding models become increasingly valuable.

**Improving agentic retrieval systems**
To enhance agentic retrieval, Colin recommends:

1. Adding re-rankers to embedding tools to improve precision and reduce token usage
2. Training specialized embedding models for different tasks (e.g., one for code, another for Slack messages)
3. Prompt-tuning tool schemas to guide agents toward efficient usage patterns
4. Creating hierarchical retrieval systems that summarize files and directories
5. Leveraging language server protocols as additional tools

One particularly effective technique is asynchronous pre-processing: "I've taken songs and used an LLM to create a dossier about each one. This simple pre-processing step took a totally non-working search system and turned it into something that works really well."

## Why aren't more people training great embedding models?

When asked what question people aren't asking enough, Colin highlighted the lack of expertise in training embedding models: "Very few people understand how to build and train good retrieval systems. It just confuses me why no one knows how to fine-tune really good embedding models."

He attributed this partly to the specialized nature of the skill and partly to data availability. For code, there's abundant data on GitHub, but most domains lack comparable resources. Additionally, the most talented engineers often prefer working on LLMs rather than embedding models.

**_Key Takeaway:_** As agents become more capable, the quality of their tools becomes increasingly important. Even though agents can compensate for suboptimal tools through persistence, providing them with better retrieval mechanisms significantly improves their efficiency and capabilities.

**Final thoughts on the future of retrieval**
Colin believes we're entering an era where the boundaries between traditional RAG and agentic systems are blurring. The ideal approach combines the strengths of both: the speed and efficiency of well-tuned embedding models with the persistence and course-correction of agents.

As these systems evolve, we'll likely see more specialized tools emerging for different retrieval contexts, along with more sophisticated pre-processing techniques that make retrieval more effective. The key is focusing on the specific problems you're trying to solve rather than getting caught up in architectural debates.

"Agents are getting radically smarter, but even Einstein preferred writing on paper instead of a stone tablet," Colin noted. "Yes, these agents are persistent, but you should give them whatever you can to improve the odds that they find what they're looking for."

---

**FAQs**

## What is agentic retrieval and how does it differ from traditional RAG?

Agentic retrieval is an approach where AI agents use tools like grep, find, or embedding models to search through code and other content. Unlike traditional RAG (Retrieval-Augmented Generation), which typically uses embedding databases and vector searches, agentic retrieval gives the agent direct control over the search process. This allows the agent to be persistent, try multiple search strategies, and course-correct when initial attempts fail. Traditional RAG is more rigid but can be faster and more efficient for certain use cases.

## Do agents make traditional RAG obsolete?

No, agents don't make traditional RAG obsolete—they complement it. The best approach is often to build agentic retrieval on top of your existing retrieval system by exposing your embedding models and search capabilities as tools that an agent can use. This combines the strengths of both approaches: the persistence and flexibility of agents with the efficiency and scalability of well-tuned embedding models.

## What are the benefits of using grep and find tools with agents?

Using simple tools like grep and find with agents offers several advantages:

- Iterative retrieval becomes much easier as agents can refine searches based on previous results
- Token budget management is simpler since old tool calls can be truncated and rerun if needed
- The system is easier to build and maintain without complex vector database dependencies
- Agents can course-correct when searches don't yield useful results by trying different approaches

## What are the limitations of using grep and find for retrieval?

While grep and find work well for certain scenarios, they have significant limitations:

- They don't scale well to very large codebases (millions of files)
- They're ineffective for searching through unstructured natural language content
- They work best with highly structured content like code that contains distinctive keywords
- They can be slower than optimized embedding-based searches for large datasets

## What's the ideal approach to retrieval for coding agents?

The best approach is often a hybrid system that combines:

1. An agentic loop that gives the agent control over the search process
2. Access to multiple search tools including grep, find, and embedding-based search
3. The ability to choose the most appropriate tool based on the specific search task
4. Course correction capabilities when initial searches don't yield useful results

## How should I evaluate agentic retrieval systems?

Start with a qualitative "vibe check" using 5-10 examples to understand how the system performs. Observe the agent's behavior, identify patterns in successes and failures, and develop an intuition for where improvements are needed. Only after this initial assessment should you move to quantitative end-to-end evaluations or specific evaluations of individual components like embedding tools. Remember that improving a single component (like an embedding model) may not necessarily improve the end-to-end performance if the agent is already persistent enough to overcome limitations.

## I already built a retrieval system with custom-trained embedding models. Should I replace it with agentic retrieval?

No, don't replace it—enhance it. Build agentic retrieval on top of your existing system by exposing your embedding models and search capabilities as tools that an agent can use. This gives you the best of both worlds: the quality and efficiency of your custom embeddings plus the persistence and flexibility of an agent.

## How can I improve my agentic retrieval system?

Focus on building better tools for your agent:

- Add re-rankers to your embedding tools to improve precision and reduce token usage
- Train different embedding models for different specific tasks
- Prompt-tune your tool schemas to help the agent use them effectively
- Consider hierarchical retrieval approaches like creating summaries of files or directories
- Add specialized tools for specific retrieval tasks (like searching commit history)

## How do memories work with agentic retrieval systems?

Memories in agentic systems can be implemented by adding tools that save and read memories. These memories can serve as a semantic cache that speeds up future searches by storing information about the codebase structure, relevant interfaces, or other insights gained during previous searches. This can significantly improve performance on similar tasks in the future.

## Why did embedding models not improve performance on SWE-Bench?

For the SWE-Bench coding evaluation, embedding models didn't significantly improve performance because:

1. The repositories were relatively small, making grep and find sufficient
2. The code was highly structured with distinctive keywords that made text-based search effective
3. The agent's persistence compensated for less sophisticated search tools
4. The tasks were relatively simple, typically solvable by a good engineer in under an hour

## This doesn't mean embedding models aren't valuable—they become essential for larger codebases, less structured content, or more complex retrieval tasks.

--8<--
"snippets/enrollment-button.md"
--8<--

---
