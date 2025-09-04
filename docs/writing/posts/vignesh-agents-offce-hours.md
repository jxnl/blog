---
title: "Before You “Build an Agent”: The Conversation I Have With Every Team"
description: "A field note for product & engineering leaders, with a coda in dialogue with Vignesh Mohankumar"
date: 2025-09-04
authors:
  - jxnl
categories:
  - Applied AI
  - Software Engineering
---

# Before You “Build an Agent”: The Conversation I Have With Every Team


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

## Part III — “Show me, don’t tell me.” A conversation with Vignesh

You couldn’t see the screen on our call, so here’s the moment that mattered, captured as it was: a quick, working prototype; no orchestrator; just a harness, a few tools, and a result we could argue about.

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

## The Claude Code SDK Testing Methodology: How to Prototype Agents Without Building an Orchestrator

The conversation with Vignesh revealed what most teams miss: you don't need to build an agent framework to test whether an agent idea is viable. What you need is a harness that lets you iterate on the three things that actually matter—system instructions, tool descriptions, and tool response formats—without getting distracted by message management, retry logic, or UI concerns.

**If your boss is asking you to "explore agents," start here. This methodology will give you evidence in days, not quarters.**

### The Core Insight: Use Claude Code as Your Testing Harness

Claude Code has a project runner mode (`claude -p`) that turns any directory into an agent execution environment. It reads a `CLAUDE.md` file as a system instruction and executes workflows using whatever CLI tools you make available. This creates a nearly perfect testing harness for agent ideas—you write instructions in plain English, expose tools as simple commands, and let Claude Code execute end-to-end.

The workflow becomes: if it works once in this harness, the idea is possible. If it fails consistently, you know what's missing—without building orchestration infrastructure.

### The Anatomy of a Rapid Prototype

Here's the exact structure I showed Vignesh, because replication matters:

```
agent-prototype/
├── .claude/agents/
│   └── youtube-study-notes-generator.md
├── CLAUDE.md              # System instruction + tool inventory  
├── tools/                 # CLI wrappers for your APIs
│   ├── yt-dl              
│   └── notes-writer      
└── tests/                 # One folder per test scenario
    ├── scenario1/
    │   ├── request.txt    # Input (URL, email, JSON, etc.)
    │   └── check.py       # Assertions on expected outputs
    ├── scenario2/
    │   ├── request.txt
    │   └── check.py
    └── scenario3/
        ├── request.txt
        └── check.py
```

**The CLAUDE.md file** becomes your executable specification:

```markdown
# YouTube Study Notes Generator

## Mission
Given a YouTube URL, produce structured study notes in markdown format.

## Execution Flow
1. Fetch transcript/subtitles using yt-dl tool
2. If transcript contains timestamps or XML noise, run cleanup-transcript  
3. Read cleaned content and produce notes.md with exact formatting requirements
4. Stop when notes.md exists and passes structural validation

## Available Tools
- `yt-dl <url>` → transcript.srt|vtt|txt (handles multiple subtitle formats)
- `cleanup-transcript <file>` → cleaned.txt (removes timestamps, ~4x token reduction)  
- `notes-writer <file>` → notes.md (enforces: 1 H1, 3 H2s, 10 bullets each)

## Success Criteria  
Final notes.md must contain:
- One H1 title derived from video content
- Three H2 sections with descriptive headers  
- Ten bullet points per section
- Brief summary at top (2-3 sentences)
- Links found in transcript under "Further Reading"

## Error Recovery
- If yt-dl fails on English subtitles, try auto-generated or alternative languages
- If transcript too short/empty, document what was attempted
- If cleanup unnecessary (already clean), proceed directly to notes-writer
```

**Tool implementations** are deliberately simple CLI wrappers:

```bash
#!/bin/bash
# yt-dl wrapper script
if [ -z "$1" ]; then
    echo "ERROR: YouTube URL required"
    echo "USAGE: yt-dl <youtube-url>"  
    exit 1
fi

# Fetch transcript with error handling
if ! yt-dlp --write-subs --write-auto-subs --sub-langs en --skip-download "$1"; then
    echo "ERROR: Could not fetch subtitles. Video may not have captions available."
    exit 1
fi

echo "SUCCESS: Transcript downloaded"
```

**Test validation** makes success concrete:

```python
# tests/scenario1/check.py
import pathlib
import re

# Verify output file exists
notes_file = pathlib.Path("notes.md")
assert notes_file.exists(), "notes.md was not generated"

# Validate structure
content = notes_file.read_text()

# Check header count
h1_count = content.count('\n# ')
assert h1_count == 1, f"Expected 1 H1, found {h1_count}"

h2_count = content.count('\n## ')  
assert h2_count >= 3, f"Expected ≥3 H2s, found {h2_count}"

# Validate bullet density per section
sections = re.split(r'\n## ', content)
for i, section in enumerate(sections[1:], 1):
    bullets = [line for line in section.split('\n') 
              if line.strip().startswith('- ')]
    assert len(bullets) >= 8, f"Section {i}: {len(bullets)} bullets (need ≥8)"

print("✅ All structural requirements met")
```

