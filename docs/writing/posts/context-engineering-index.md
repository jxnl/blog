---
title: "Context Engineering Series: Building Better Agentic RAG Systems"
description: "A comprehensive guide to moving beyond chunks toward structured tool responses that teach agents how to navigate data landscapes. Learn from real implementations across coding agents and enterprise systems."
date: 2025-08-28
slug: "context-engineering-index"
tags:
  - Context Engineering
  - Agents
  - RAG
  - Series
---

# Context Engineering Series for Agentic RAG Systems?

I've been helping companies build agentic RAG systems and studying coding agents from Cognition, Claude Code, Cursor, and others. These coding agents are probably unlocking a trillion-dollar industry—making them the most economically viable agents to date.

This series shares what I've learned from these teams and conversations with professional developers using these systems daily, exploring what we can apply to other industries.

!!! info "Related Series"
    **[Coding Agents Speaker Series](./coding-series-index.md)**: Deep insights from the teams behind leading coding agents including Cognition (Devin), Sourcegraph (Amp), Cline, and Augment. While this Context Engineering series focuses on technical implementation patterns, the Speaker Series reveals strategic insights and architectural decisions.
    
    **[RAG Master Series](./rag-series-index.md)**: Comprehensive guide to building and scaling retrieval-augmented generation systems. Context Engineering principles directly enhance RAG implementations—structured tool responses and faceted search are foundational RAG optimization techniques.

<!-- more -->

## What is Context Engineering?

We've moved far beyond prompt engineering. Now we're designing portfolios of tools (directory listing, file editing, web search), slash commands like `/pr-create` that inject prompts, specialized subagents such as `@pr-creation-agent`, and instruction files like `AGENT.md` that work across IDEs, command lines, GitHub, and Slack.

Context engineering is designing tool responses and interaction patterns that give agents situational awareness to navigate complex information spaces effectively.

To understand what this means practically, let's look at how systems have evolved:

## What Key Terms Should I Know?

- Context Engineering: Designing tool responses and interaction patterns that teach agents how to navigate data landscapes, not just consume chunks.
- Faceted Search: Returning metadata aggregations (counts, categories) alongside results so agents can refine queries strategically.
- Agent Peripheral Vision: Structured hints about the broader information space beyond top‑k results.
- Tool Response as Prompt Engineering: Using structure (XML/JSON), metadata, and inline system instructions in tool outputs to shape future behavior.
- Context Pollution: Noisy, low-signal outputs (logs, traces) that crowd out useful reasoning context.
- Context Rot: Reliability degrading as conversations get longer and messier.
- Subagents: Specialized sidecar agents that do token-heavy, messy reads in isolation and return distilled summaries.
- Compaction: Summarizing conversation history to preserve essential trajectory while freeing context; treated as “momentum” in this series.
- Agent Trajectory: The full sequence of tool calls, steps, and messages that accomplish a task.
- Form Factors: Chatbots (conversational), workflows (side‑effect engines), and research artifacts (reports/tables).
- MCP (Model Context Protocol): A protocol for reusable tools across clients; best when reuse and client diversity justify the overhead.
- RAG: Retrieval‑augmented generation; here, evolved from chunks to structured, faceted information landscapes.

**Before:** We precomputed what chunks needed to be put into context, injected them, and then asked the system to reason about the chunks. Search was a one-shot operation—you got your top-k results and that was it.

```python
def search(query: str, n_chunks: int = 10) -> list[str]:
    """Return raw text chunks, no metadata."""
    chunks = vector_search(query, top_k=n_chunks)
    return [chunk.text for chunk in chunks]

# One-shot RAG pattern
def answer_question(question: str) -> str:
    chunks = search(question)
    context = "\n".join(chunks)
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can answer questions about the context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content
```

**Now:** Agents are incredibly easy to build because all you need is a messages array and a bunch of tools. They're persistent, make multiple tool calls, and build understanding across conversations. They don't just need the right chunk—they need to understand the landscape of available information.

```python
from pydantic import BaseModel

class SearchTool(BaseModel):
    """Search with metadata and facets for strategic exploration."""
    query: str
    n_chunks: int = 10
    
    def run(self) -> dict:
        results = vector_search(self.query, top_k=self.n_chunks)
        return {
            chunk.id: chunk.text for chunk in results
        }

# Agent loop - persistent conversation with tool execution
messages = [
    {"role": "system", "content": "Use search strategically to explore information landscapes."}
]

while True:
    response = client.chat.completions.create(
        messages=messages,
        tools=[SearchTool]
    )
    
    if response.tool_calls:
        # Execute tools and add results to conversation
        for tool_call in response.tool_calls:
            result = SearchTool(**tool_call.args).run()
            messages.append({"role": "tool", "content": str(result), "tool_call_id": tool_call.id})
    else:
        # Agent has final answer
        break
```

