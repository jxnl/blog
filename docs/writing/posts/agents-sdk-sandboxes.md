---
title: Sandboxes are coming to the Agents SDK, soon powered by the Codex app server
description: Developers do not build agents just to answer questions. They build them to deliver work, and that work needs a real place to happen.
date: 2026-04-15
authors:
  - jxnl
categories:
  - Applied AI
  - Software Engineering
comments: true
draft: true
slug: agents-sdk-sandboxes
tags:
  - Agents
  - Sandboxes
  - OpenAI
  - Coding Agents
  - Context Engineering
---

# Sandboxes are coming to the Agents SDK, soon powered by the Codex app server

Today we are adding first-party sandbox support to the Agents SDK.

Developers do not build agents just to answer questions. They build them to deliver work. And real work needs a place to happen: somewhere it can be tracked, resumed, inspected, and kept on course over time.

```python
from docker import from_env as docker_from_env

from agents import Runner
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.capabilities import Compaction, Filesystem, Shell
from agents.sandbox.entries import Dir, File, GitRepo
from agents.sandbox.sandboxes.docker import DockerSandboxClient, DockerSandboxClientOptions

# Define the manifest.
manifest = Manifest(
    entries={
        "AGENTS.md": File(content=b"Inspect the codebase before answering. Keep it concise.\n"),
        "repo": GitRepo(repo="openai/openai-agents-python", ref="main"),
        "output": Dir(description="Write generated artifacts here."),
    }
)

# Define the client.
# Other providers follow the same shape: CloudflareSandboxClient,
# E2BSandboxClient, DaytonaSandboxClient, ModalSandboxClient, etc.
client = DockerSandboxClient(docker_from_env())

# Define the sandbox session.
session = await client.create(
    manifest=manifest,
    options=DockerSandboxClientOptions(image="python:3.14-slim"),
)

# Define the worker.
agent = SandboxAgent(
    name="Codebase Summarizer",
    model="gpt-5.4",
    default_manifest=manifest,
    capabilities=[Shell(), Filesystem(), Compaction()],
)

# Run the worker in the sandbox.
async with session:
    result = await Runner.run(
        agent,
        "Write a short summary of what's going on in this codebase as a presentation and save it to output/summary.pdf.",
        run_config=RunConfig(sandbox=SandboxRunConfig(session=session)),
    )
```

By the end of this post, you'll understand:

1. What it means for the Agents SDK to be in distribution.
   - We used to beg models for JSON until function calling gave us a real place to put it.
   - Built-in tools like shell work better than hand-rolled `bash` or `shell` lookalikes.
   - Compaction and memory are not prompt tricks. They work best when they are part of the harness.
2. Why "everything is computer," but not every task needs one.
   - Some tasks should stay lightweight.
   - Some tasks need files, processes, browsers, credentials, or persistent state.
   - Isolation matters when model-generated code can read files, run commands, or touch credentials.
   - Separating orchestration from compute lets you choose the right amount of computer for the job.
3. How sandboxes help agents leave behind real work.
   - Pull requests, migrations, and vibe-coded apps.
   - Data rooms turned into memos, spreadsheets, and evidence tables.
   - Artifacts like PDFs, decks, charts, and reports.
   - Browser workflows, app debugging, and computer use.
   - Autonomous research runs, including GPU-backed experiments.
4. Why building on the Agents SDK helps you build toward where agents are going.
   - New capabilities can land underneath the harness.
   - You get to benefit from that without rebuilding your agent infrastructure from scratch.

<!-- more -->

## What does it mean to be in distribution?

Remember structured outputs before structured outputs?

### Structured outputs

Before function calling, you had to beg for JSON. You asked for things in quotes, maybe in a code block, maybe in XML, maybe in something else, and then figured out where in the prompt you could stuff examples and all that good stuff.

> "Please return only JSON in <json> tags. No commentary. No markdown. No explanation."

I was one of the creators of Instructor, and a lot of that work came from thinking about what it means to be in distribution for the model.

At the time, a lot of the work was basically about using function calling to trick the model into giving me JSON.

Eventually we got function calling, which was the first time there was actually a place we could expect JSON. We used that heavily. Later, we got things like output schemas, and things got a lot better and a lot more reliable. There was less tricking the model and more using interfaces the model actually understood well.

That is what I mean by being in distribution.

### Shell tool

Being in distribution is also as simple as using the right tools. We now have our own batch of raw tools, our own compaction tools, and our own memory tools, and those have been reinforced into the system. That might sound like a small difference, but maybe we name our tool `bash` and somebody else names their tool `shell`. That can actually matter for performance.

> With shell access, you can spend a lot of time debating whether the tool should be called `run_command`, `bash`, or `shell`, what the docstring should say, and how to prompt it to be more creative with piping, composition, and interacting with other Unix commands. A lot of that can be captured much more cleanly by using OpenAI's built-in shell capability instead. The point is not just convenience. The point is that the model already understands that tool shape better.

```python
from agents.sandbox import SandboxAgent
from agents.sandbox.capabilities import Compaction, Filesystem, Shell

agent = SandboxAgent(
    name="Source assistant",
    model="gpt-5.4",
    instructions="Search the repo, inspect files, and keep going across long tasks.",
    default_manifest=manifest,
    capabilities=[Shell(), Filesystem(), Compaction()],
)
```

### Compaction and prompt caching

On Twitter, I have seen a lot of people talk about how much they love Codex's ability to compact and keep going. Not only is it not a prompt trick, it is a real path in the harness, and it is in distribution to these models.

The same thing applies to memory and prompt caching. Long-running agents need to carry state forward without replaying the whole world every turn, and prompt caching matters because it improves price performance.

