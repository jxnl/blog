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

*Field note from a conversation with [Vignesh Mohankumar](https://nila.is/), a successful consultant who helps companies navigate AI implementation decisions. Our discussion revealed the frameworks teams need before building any agentic system.*


## Part I — The talk I give when a team says, “We’re going to build agents.”

I don’t start with models. I don’t start with orchestration. I start with a simple, grounding question:

**What is the thing you want to exist in the world when this works?**

When teams answer honestly, the ambition collapses into one of three outcomes. Not architectures. Not hype objects. Outcomes. If we can agree on the outcome, the rest becomes engineering rather than myth-making.

### 1) The conversation interface (chatbots)

Sometimes the right answer is a conversational surface that can reach into tools. A place where a human supervises the loop and the system proposes the next best move. The success metric here is not “did we use the newest API,” it’s much plainer: did the user get routed to the right capability and leave with momentum? When chat is the surface, your job becomes instrumenting tool access, keeping latency human-grade, and making each response an act of triage that narrows uncertainty.

### 2) The side-effect engine (workflows)

Other times the right answer is not a surface at all—it’s a sequence that runs on triggers and produces work you can measure. No fanfare, no typing bubbles: a contract goes out, an invoice is posted, a ticket changes state. These systems live or die on three numbers: completion rate, correctness, and time-to-done. The user experience is the audit trail.

### 3) The research artifact (reports & tables)

And then there are days when the only thing that matters is an artifact you can hold up to the light—a standardized brief, a table of facts, a weekly research note. In that world, your user is future-you. You’ll judge yourself not by clever routing but by whether the artifact is consistent, legible, and structurally faithful to a spec. If the output can sit in a board packet without apology, the system is working.

That’s the topography. The rest of our choices—tool design, prompts, data plumbing, even whether we touch an orchestrator—flow downstream of which of these three you’re truly building. I don’t need twenty examples to make the point; I need you to pick one hill to plant a flag on. It will spare you from designing a chatbot that secretly wants to be a batch process, or from forcing a report generator to pretend it’s a concierge. Once we align on the outcome, we can get disciplined about two things that actually move the needle:

* **Tooling shape and clarity.** The system will only be as good as the verbs you give it. Name them like verbs, design their arguments like contracts, and make their errors teach the next step.
* **A harness for fast learning.** You don’t need to “build agents” to find out if the idea is viable. You need a place to try instructions against tools, produce an output, and assert on it. If you can get a pass even once, it’s possible. Then we decide whether it’s worth turning into steel.

Everything else is preference.

But before we climb the complexity ladder, there's a practical question that comes up in every conversation: should you build your own tools, or should you invest in MCP servers? The economics matter more than the architecture diagrams suggest.

## The MCP Decision Matrix

MCP servers make sense when you have **reuse pressure**—when the same tools need to serve multiple clients. If your team uses Claude Desktop, ChatGPT, and maybe a LangChain prototype, and they all need the same Google Drive integration, an MCP server centralizes that work. You build the server once, and three different clients can consume it.

But here's what the documentation doesn't tell you: MCP is overhead. You're not just building an API; you're building a protocol adapter, managing authentication across clients, and debugging connection issues that have nothing to do with your core business logic. If you have six tools that only your custom chatbot will ever use, you probably don't need MCP. A simple `for` loop with the OpenAI SDK will get you there faster.

The economic boundary is surprisingly sharp. If you told me you're building internal tools for a team that's already standardized on Claude Enterprise—which has Google Drive, Atlassian, and calendar integrations built in—then exposing four more APIs via MCP starts to make sense. You're not building the MCP client; you're just extending an existing ecosystem.

But if your team is using Ruby, or you're in an environment where MCP client libraries don't exist or are immature, you might spend more time on protocol plumbing than on the actual business logic. At that point, you're better off with direct API calls and a simple message loop.

**The Hidden Costs**

There's also a maintenance burden that's easy to underestimate. MCP servers need to handle authentication, rate limiting, error propagation, and versioning across multiple clients that may update at different cadences. If Claude Desktop updates its MCP client behavior, or if ChatGPT changes how it handles tool responses, you're suddenly debugging protocol mismatches instead of improving your agent.

Compare that to the alternative: if you're building a focused application with a known set of tools, you can wrap your APIs as simple functions, control the entire stack, and optimize for your specific use case. You lose the reuse benefit, but you gain predictability and debugging simplicity.

**When to Choose MCP**

The decision comes down to a few concrete factors:

1. **Client diversity**: Are you serving multiple agent platforms, or just one application?
2. **Team standardization**: Does your organization already have MCP infrastructure, or are you starting from scratch?
3. **Tool complexity**: Are your tools simple CRUD operations, or do they involve complex authentication and state management?
4. **Headcount allocation**: Do you want to spend engineering time on protocol compliance, or on business logic?

If you're answering "multiple platforms," "existing infrastructure," "complex tools," and "protocol is fine," then MCP is probably worth the investment. Otherwise, start simple and upgrade when reuse pressure appears.

---

## Part II — The autonomy spectrum (what we can safely automate, and how)

When leadership hears “agent,” they imagine a fully general intelligence. That’s not what ships. What ships is a careful climb up an autonomy ladder. Here’s the spectrum I use with teams—same staircase every time, same caution tape in the same places.

### Step 0: Deterministic system (no AI)

This is the world of rules and branches. If the input is well-behaved and the task has a single correct path, write code. It’s cheaper, faster, and easier to certify. Use this wherever stability is high and variance is low.

**Risk if skipped:** you’ll pay model tax to rediscover if-else.

### Step 1: The AI function

You still own the control flow. You call into an LLM the way you’d call into a library: **data in, structure out.** Extract action items from a transcript; normalize an address; classify a document. You wrap it in tests and treat it like a dependency. No loops. No magic. Just a sharp tool in a fixed slot.

**Why it exists:** reality is messy; these functions sand it down so your code can stay sane.

### Step 2: The prompt chain

Now you have a few steps that benefit from language in-between—draft, critique, revise; extract, verify, summarize. You still control the order. The model gives you leverage inside each step, but you decide what comes next and when you’re done. Think of it as a conveyor belt with clever stations.

**Failure mode:** using a chain where you needed a single function—or worse, a chain where you needed a graph.

### Step 3: The graph state machine (Level **two**)

At this level, the work genuinely branches. There are named states, explicit transitions, and the model helps pick the next state when the data is ambiguous. Intake might lead to triage; triage might lead to one of three specialized flows; each flow has its own exit criteria. You pilot the aircraft; the model calls headings in turbulence.

**What changes:** you no longer pretend every request is the same request, and you stop burying state inside prompts. You model it.

### Step 4: The tool-calling loop (Level **three**)

This is what most people picture when they say “agent”: a stateful loop where the model proposes an action, you perform it (call a tool), append the result, and continue until a success condition is met. It is powerful, expensive, and easy to misuse. It also unlocks the long tail—the odd cases where deterministic flows buckle and the world needs improvisation.

**How to keep it honest:** put the order-of-operations in three places—your system instruction, your tool descriptions, and your tool **errors** (“missing `user_id`; first call `lookup_user(email)`”). Give the loop a finish line it can see. Cap the number of tool calls. Measure the cost.

The spectrum matters because it gives you a migration path. You don’t have to start at Level Three to get value; in fact, you probably shouldn’t. Start with a deterministic backbone, add AI functions where variance is high, introduce a chain when language helps, upgrade to a graph when order genuinely branches, and reserve the tool-calling loop for the parts of your business where improvisation pays for itself. This is how you buy reliability with judgment rather than with hope.

---

## Part III — "Show me, don't tell me." A conversation with Vignesh

During our conversation, [Vignesh](https://nila.is/) asked the questions every CTO asks about agent reliability and economics. You couldn't see the screen during our call, so here's the moment that mattered, captured as it was: a quick, working prototype; no orchestrator; just a harness, a few tools, and a result we could argue about.

**Vignesh:** *Everyone says “build an agent,” and the diagrams always have a while-loop. In practice, how do you know it won’t wander? How do you get order without hard-coding order?*

**Jason:** I don’t start by building the loop. I start by giving the model a room to work in. In that room is a single document—the instruction—and a handful of tools with painfully clear names. The instruction describes the job and, crucially, the finish line. The tools describe their preconditions and what they return. And their error messages tell you the next step when you call them wrong. That’s my harness.

**Vignesh:** *Okay, but does it do anything non-toy?*

**Jason:** I showed you one that’s barely two pages of text and three tools. The goal was modest: “Given a YouTube URL, produce clean study notes.” The tools were wrappers around things we already understand: a downloader to fetch subtitles, a cleaner to strip timestamp chatter and shrink the token footprint, and a writer to turn content into a tight set of sections and bullets. The instruction said: if the transcript is bloated, clean first; then read; then write in this exact format; then stop when the file exists and matches the shape.

**Vignesh:** *And on screen?*

**Jason:** You watched it negotiate the messy part. The video didn’t offer default English subtitles. A brittle script would have died right there. In the harness, that’s not failure—that’s an opportunity to pivot. The downloader surfaced what it could; the cleaner reduced noise; the writer still had enough to structure useful notes. The loop wasn’t “creative”; it was disciplined. It moved toward the finish line because we’d drawn one.

**Vignesh:** *You keep saying “harness.” Why not just wire an orchestrator and be done with it?*

**Jason:** Because the harness tells us if the idea is possible without committing to a platform. I can create five test folders—each with a real URL in a `request.txt`—run the project, and assert on a single file: does `notes.md` exist with one title, three sections, ten bullets each? If it passes even once, I’ve learned enough to justify hardening. If it never passes, I’ve learned that faster and cheaper than any orchestrator could teach me.

**Vignesh:** *Where do you put the intelligence, then—in the model or in the tools?*

**Jason:** In both, but for different reasons. The tools carry **capability** and **contract**. The instruction carries **intent** and **order**. And the error strings carry **teaching**. A good tool error is worth a page of prompt engineering: “You’re missing `user_id`; first call `lookup_user(email)`.” That line is a rail for the loop. It’s how you nudge improvisation into choreography.

**Vignesh:** *And cost? Leaders will ask.*

**Jason:** Put it on the table early. The harness exposes the economics in hours, not quarters: how many tool calls, how much latency, how often we miss the finish line. If the hot path is stable, we freeze it into code and save the loop for the long tail. If the hot path isn’t stable, at least we know why—and we can decide whether the long tail is worth the spend.

**Vignesh:** *So your rule of thumb?*

**Jason:** If a deterministic system can do it, let it. If a single AI function can sand the edge off messy input, use it. If language between steps helps, chain. If order truly branches, model it as a graph. And if the job still resists, give it a loop with tools, a visible finish line, and errors that teach. Then prove it once in a harness before you build anything meant to last.

---

## From Conversation to Prototype: The Fast Path

During our conversation, [Vignesh](https://nila.is/) and I explored a critical question that comes up in every agent consulting engagement: *How do you test whether an agent idea actually works without building all the infrastructure first?*

The answer turned into a complete methodology that I've extracted into its own guide: **[Context Engineering: Rapid Agent Prototyping](./context-engineering-agent-prototyping.md)**. 

**The core insight**: Use Claude Code's project runner as a testing harness. Write instructions in English, expose tools as simple CLI commands, create test folders with real inputs, and get evidence in hours instead of weeks.

This approach has saved multiple teams from months of premature infrastructure work. If you're being asked to "build agents," start there first—get one passing test before you write any orchestration code.

The methodology also integrates with all the other context engineering patterns: [tool response design](./context-engineering-tool-response.md), [slash commands vs subagents](./context-engineering-slash-commands-subagents.md), and [compaction behavior](./context-engineering-compaction.md). Prototyping reveals which patterns your specific use case actually needs.

---

## A note to leadership

Ask your team for an outcome, not a platform. Ask them which of the three they're building—**chat surface**, **side-effect engine**, or **research artifact**—and how they'll know it worked. Then ask them where on the **autonomy spectrum** they intend to start, and what would make them move up a rung. 

Finally, ask for a harness: a place to try the idea against real inputs, produce a tangible result, and assert on it. If they can show you one passing run, you have evidence. If they can't, you still have clarity. Both are progress.

**Share this guide with your team before they start building. Understanding form factors and complexity levels will save you months of premature architecture work and give you confidence in what's actually possible.**
