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

# Context Engineering: Rapid Agent Prototyping

*This is part of the [Context Engineering Series](./context-engineering-index.md). I'm focusing on rapid prototyping because testing agent viability quickly is essential for good context engineering decisions.*

**If your boss is asking you to "explore agents," start here. This methodology will give you evidence in days, not quarters.**

Most teams waste months building agent frameworks before they know if their idea actually works. There's a faster way: use Claude Code as your testing harness to validate agent concepts without writing orchestration code.

## The Core Problem

When teams want to test an agent idea, they typically start by building infrastructure:
- Message management systems
- Tool call parsing logic  
- Retry mechanisms
- UI frameworks
- Logging and monitoring

By the time they get to testing the actual agent behavior, they've invested weeks in plumbing. Often they discover the fundamental idea doesn't work, but only after significant engineering investment.

## The Claude Code SDK Solution

Claude Code has a project runner mode (`claude -p`) that turns any directory into an agent execution environment. It reads a `CLAUDE.md` file as system instructions and executes workflows using CLI tools you provide. This creates a perfect testing harness—you write instructions in English, expose tools as simple commands, and let Claude Code handle the execution loop.

**The key insight**: If it works once in this harness, the idea is viable. If it fails consistently, you know what's missing without building any infrastructure.

## The Anatomy of a Rapid Prototype

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

### The CLAUDE.md File: Your Executable Specification

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

### Tool Implementations: Simple CLI Wrappers

Tools should be deliberately simple—CLI commands that wrap your actual APIs:

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

### Test Validation: Make Success Concrete

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

## The Execution Protocol

To test any agent idea:

1. **Navigate to test scenario**: `cd tests/scenario1`
2. **Execute the workflow**: `claude -p` (reads CLAUDE.md, runs end-to-end)  
3. **Validate results**: `python check.py` (pass/fail with specific reasons)

What you observe is Claude Code reading instructions, selecting tools, handling errors, and producing artifacts. You can watch it navigate edge cases in real-time—like when a video lacks English subtitles, it explores alternatives rather than simply failing.

## Why This Beats Building Infrastructure First

**Iteration speed**: You edit text files, not debug message loops or tool call parsing.

**Real-world inputs**: Test with actual URLs, emails, PDFs—not sanitized examples.

**Binary success metrics**: Either output meets specification or it doesn't. No subjective evaluation.

**Tool design feedback**: Immediately discover whether tool names are intuitive and error messages helpful.

**Economic transparency**: Token costs, latency, and failure rates visible in hours, not sprints.

## Advanced Patterns for Production Readiness

### Teaching Through Tool Errors

Instead of generic failures, tools should guide next actions:

```bash
if [ -z "$user_id" ]; then
    echo "ERROR: user_id parameter missing"
    echo "NEXT_STEP: Call lookup_user --email user@domain.com first"
    exit 1
fi
```

### Structured Tool Responses

Control output format for easier parsing:

```bash  
echo "STATUS: SUCCESS"
echo "OUTPUT_FILE: notes.md"
echo "METRICS: tokens_used=15420, sections=3, bullets=47"
echo "WARNINGS: Used auto-generated subtitles, accuracy may vary"
```

### Sub-Agent Workflows

Handle complexity with specialized instructions:

```markdown
## Sub-Agent: Content Analysis  
For transcripts >50,000 characters:
1. Use split-content tool to create manageable chunks
2. Call /analyze-section on each chunk with specific focus areas  
3. Use /synthesize-findings to combine results into final notes
```

## The Economics of Rapid Prototyping

**Time to evidence**: Validate agent feasibility in hours, not weeks.

**Risk mitigation**: If Claude Code can't achieve the task with perfect tool access and no UI constraints, your production version likely won't either.

**Tool clarity discovery**: Learn whether you need narrow tools (`search_contracts`, `search_invoices`) or broad ones (`search(type=contract)`).

**Failure mode identification**: Pinpoint exactly where prompts are insufficient and where tools need better error handling.