!!! tip "How Easy Are Agents to Build?"
    Coding agents have become remarkably simple to implement. Check out [How to Build an Agent](https://ampcode.com/how-to-build-an-agent) - if you give a coding agent literally just this blog post, it will write a coding agent for you. The barrier to entry has never been lower.

The fundamental shift is this: **agents don't just consume information, they explore information spaces**. Context engineering is about designing systems that support this exploration—giving agents not just the right data, but the right understanding of what data exists and how to navigate it.

<!-- more -->

## What Does This Series Cover?

This series explores practical approaches to context engineering across different domains and use cases. The focus is on implementation strategies, real-world examples, and measurable business outcomes from companies making this transition.

**Topics include:**

- Moving beyond chunks to structured information landscapes
- Multi-level response architectures that provide navigational context
- Agent-friendly data organization patterns
- Performance optimization for agentic workloads
- Business metrics and ROI measurement strategies

## What Posts Are in This Series?

### 1. [Beyond Chunks: Context Engineering Tool Response](./context-engineering-tool-response.md)

**Core thesis:** Agent success depends on tool response structure, not just content. Shows how faceted search and metadata give agents "peripheral vision" of data landscapes, enabling strategic exploration beyond top-k similarity results.

**Key insight:** Tool responses become prompt engineering—XML structure and system instructions in tool outputs directly influence how agents think about subsequent searches.

### 2. [Slash Commands vs Subagents: How to Keep AI Tools Focused](./context-engineering-slash-commands-subagents.md)

**Core thesis:** Context pollution is killing agent performance, but subagent architecture solves it. Bad context is cheap but toxic—100k lines of logs cost nothing computationally but destroy valuable reasoning context.

**Key insight:** Same diagnostic capability, dramatically different economics: slash commands flood main threads with 91% noise, subagents burn tokens off-thread and return 8x cleaner context with 76% signal.

### 3. [Two Experiments We Need to Run on AI Agent Compaction](./context-engineering-compaction.md)

**Core thesis:** If in-context learning is gradient descent, then compaction is momentum. We can use compaction as both an optimization technique and a lens for understanding agent behavior at scale.

**Key insight:** Compaction timing affects learning trajectory preservation, and specialized compaction prompts can reveal systematic patterns in agent failures and successes across populations.

### 4. [Context Engineering: Agent Frameworks and Form Factors](./context-engineering-agent-frameworks.md)

**Core thesis:** Agent success starts with choosing the right form factor—chatbot, workflow, or research artifact—and navigating the autonomy spectrum from deterministic systems to tool-calling loops.

**Key insight:** Teams fail because they don't commit to outcomes. The MCP decision matrix and autonomy spectrum provide clear frameworks for making architectural choices based on economic realities rather than hype.

### 5. [Context Engineering: Rapid Agent Prototyping](./context-engineering-agent-prototyping.md)

**Core thesis:** Most teams waste months building agent infrastructure before knowing if their idea works. Claude Code's project runner provides a faster path to evidence through folder-based testing and executable specifications.

**Key insight:** If Claude Code can't achieve your task with perfect tool access and no UI constraints, your production version probably won't either. Get one passing test before building any orchestration code.

**Start Here:** If you're new to context engineering, begin with the foundational post above, then explore agent frameworks and prototyping approaches.

## How Should I Use This Series?

- Quick Start: Audit your tool responses for sources and structure; add Level 2 (source metadata) immediately.
- Prototype: Use a CLAUDE.md + CLI tools + scenario checks to validate one task end‑to‑end before building orchestration.
- Isolate Noise: Keep test logs and heavy reads in subagents; return summaries to main thread.
- Measure: Track clarification rate, expert escalations, 504s, and resolution time before/after changes.
- Plan Compaction: Choose when and how to compact; test timing and prompts on long trajectories.

- Recommended Paths by Role:
  - Engineering: Tool Response → Rapid Prototyping → Slash vs Subagents → Compaction → Frameworks
  - Product/Leads: Frameworks → Rapid Prototyping → Tool Response → Slash vs Subagents
  - Researchers: Compaction → Tool Response → Slash vs Subagents → Rapid Prototyping

## Who Is This Series For?

- **Engineering teams** building agentic RAG systems
- **Product leaders** evaluating the ROI of agent implementations  
- **AI researchers** interested in tool design and agent cognition
- **Anyone** curious about how agents actually work with structured data

Each post includes practical code examples, implementation strategies, and real business metrics from companies that have made this transition.

## How Do I Get Started?

Start with the foundational post [Beyond Chunks: Why Context Engineering is the Future of RAG](./context-engineering-tool-response.md) to understand the core thesis and four-level framework. From there, you can either read sequentially or jump to specific topics based on your current implementation needs.

The future of RAG isn't about better embeddings or larger context windows—it's about teaching agents to navigate information spaces systematically. Let's explore how to build that future together.

## Want to Learn More?

I know this is a lot to absorb—context engineering touches everything from tool design to business metrics. I try to write down what I learn from consulting, but sometimes a more structured approach helps. If you're looking to implement these patterns systematically, I also do training and consulting:

[Free 6-Week RAG Email Course](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }
