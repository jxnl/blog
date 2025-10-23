---
title: "Context Engineering: Agent Frameworks and Form Factors"
description: "How to choose between chatbots, workflows, and research artifacts - and navigate the autonomy spectrum from deterministic systems to tool-calling loops"
date: 2025-09-04
authors:
  - jxnl
categories:
  - Applied AI
  - Software Engineering
tags:
  - Context Engineering
  - Agents
  - RAG
  - Series
---

# How Should We Choose Agent Frameworks and Form Factors?

_This is part of the [Context Engineering Series](./context-engineering-index.md). I'm focusing on agent frameworks because understanding form factors and complexity levels is essential before building any agentic system._

## What Do We Actually Mean When We Say We Want to Build Agents?

_Field note from a conversation with [Vignesh Mohankumar](https://nila.is/), a successful consultant who helps companies navigate AI implementation decisions. [Vignesh](https://nila.is/) and I are both AI consultants helping companies build AI systems—he focuses on implementations and workflows, while I help with overall strategy and execution._

When companies say they want to build agents, I focus on practical outcomes. What specific functionality do you need? What business value are you trying to create?

<!-- more -->

There are three main approaches that work for most companies:

### 1) The conversation interface (chatbots)

This is a chat interface that can access tools and APIs. A human oversees the conversation while the system suggests actions. Success means users get connected to the right functionality and can complete their tasks. Focus on tool integration, fast response times, and helping users find what they need quickly.

### 2) The side-effect engine (workflows)

This is automated workflow execution triggered by events. No user interface needed—contracts get sent, invoices get processed, tickets get updated. Success is measured by completion rate, accuracy, and processing time. The user experience is the audit trail showing what happened.

### 3) The research artifact (reports & tables)

This produces structured outputs like reports, summaries, or data tables. The system generates documents that follow a consistent format and meet quality standards. Success means the output is accurate, well-formatted, and ready to use in business contexts.

Choose one of these three approaches first. All other technical decisions—tool design, prompts, data processing, orchestration—depend on this choice. Don't try to build a chatbot that should be a workflow, or force a report generator to be conversational. Once you know what you're building, focus on two key areas:

- **Clear tool design.** Your system is limited by the tools you provide. Name functions clearly, define inputs and outputs precisely, and make error messages helpful.
- **Testing setup.** Test your concept quickly before building complex systems. Create a simple environment to try instructions with tools and verify outputs. One successful test proves the concept works.

Everything else is preference.

A practical question that comes up frequently: should you build custom tools or use MCP servers? The economics are more important than the technical architecture.

## When Should We Choose MCP?

MCP servers make sense when you need the same tools across multiple applications. If your team uses Claude Desktop, ChatGPT, and other AI platforms that all need Google Drive integration, an MCP server lets you build once and reuse everywhere.

However, MCP adds complexity. You're building protocol adapters, managing authentication across clients, and debugging connection issues. If you have tools that only one application will use, MCP is probably overkill. Direct API calls with the OpenAI SDK will be faster to implement.

The decision is straightforward. If your team already uses Claude Enterprise—which includes Google Drive, Atlassian, and calendar integrations—then adding four more APIs via MCP makes sense. You're extending an existing system, not building from scratch.

But if your team is using Ruby, or you're in an environment where MCP client libraries don't exist or are immature, you might spend more time on protocol plumbing than on the actual business logic. At that point, you're better off with direct API calls and a simple message loop.

**When to Choose MCP**

The decision comes down to a few concrete factors:

1. **Client diversity**: Are you serving multiple agent platforms, or just one application?
2. **Team standardization**: Does your organization already have MCP infrastructure, or are you starting from scratch?
3. **Tool complexity**: Are your tools simple CRUD operations, or do they involve complex authentication and state management?
4. **Headcount allocation**: Do you want to spend engineering time on protocol compliance, or on business logic?

If you're answering "multiple platforms," "existing infrastructure," "complex tools," and "protocol is fine," then MCP is probably worth the investment. Otherwise, start simple and upgrade when reuse pressure appears.

---

## How Does the Autonomy Spectrum Guide What We Automate?

When leadership hears "agent," they imagine fully autonomous systems. That's not what works in practice. Successful systems follow a spectrum of increasing autonomy. Here's the progression I recommend:

### Step 0: Deterministic system (no AI)

Use traditional programming with if/else logic and clear rules. When inputs are predictable and tasks have one correct solution, code is cheaper, faster, and more reliable than AI. Use this approach when requirements are stable and inputs vary little.

### Step 1: The AI function

You control the workflow completely. Call the LLM like any other function: pass in data, get structured output back. Extract action items from transcripts, normalize addresses, classify documents. Test it like any dependency. No loops or complex logic—just a single AI call per task.

**Why it works:** Real-world data is messy. These functions clean it up so your code can handle it reliably.

### Step 2: The prompt chain

Chain multiple AI calls together when tasks need several steps: draft, then critique, then revise; or extract, then verify, then summarize. You still control the order completely. The AI handles each step, but you decide what comes next and when to stop.

**Common mistake:** Using chains for simple tasks that need only one AI call, or for complex tasks that need branching logic.

### Step 3: The graph state machine

Here the workflow has multiple paths. You define specific states and transitions between them. The AI helps choose which path to take when the data isn't clear. For example: intake leads to triage, which leads to one of three different workflows, each with its own ending conditions.

**Key difference:** You recognize that requests are different and need different handling. You track the current state clearly instead of hiding it in prompts.

### Step 4: The tool-calling loop

This is the classic "agent": a loop where the AI suggests an action, you execute it with a tool, add the result back to the conversation, and repeat until the task is complete. It's powerful but expensive and easy to get wrong. Use this for unusual cases that can't be handled with fixed workflows.

**How to control it:** Put the steps in your system prompt, tool descriptions, and error messages ("missing `user_id`; first call `lookup_user(email)`"). Set clear end conditions. Limit the number of tool calls. Track the cost.

This progression gives you a clear upgrade path. You don't need to start with the most complex option. Begin with deterministic code, add AI functions where you need flexibility, use chains when tasks have multiple steps, upgrade to graphs when workflows branch, and save the tool-calling loop for cases that truly need improvisation. This builds reliability step by step.

## Why Is Every Level a Tool for Higher Levels?

Here's what makes this spectrum powerful: **any system at any level can become a tool for systems at higher levels**. A deterministic script becomes a tool for an AI function. An AI function becomes a tool for a prompt chain. A complete prompt chain becomes a tool for a graph state machine. Even an entire tool-calling agent can be a single tool in a larger orchestration system.

Think of it this way:

**Level 0 → Level 1**: Your AI function might call a deterministic validation script to check if extracted data meets business rules.

**Level 1 → Level 2**: Your prompt chain might use an AI function to classify documents, then route each document type to specialized processing.

**Level 2 → Level 3**: Your graph state machine might have states that are themselves complete prompt chains—one for intake processing, another for follow-up generation.

**Level 3 → Level 4**: Your tool-calling loop might have access to tools that are actually complete sub-agents, each handling specialized domains like "customer data research" or "contract generation."

This creates an architecture where simple, reliable components compose into more complex systems. The customer support agent that routes to password reset isn't calling a single API—it's calling a complete Level 2 chain that handles authentication, validation, and email generation. From the agent's perspective, it's just another tool.

### Why Does This Matter for Architecture?

**Testability**: Each level can be tested independently. Your Level 1 AI function works reliably before it becomes a tool in your Level 2 chain.

**Reliability**: Complex systems are built from proven components. If your document classification AI function has a 95% success rate, you can count on that when designing the higher-level system.

**Cost Control**: You can optimize each level separately. Maybe your Level 1 function is expensive but accurate, so you only call it after a cheap deterministic filter.

**Migration**: You can replace any level without changing the levels above it. Start with a simple deterministic tool, then upgrade it to an AI function when you need more flexibility—the calling system doesn't change.

**Team Structure**: Different teams can own different levels. The infrastructure team builds Level 0 tools, the AI team builds Level 1 functions, the product team composes them into Level 2 chains.

This is how you build agent systems that actually work in production: not as monolithic "intelligent" systems, but as compositions of focused, reliable components at different levels of autonomy.

---

## How Do We Go from Concept to Working System?

A critical question comes up in every agent consulting engagement: _How do you test whether an agent idea actually works without building all the infrastructure first?_

The answer turned into a complete methodology that I've extracted into its own guide: **[Context Engineering: Rapid Agent Prototyping](./context-engineering-agent-prototyping.md)**.

**The core insight**: Use Claude Code's project runner as a testing harness. Write instructions in English, expose tools as simple CLI commands, create test folders with real inputs, and get evidence in hours instead of weeks.

This approach has saved multiple teams from months of premature infrastructure work. If you're being asked to "build agents," start there first—get one passing test before you write any orchestration code.

The methodology also integrates with all the other context engineering patterns: [tool response design](./context-engineering-tool-response.md), [slash commands vs subagents](./context-engineering-slash-commands-subagents.md), and [compaction behavior](./context-engineering-compaction.md). Prototyping reveals which patterns your specific use case actually needs.

---

## What Should Leadership Ask For?

Ask your team for specific results, not just "agents." Have them pick one of the three approaches—**chatbot**, **workflow**, or **report generator**—and define success. Ask where they'll start on the complexity spectrum and when they'd add more AI.

Ask for a testing setup where they can try the idea with real data and measure results. If they can show one successful test, the concept works. If they can't, you know that before investing more time.

**Share this guide with your team before they start building. Understanding these approaches and complexity levels will save months of unnecessary work and help you focus on what's actually achievable.**