### The Execution Protocol

To test any agent idea:

1. **Navigate to test scenario**: `cd tests/scenario1`
2. **Execute the workflow**: `claude -p` (reads CLAUDE.md, runs end-to-end)  
3. **Validate results**: `python check.py` (pass/fail with specific reasons)

What you observe is Claude Code reading your instructions, selecting tools, handling errors, and producing artifacts. The critical moment in the Vignesh demo was watching it navigate missing English subtitles—instead of failing, it explored alternatives and still delivered structured notes.

### Why This Beats Building an Orchestrator First

**Iteration speed**: You're editing text files, not debugging message arrays or tool call parsing.

**Real-world inputs**: Test with actual URLs, emails, PDFs—not sanitized examples.

**Binary success metrics**: Either the output meets specification, or it doesn't. No subjective evaluation needed.

**Tool design feedback**: You immediately discover whether tool names are intuitive, argument patterns sensible, and error messages helpful.

**Economic transparency**: Token costs, latency, and failure rates become visible in hours, not sprints.

### Advanced Patterns for Production Readiness

**Teaching through tool errors**: Instead of generic failures, tools should guide next actions:

```bash
if [ -z "$user_id" ]; then
    echo "ERROR: user_id parameter missing"
    echo "NEXT_STEP: Call lookup_user --email user@domain.com first"
    exit 1
fi
```

**Structured tool responses**: Control output format for easier parsing:

```bash  
echo "STATUS: SUCCESS"
echo "OUTPUT_FILE: notes.md"
echo "METRICS: tokens_used=15420, sections=3, bullets=47"
echo "WARNINGS: Used auto-generated subtitles, accuracy may vary"
```

**Sub-agent workflows**: Handle complexity with specialized instructions:

```markdown
## Sub-Agent: Content Analysis  
For transcripts >50,000 characters:
1. Use split-content tool to create manageable chunks
2. Call /analyze-section on each chunk with specific focus areas  
3. Use /synthesize-findings to combine results into final notes
```

### The Economics of Rapid Prototyping

**Time to evidence**: Validate agent feasibility in hours, not weeks.

**Risk mitigation**: If Claude Code can't achieve the task with perfect tool access and no UI constraints, your production version likely won't either.

**Tool clarity discovery**: Learn whether you need narrow tools (`search_contracts`, `search_invoices`) or broad ones (`search(type=contract)`).

**Failure mode identification**: Pinpoint exactly where prompts are insufficient and where tools need better error handling.

**Production migration**: Successful test folders become your production test suite. Tools and instructions transfer directly to any framework you build.

### When This Methodology Doesn't Apply

Clear boundaries exist for this approach:

- **Real-time interaction dependencies**: If the agent's value requires immediate user feedback loops
- **Multi-session state requirements**: When context must persist across days or users  
- **High-volume production loads**: Claude Code isn't designed for concurrent execution at scale
- **Complex authentication flows**: OAuth dances and multi-step auth make CLI wrappers cumbersome

But for the fundamental question—"Is this agent idea possible?"—this methodology provides the fastest path to reliable evidence.

### Implementation Checklist for Teams

Before writing any orchestration code:

- [ ] **Define the form factor**: Chatbot, workflow, or research artifact?
- [ ] **Identify 3-6 core tools** that would make the task possible
- [ ] **Create 5-10 test scenarios** with real-world inputs
- [ ] **Write CLAUDE.md** with clear success criteria
- [ ] **Build simple CLI tool wrappers** for your APIs
- [ ] **Execute test scenarios** and iterate on instructions/tools
- [ ] **Achieve at least one passing test** before considering production architecture

This methodology has saved multiple consulting engagements from months of premature infrastructure work. **If you're being asked to "build agents," start here. Get evidence first, then decide what's worth hardening into production.**

---

## A note to leadership

Ask your team for an outcome, not a platform. Ask them which of the three they're building—**chat surface**, **side-effect engine**, or **research artifact**—and how they'll know it worked. Then ask them where on the **autonomy spectrum** they intend to start, and what would make them move up a rung. 

Finally, ask for a harness: a place to try the idea against real inputs, produce a tangible result, and assert on it. If they can show you one passing run, you have evidence. If they can't, you still have clarity. Both are progress.

**Share this guide with your team before they start building. The methodology will save you months of premature architecture work and give you confidence in what's actually possible.**
