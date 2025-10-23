---
title: "Context Engineering: Rapid Agent Prototyping"
description: "How to test agent ideas in hours using Claude Code SDK without building orchestration infrastructure - proven methodology from consulting engagements"
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

# How Do We Prototype Agents Rapidly?

_This is part of the [Context Engineering Series](./context-engineering-index.md). I'm focusing on rapid prototyping because testing agent viability quickly is essential for good context engineering decisions._

**If your boss is asking you to "explore agents," start here. This methodology will give you evidence in days, not quarters.**

Most teams waste months building agent frameworks before they know if their idea actually works. There's a faster way: use Claude Code as your testing harness to validate agent concepts without writing orchestration code.

<!-- more -->

## What Problem Does Rapid Prototyping Solve?

When teams want to test an agent idea, they typically start by building infrastructure:

- Message management systems
- Tool call parsing logic
- Retry mechanisms
- UI frameworks
- Logging and monitoring

By the time they get to testing the actual agent behavior, they've invested weeks in plumbing. Often they discover the fundamental idea doesn't work, but only after significant engineering investment.

## How Does the Claude Code SDK Help?

Claude Code has a project runner mode (`claude -p`) that turns any directory into an agent execution environment. It reads a `CLAUDE.md` file as system instructions and executes workflows using CLI tools you provide. This creates a perfect testing harness—you write instructions in English, expose tools as simple commands, and let Claude Code handle the execution loop.

**The key insight**: If it works once in this harness, the idea is viable. If it fails consistently, you know what's missing without building any infrastructure.

## Which Coding Agents Does This Work With?

While this article shows Claude Code, the approach is agent-agnostic. If a coding system can be driven from a CLI and read a simple instruction file (for example, `CLAUDE.md` or `agents.md`), you can use it with this harness.

Examples that fit (or can with a thin adapter):

- Cursor’s coding agent
- Devin
- AMP Code
- Codex
- Windsurf Agent

This also unlocks cross-agent evals:

- Keep the same `commands/` and `subagents/` folders and success criteria
- Add a small wrapper per agent that maps a standard command (for example, `run-agent <scenario-dir>`) to its CLI flags or subcommands
- Run the same scenarios across agents and compare pass rate, time, and cost

As features converge (slash commands, subagents, instruction files), you can swap the runner without changing your prototype. This lets you identify the useful components of systems that actually work well, separate from any single vendor.

## What Is the Anatomy of a Rapid Prototype?

Here's the exact structure that lets you test any agent idea:

```
agent-prototype/
├── .claude/agents/
│   └── youtube-study-notes-generator.md
├── CLAUDE.md              # System instruction + tool inventory
├── tools/                 # CLI wrappers for your APIs
│   ├── youtube-dl
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

### What Goes in CLAUDE.md?

This becomes your system prompt, structured for execution:

```markdown
# YouTube Study Notes Generator

## Mission

Given a YouTube URL, produce structured study notes in markdown format.

## Execution Flow

1. Fetch transcript/subtitles using youtube-dl tool
2. If transcript contains timestamps or XML noise, run cleanup-transcript.py
3. Read cleaned content and produce notes.md with exact formatting requirements
4. Stop when notes.md exists and passes structural validation

## Available Tools

- `youtube-dl <url>` → transcript.srt|vtt|txt (handles multiple subtitle formats)
- `cleanup-transcript.py <file>` → cleaned.txt (removes timestamps, ~4x token reduction)

## Success Criteria

Final notes.md must contain:

- One H1 title derived from video content
- Three H2 sections with descriptive headers
- Ten bullet points per section
- Brief summary at top (2-3 sentences)
- Links found in transcript under "Further Reading"

## Error Recovery