**Production migration**: Successful test folders become your production test suite. Tools and instructions transfer directly to any framework you build.

## Real Example: Customer Service Agent

Let me show you how this works for a more complex scenario:

```markdown
# Customer Service Agent

## Mission
Process customer support requests and route to appropriate resolution

## Execution Flow
1. Parse customer email/message using parse-request tool
2. Look up customer history using customer-lookup tool  
3. Classify issue severity and type using classify-issue tool
4. Route to appropriate resolution:
   - Password reset → trigger-password-reset tool
   - Billing inquiry → escalate-to-billing tool
   - Technical issue → create-support-ticket tool
5. Send response using send-response tool

## Available Tools
- `parse-request <message>` → structured request data
- `customer-lookup <email>` → customer history and account status
- `classify-issue <request_data>` → severity and category
- `trigger-password-reset <customer_id>` → reset link sent
- `escalate-to-billing <customer_id> <issue>` → billing team notified
- `create-support-ticket <details>` → ticket created
- `send-response <customer_email> <response>` → customer notified
```

Test scenarios become customer emails with expected outcomes:

```
# tests/password-reset-request/request.txt
From: user@example.com
Subject: Can't log in to my account

Hi, I've been trying to log in but keep getting "invalid password" errors. 
I'm sure I'm using the right password. Can you help me reset it?

Thanks,
Jane
```

```python
# tests/password-reset-request/check.py
import json
import pathlib

# Check that password reset was triggered
reset_file = pathlib.Path("password_reset_triggered.json")
assert reset_file.exists(), "Password reset was not triggered"

reset_data = json.loads(reset_file.read_text())
assert reset_data["customer_email"] == "user@example.com"
assert reset_data["method"] == "email_link"

# Check customer response was sent
response_file = pathlib.Path("customer_response.txt")
assert response_file.exists(), "No response sent to customer"

response = response_file.read_text()
assert "password reset link" in response.lower()
assert "user@example.com" in response

print("✅ Password reset flow completed correctly")
```

## When This Methodology Doesn't Apply

Clear boundaries exist:

* **Real-time interaction dependencies**: If the agent's value requires immediate user feedback loops
* **Multi-session state requirements**: When context must persist across days or users  
* **High-volume production loads**: Claude Code isn't designed for concurrent execution at scale
* **Complex authentication flows**: OAuth dances make CLI wrappers cumbersome

But for the fundamental question—"Is this agent idea possible?"—this provides the fastest path to evidence.

## Implementation Checklist

Before writing orchestration code:

- [ ] **Define success criteria**: What concrete output proves the agent works?
- [ ] **Identify 3-6 core tools** that would make the task possible
- [ ] **Create 5-10 test scenarios** with real-world inputs  
- [ ] **Write CLAUDE.md** with clear execution flow
- [ ] **Build simple CLI tool wrappers** for your APIs
- [ ] **Execute test scenarios** and iterate on instructions/tools
- [ ] **Achieve at least one passing test** before considering production architecture

## Migration to Production

Once you have passing tests, you have several options:

**Option 1: Harden the harness**
Keep using Claude Code but add proper logging, monitoring, and error handling for production workloads.

**Option 2: Reimplement the hot path**  
Use your successful tests as specifications to build optimized production code for the most common scenarios.

**Option 3: Hybrid approach**
Build deterministic workflows for the predictable 80% of cases, keep the agent for the complex 20%.

The test folders become your regression suite regardless of which path you choose.

## Conclusion

Stop building agent infrastructure before you know if the idea works. Use this methodology to get evidence in hours:

1. Write instructions in English (CLAUDE.md)
2. Expose tools as simple CLI commands
3. Create tests with real inputs and concrete success criteria  
4. Run `claude -p` and iterate until you get a pass

If Claude Code can't make it work with perfect tool access and no constraints, your production version probably won't either. But if you can get one passing test, you've proven the concept and can invest in hardening with confidence.

**The fastest way to prototype an agent isn't to build an agent at all—it's to test whether the idea works before you build anything.**