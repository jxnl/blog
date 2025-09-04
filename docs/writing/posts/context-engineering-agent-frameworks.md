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

# Context Engineering: Agent Frameworks and Form Factors

*This is part of the [Context Engineering Series](./context-engineering-index.md). I'm focusing on agent frameworks because understanding form factors and complexity levels is essential before building any agentic system.*

## Part I — What I actually talk about when companies say they want to build agents

*Field note from a conversation with [Vignesh Mohankumar](https://nila.is/), a successful consultant who helps companies navigate AI implementation decisions. [Vignesh](https://nila.is/) and I are both AI consultants helping companies build AI systems—he focuses on implementations and workflows, while I help with overall strategy and execution.*

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

* **Clear tool design.** Your system is limited by the tools you provide. Name functions clearly, define inputs and outputs precisely, and make error messages helpful.
* **Testing setup.** Test your concept quickly before building complex systems. Create a simple environment to try instructions with tools and verify outputs. One successful test proves the concept works.

Everything else is preference.

A practical question that comes up frequently: should you build custom tools or use MCP servers? The economics are more important than the technical architecture.

## The MCP Decision Matrix

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

## Part II — The autonomy spectrum (what we can safely automate, and how)

When leadership hears "agent," they imagine fully autonomous systems. That's not what works in practice. Successful systems follow a spectrum of increasing autonomy. Here's the progression I recommend:

### Step 0: Deterministic system (no AI)

Use traditional programming with if/else logic and clear rules. When inputs are predictable and tasks have one correct solution, code is cheaper, faster, and more reliable than AI. Use this approach when requirements are stable and inputs vary little.

### Step 1: The AI function

You control the workflow completely. Call the LLM like any other function: pass in data, get structured output back. Extract action items from transcripts, normalize addresses, classify documents. Test it like any dependency. No loops or complex logic—just a single AI call per task.

**Why it works:** Real-world data is messy. These functions clean it up so your code can handle it reliably.

### Step 2: The prompt chain

Chain multiple AI calls together when tasks need several steps: draft, then critique, then revise; or extract, then verify, then summarize. You still control the order completely. The AI handles each step, but you decide what comes next and when to stop.

**Common mistake:** Using chains for simple tasks that need only one AI call, or for complex tasks that need branching logic.

### Step 3: The graph state machine (Level **two**)

Here the workflow has multiple paths. You define specific states and transitions between them. The AI helps choose which path to take when the data isn't clear. For example: intake leads to triage, which leads to one of three different workflows, each with its own ending conditions.

**Key difference:** You recognize that requests are different and need different handling. You track the current state clearly instead of hiding it in prompts.

### Step 4: The tool-calling loop (Level **three**)

This is the classic "agent": a loop where the AI suggests an action, you execute it with a tool, add the result back to the conversation, and repeat until the task is complete. It's powerful but expensive and easy to get wrong. Use this for unusual cases that can't be handled with fixed workflows.

**How to control it:** Put the steps in your system prompt, tool descriptions, and error messages ("missing `user_id`; first call `lookup_user(email)`"). Set clear end conditions. Limit the number of tool calls. Track the cost.

This progression gives you a clear upgrade path. You don't need to start with the most complex option. Begin with deterministic code, add AI functions where you need flexibility, use chains when tasks have multiple steps, upgrade to graphs when workflows branch, and save the tool-calling loop for cases that truly need improvisation. This builds reliability step by step.

---

## Part III — "Show me, don't tell me." A conversation with Vignesh

[Vignesh](https://nila.is/) asked the key questions that every CTO has about agent reliability and cost. During our call, I showed him a working example: a simple prototype with clear tools and measurable results.

**Vignesh:** *Everyone says “build an agent,” and the diagrams always have a while-loop. In practice, how do you know it won’t wander? How do you get order without hard-coding order?*

**Jason:** I don't build the loop first. I set up a testing environment with clear instructions and well-named tools. The instructions describe the job and when it's complete. The tools explain what they need and what they return. Error messages guide the AI to the next step when something goes wrong.

**Vignesh:** *Okay, but does it do anything non-toy?*

**Jason:** I showed you a simple example with three tools. The goal: "Take a YouTube URL and create study notes." The tools download subtitles, clean up timestamps to save tokens, and format content into sections with bullet points. The instructions were clear: clean the transcript if needed, then read it, then write notes in the specified format, then stop when done.

**Vignesh:** *And on screen?*

**Jason:** You saw it handle the tricky part. The video didn't have English subtitles, which would break a rigid script. But the system adapted: it got what subtitles were available, cleaned them up, and still produced useful notes. It worked because we set a clear goal and gave it the right tools.

**Vignesh:** *You keep saying “harness.” Why not just wire an orchestrator and be done with it?*

**Jason:** The testing setup shows us if the idea works before we build complex systems. I create test folders with real URLs, run the project, and check if the output file has the right format—one title, three sections, ten bullets each. If it works once, we know it's possible. If it never works, we learn that quickly and cheaply.

**Vignesh:** *Where do you put the intelligence, then—in the model or in the tools?*

**Jason:** Both places, but differently. Tools define what's possible and how to use them. Instructions explain the goal and steps. Error messages teach the AI what to do next: "Missing `user_id`; first call `lookup_user(email)`." Good error messages guide the AI better than long prompts.

**Vignesh:** *And cost? Leaders will ask.*

**Jason:** Track it from the start. Testing shows you the real costs quickly: number of API calls, response time, success rate. If common tasks work reliably, write code for those and use AI for edge cases. If nothing is predictable, at least you know that before spending months building.

**Vignesh:** *So your rule of thumb?*

**Jason:** Use regular code when possible. Add AI functions for messy data. Chain AI calls for multi-step tasks. Use graphs when workflows branch. Save tool-calling loops for complex cases that need flexibility. Test everything quickly before building production systems.

---

## From Conversation to Prototype: The Fast Path

During our conversation, [Vignesh](https://nila.is/) and I explored a critical question that comes up in every agent consulting engagement: *How do you test whether an agent idea actually works without building all the infrastructure first?*

The answer turned into a complete methodology that I've extracted into its own guide: **[Context Engineering: Rapid Agent Prototyping](./context-engineering-agent-prototyping.md)**. 

**The core insight**: Use Claude Code's project runner as a testing harness. Write instructions in English, expose tools as simple CLI commands, create test folders with real inputs, and get evidence in hours instead of weeks.

This approach has saved multiple teams from months of premature infrastructure work. If you're being asked to "build agents," start there first—get one passing test before you write any orchestration code.

The methodology also integrates with all the other context engineering patterns: [tool response design](./context-engineering-tool-response.md), [slash commands vs subagents](./context-engineering-slash-commands-subagents.md), and [compaction behavior](./context-engineering-compaction.md). Prototyping reveals which patterns your specific use case actually needs.

--  -

## A note to leadership

Ask your team for specific results, not just "agents." Have them pick one of the three approaches—**chatbot**, **workflow**, or **report generator**—and define success. Ask where they'll start on the complexity spectrum and when they'd add more AI. 

Ask for a testing setup where they can try the idea with real data and measure results. If they can show one successful test, the concept works. If they can't, you know that before investing more time.

**Share this guide with your team before they start building. Understanding these approaches and complexity levels will save months of unnecessary work and help you focus on what's actually achievable.**