- If youtube-dl fails on English subtitles, try auto-generated or alternative languages
- If transcript too short/empty, document what was attempted
- If cleanup unnecessary (already clean), proceed directly to notes-writer
```

### How Should We Implement Tools as CLI Wrappers?

Tools should be deliberately simple—CLI commands that wrap your actual APIs. This connects directly to the [tool response design principles](./context-engineering-tool-response.md) I've written about—the structure of your tool outputs becomes as important as the functionality itself:

```bash
#!/bin/bash
# youtube-dl wrapper script
if [ -z "$1" ]; then
    echo "ERROR: YouTube URL required"
    echo "USAGE: youtube-dl <youtube-url>"
    exit 1
fi

# Fetch transcript with error handling
if ! yt-dlp --write-subs --write-auto-subs --sub-langs en --skip-download "$1"; then
    echo "ERROR: Could not fetch subtitles. Video may not have captions available."
    exit 1
fi

echo "SUCCESS: Transcript downloaded"
```

### How Do We Validate Success in Tests?

Each test folder represents a real scenario with concrete pass/fail criteria:

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

## How Do We Execute the Prototype?

To test any agent idea:

1. **Navigate to test scenario**: `cd tests/scenario1`
2. **Execute the workflow**: `claude -p` (reads CLAUDE.md, runs end-to-end)
3. **Validate results**: `python check.py` (pass/fail with specific reasons)

What you observe is Claude Code reading instructions, selecting tools, handling errors, and producing artifacts. You can watch it navigate edge cases in real-time—like when a video lacks English subtitles, it explores alternatives rather than simply failing.

## Why Is This Better Than Building Infrastructure First?

**Iteration speed**: You edit text files, not debug message loops or tool call parsing.

**Real-world inputs**: Test with actual URLs, emails, PDFs—not sanitized examples.

**Binary success metrics**: Either output meets specification or it doesn't. No subjective evaluation.

**Tool design feedback**: Immediately discover whether tool names are intuitive and error messages helpful.

**Economic transparency**: Token costs, latency, and failure rates visible in hours, not sprints.

## How Do We Prepare for Production?

### How Can Tool Errors Teach Next Actions?

Instead of generic failures, tools should guide next actions:

```bash
if [ -z "$user_id" ]; then
    echo "ERROR: user_id parameter missing"
    echo "NEXT_STEP: Call lookup_user --email user@domain.com first"
    exit 1
fi
```

### How Should We Structure Tool Responses?

Control output format for easier parsing. This is a practical application of the [context engineering principles](./context-engineering-tool-response.md) around faceted tool responses—providing metadata that helps agents make better decisions:

```bash
echo "STATUS: SUCCESS"
echo "OUTPUT_FILE: notes.md"
echo "METRICS: tokens_used=15420, sections=3, bullets=47"
echo "WARNINGS: Used auto-generated subtitles, accuracy may vary"
echo "FACETS: language=auto-generated, video_length=1247s, transcript_quality=medium"
```

Just like Level 4 faceted search responses, this gives Claude Code peripheral vision about the task completion, enabling better follow-up decisions.

### Sub-Agent Workflows and Slash Commands

Handle complexity with specialized instructions. The Claude Code harness naturally supports both [slash commands and subagents](./context-engineering-slash-commands-subagents.md)—two different approaches to managing context pollution:

```markdown
## Sub-Agent: Content Analysis

For transcripts >50,000 characters:

1. Use split-content tool to create manageable chunks
2. Call /analyze-section on each chunk with specific focus areas
3. Use /synthesize-findings to combine results into final notes
```

**The key insight from prototyping**: Claude Code lets you experiment with both approaches. You can implement `/analyze-transcript` as a slash command that dumps everything into the main context, or as a subagent that processes off-thread and returns clean summaries. Testing both in your prototype reveals which approach works better for your specific use case—often subagents win for token-heavy operations.

## The Economics of Rapid Prototyping

**Time to evidence**: Validate agent feasibility in hours, not weeks.

**Risk mitigation**: If Claude Code can't achieve the task with perfect tool access and no UI constraints, your production version likely won't either.

**Tool clarity discovery**: Learn whether you need narrow tools (`search_contracts`, `search_invoices`) or broad ones (`search(type=contract)`).

**Context management insights**: Because Claude Code handles conversation state automatically, you can focus on testing how much context pollution your tools create. This naturally surfaces candidates for [subagent architecture](./context-engineering-slash-commands-subagents.md) vs slash commands.

**Compaction benefits**: Claude Code's automatic [compaction behavior](./context-engineering-compaction.md) means you can prototype long-running tasks without managing conversation state manually. This reveals which workflows naturally generate trajectory data worth preserving vs noise that should be compacted away.

**Failure mode identification**: Pinpoint exactly where prompts are insufficient and where tools need better error handling.

**Production migration**: Successful test folders become your production test suite. Tools and instructions transfer directly to any framework you build.

## When Doesn't This Methodology Apply?

The boundaries are narrower than you might expect:

- **High-volume production loads**: Claude Code isn't designed for concurrent execution at scale—but this rarely matters for prototyping
- **Hardware integration requirements**: Physical device control or specialized hardware interfaces can't be easily wrapped in CLI tools

**Common misconceptions about limitations:**

- **Complex authentication**: Actually works well—API keys, service account tokens, and even multi-step auth flows can be handled in your CLI wrappers. Claude Code manages tool permissions and can resume from previous sessions.
- **Multi-session state**: Claude Code handles conversation history and can pick up where it left off across sessions. State that needs to persist beyond the conversation can be managed through your tools.
- **Real-time interaction**: The command-line interaction pattern is often simpler than building a chat interface—users can provide input when the agent requests it.

But for the fundamental question—"Is this agent idea possible?"—this provides the fastest path to evidence in almost all cases.

## What Checklist Guides Implementation?

Before writing orchestration code:

- [ ] **Define success criteria**: What concrete output proves the agent works?
- [ ] **Identify 3-6 core tools** that would make the task possible
- [ ] **Create 5-10 test scenarios** with real-world inputs
- [ ] **Write CLAUDE.md** with clear execution flow
- [ ] **Build simple CLI tool wrappers** for your APIs
- [ ] **Execute test scenarios** and iterate on instructions/tools
- [ ] **Achieve at least one passing test** before considering production architecture
- [ ] **Explore architectural patterns**: Use the prototype to test whether [slash commands or subagents](./context-engineering-slash-commands-subagents.md) work better for your specific use case

## What Is the Bottom Line?

Stop building agent infrastructure before you know if the idea works. Use this methodology to get evidence in hours:

1. Write instructions in English (CLAUDE.md)
2. Expose tools as simple CLI commands
3. Create tests with real inputs and concrete success criteria
4. Run `claude -p` and iterate until you get a pass

If Claude Code can't make it work with perfect tool access and no constraints, your production version probably won't either. But if you can get one passing test, you've proven the concept and can invest in hardening with confidence.

**The fastest way to prototype an agent isn't to build an agent at all—it's to test whether the idea works before you build anything.**

## How Does This Connect to the Context Engineering Framework?

This prototyping methodology integrates with all the other context engineering patterns:

**Tool Response Design**: Your CLI tools naturally implement the [four levels of context engineering](./context-engineering-tool-response.md)—from minimal chunks to faceted responses with metadata. Prototyping reveals which level your use case actually needs.

**Context Pollution Management**: The harness makes [slash commands vs subagents](./context-engineering-slash-commands-subagents.md) trade-offs visible immediately. You'll see when main context gets flooded with noise and when clean subagent responses perform better.

**Compaction Understanding**: Long-running prototypes surface [compaction patterns](./context-engineering-compaction.md) naturally. You'll discover which conversation trajectories preserve learning vs which create maintenance burden.

**Form Factor Validation**: The methodology connects directly to the [agent framework decisions](./context-engineering-agent-frameworks.md) around chatbots, workflows, and research artifacts. Your tests reveal which form factor actually delivers the outcome you need.

This is why rapid prototyping belongs in the Context Engineering series—it's not just about speed, it's about discovering the right information architecture for your specific problem before committing to production complexity.