All of these things add up to incredibly good price performance across long-running tasks. It is not only about fitting more into context. It is about making the work cheaper, faster, and less brittle.

Where is this headed? I'm not really sure, but I know that by using an in-distribution harness, you can see where the puck is going with us, rather than having to chase it from behind.

## Why is everything computer?

There have been a lot of conversations lately about how coding agents are actually the precursor to a much broader set of knowledge-work skills. Code is the easiest way to learn this because it gives you a very concrete environment to act in.

### Coding Becomes Knowledge Work

That can start with something as simple as running a Python script. Then it graduates to writing tools that call Playwright to control a browser, generate Excel spreadsheets with common Python libraries like openpyxl or XlsxWriter, or generate slides that export to PDF and PowerPoint with Slidev.

As things get even more advanced, computer use and browser use let the agent do even more, whether that is in a browser or its own Linux box.

### Separating orchestration vs compute

That also does not mean every single task you want an agent to do needs to be provisioned with 2 GB of RAM.

By separating the computer, or in this case the sandbox, from the agent orchestration layer, you get the benefits of using AI while still having the flexibility to mount a sandbox only when you need it. You can think without turning the laptop on every time. The computer is there when the work actually requires it.

### Isolation and security

That separation matters for security too. You are much less likely to leak something like your OpenAI API credentials on the machine running the agent if the code is actually executing inside a separate sandbox.

We effectively separate the brain and the hands.

This matters because agentic code execution is not theoretical anymore. If the agent can read files, run commands, install packages, open browsers, and keep going over a long task, then the execution boundary becomes part of the product. You do not want that boundary to be an accident of whatever machine happened to run the agent loop.

Some tasks need no sandbox. Some need one small workspace. Some are better served by many isolated workspaces. The important part is that the harness can decide what needs compute, while the sandbox defines what that compute is allowed to touch.

## What are the applications of sandboxes?

The point of a sandbox is not just that the agent can run commands. The point is that the agent can leave behind work.

The way I think about this is: what is the work that needs to get done, where does it need to get done, and what should the agent leave behind? Once you know the deliverable, it becomes much easier to scaffold the agent, build evals around it, and move forward.

### Code generation for pull requests, migrations, and vibe coding

Code generation gets much more useful when the agent can work inside the repo instead of describing changes from the outside. Give it a real checkout, shell and filesystem tools, validation commands, and a resumable workspace where it can leave behind a patch or pull request.

Sample prompt:

> The repo is cloned at `repo/`. Read `AGENTS.md`, make the smallest safe change, run tests, and prepare a PR summary. If there is an app, serve it and use the browser to verify it.

### Data room extraction

Data rooms are where a messy folder becomes a real work product. Mount the PDFs, spreadsheets, contracts, filings, or exports, then ask the agent to turn unstructured data into a memo, evidence table, workbook, risk register, or database. The workspace does not have to be local either: it can mount S3, Google Cloud Storage, Azure Blob Storage, or Cloudflare R2 and inspect only what it needs.

Sample prompt:

> Read everything in `data-room/`. Create `output/customers.xlsx` with two tabs: `Contracts` and `Risks`. Include source files for every row.

### Creating artifacts like PDFs, spreadsheets, and more

Artifacts are the part I keep coming back to because the output of an agent does not have to be a string. It can be a spreadsheet, PDF, dataset, chart, report, PowerPoint, or folder of generated files, and skills make those outputs much easier to produce reliably.

Sample prompt:

> Use the Slidev skill to turn `brief.md` and `figures/` into a short investor update deck. Write the source to `output/deck/`, export `output/investor-update.pdf`, and list the files created.

### Computer use and browser use for debugging

A generated app is only really useful once someone can run it. If the sandbox can expose a port, the agent can build a Vite app, serve it, open it in a browser, click around, take screenshots, and fix what it sees.

This is also where providers start to feel distinct. Daytona has been building some of the more compelling computer-use examples here: browser-driven form filling, app interaction, and workflows where the agent is not just producing code but actually operating the environment it created.

Sample prompt:

> Use `user.json` and `task.md` to complete the browser workflow. Fill out the form, upload files from `attachments/`, stop if anything is ambiguous, then call `mark_task_done` with the confirmation number.

### Autonomous research, including GPUs

Autonomous research needs somewhere to accumulate evidence, attempts, and intermediate results. The sandbox can hold data, scripts, logs, evaluation outputs, and a durable run ledger; compaction, memory, and resumability keep the work alive when it needs to fan out, pause, or continue later.

Modal has some of the clearest examples of this shape already. The same is true on the migration side, where longer-running, artifact-producing workflows need a durable place to run.

Sample prompt:

> Run a parameter-golf search over `experiments/`. Fan out GPU-backed candidates, write every attempt to `runs/ledger.csv`, keep the best valid runs in `output/best-runs.json`, and write a short memo on what mattered.

## Meeting you where you are today, taking you to where we will all be tomorrow

The thing I want you to take away is pretty simple: use the Agents SDK because it helps you build toward where agents are going, not where they are today.

Build something that might not 100% work today. Maybe it is artifact creation. Maybe it is a browser workflow. Maybe it is a data room, a code migration, or a research agent. In five or six months, not only might that agent work, it might work well, because the capabilities underneath it keep getting better.

You get those benefits because you are separating the harness from execution, investing in sandbox infrastructure, and using a harness that is in distribution to the models.

That is why I keep coming back to the work you want to deliver, not just how the work gets done. If you build ambitiously, we will do our best to meet you where you are and help take you to where we all need to be.

If you want the broader launch context, see the OpenAI post on the next evolution of the Agents SDK.
