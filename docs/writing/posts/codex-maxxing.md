---
title: Codex-maxxing
description: How I use Codex as a place where long-running work can live.
date: 2026-05-10
authors:
  - jxnl
categories:
  - Applied AI
  - Personal
comments: true
draft: false
slug: codex-maxxing
tags:
  - Codex
  - AI
  - Workflows
  - Personal Software
---

# Codex-maxxing

I was already using coding agents a lot before Codex. Mostly, though, I used them through interfaces built for coding work: making diffs, changing repos, and shipping code.

Around November, I started pushing them into knowledge work too. I made presentations in [Slidev](https://sli.dev/), used agents more like note-takers with voice input, and kept looking for other artifacts a coding agent could help me produce: an `index.html`, a PDF, a spreadsheet, a slide deck.

The latest Codex app upgrades are the first thing I've used that make that broader mode feel native. Codex is still excellent for coding, but the more interesting shift is that it gives my work somewhere to live.

What changed my behavior was learning to give work an operating loop: a durable thread, shared memory, tools that can act on my computer, ways to steer and resume the task, and a surface where I can review the artifact itself.

<!-- more -->

## Durable threads
The first thing that changed my behavior was compaction.

!!! note "Compaction"

    Compaction
    : Compressing a long-running thread so it can keep going without carrying every old message in full.

I now keep a pinned thread for every important workstream I care about:

- my Chief of Staff thread
- [the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- [the OpenAI CLI](https://github.com/openai/openai-cli)
- [Codex for open source](https://openai.com/form/codex-for-oss)
- one just to monitor Twitter

These are not short chats. They are megathreads that I have been compacting for months. They accumulate history, preferences, and old decisions that I do not want to recreate every time I come back.

!!! tip "Pinned thread shortcuts"

    You can jump directly to pinned threads with `Command-1` through `Command-9`.

There is a tradeoff here. Long-running threads are not free. If you revisit them later, the conversation is probably no longer in cache, so you can incur more cost than you would in a fresh short thread. For workstreams I care about, continuity is worth it.

## Voice input

Voice input gets more of my actual thinking into Codex.

The benefit is not speed. It is that the agent gets the unedited version of my thinking. Codex has built-in voice input, but I also use Wispr Flow because system-wide dictation changes how much context I can feed into everything else too. If I am planning a piece of work, I might say, "I think there is some guy named Ben in Slack who mentioned this, I do not remember exactly what, just go look." That sentence is too vague and annoying to type, but completely natural to say.

The same thing applies to transcripts. If I want to write a post, I can call someone, record the conversation, or talk to them in person with Granola on my phone, then use the transcript as the starting material. A lot of plans get better when the model has access to the messy version of what I think, not just the polished one.

## Steering

Voice becomes more useful when combined with steering.

!!! note "Steering"

    Steering
    : Adding more direction while Codex is already working instead of waiting for the current step to finish.

Steering lets you inject the next message after a tool call. If I am reviewing a website, I can keep talking while I look at it:

- make this smaller
- this copy is wrong
- the spacing between these two things feels off
- once this is done, open a PR
- wait for the preview deploy
- send the preview link to the person who needs to review it on Slack

I do not need to wait for each step to finish before deciding the next one. I can keep adding intent while the agent is still working, then walk away with the queue already shaped.

Later, Heartbeats can monitor the PR or Slack thread after I leave. The unit of work stops being "one prompt, one answer." It becomes a small operating loop.

## Memory

Once threads started lasting longer, they needed shared memory outside any one repo.

The important move is saving things to disk. A long thread can remember a lot, but that memory is trapped inside the thread unless the useful parts get written somewhere durable. The point of the memory system is to turn what the thread learns into artifacts I can inspect, edit, diff, and reuse.

Most of my long-running threads start in an Obsidian vault:

```text
vault/
├── TODO.md
├── people/
├── projects/
├── agent/
└── notes/
```

At the top level, I keep `AGENTS.md` instructions that tell the model to write things down: as you learn more about people, make progress on projects, make a decision, or close an open loop, update the relevant pages in the vault.

The vault is where the agent lives, separate from any one project. Repositories hold code. The vault holds rolling context around my work: people, decisions, open loops, daily notes, project state, and the bits of understanding that would otherwise get lost between threads.

I also keep the vault as a GitHub repo. That buys me two things:

1. it can work in the cloud
2. diffs become a review surface for memory

When the agent updates the vault, I can read the diff and see what it thought was important enough to remember. That review step matters. I do not want evergreen threads to quietly accumulate vibes in conversation history. I want them to write down what changed: this person prefers this, this project is waiting on that, this decision was made, this loop is closed.

This is also why I like memory as files. Files force the agent to compress experience into a form that can survive the thread. If the thread dies, compacts badly, or becomes too expensive to keep leaning on, the useful knowledge is still there. The pattern is simple: keep important work in a repo, give Codex permission and instructions to update it, and review the diff like any other change.

At that point, pinned threads start to feel less like chats and more like different workers reading from the same notebook.

Codex also has first-party memory features in `Settings > Personalization > Memories`. I think of those as a recall layer on top of the explicit disk-backed system. The vault is the source of truth I can review and edit. Memories are what help Codex remember stable preferences, recurring workflows, project conventions, and known pitfalls when I start a new thread.

[Chronicle](https://developers.openai.com/codex/memories/chronicle) is interesting for the same reason. I have not used it seriously yet, and the docs are clear that it is an opt-in research preview with real tradeoffs around permissions, rate limits, prompt injection, and unencrypted local memory files. But directionally it points at the same thing I care about: work should leave behind structured memory, not just a longer chat transcript.

!!! note "Shared memory"

    Shared memory
    : Context kept outside a single chat, such as notes in my vault that different threads can reuse.

## Computer and Browser Use

Once a thread has memory, the next question is what it can touch.

The most useful distinction in my own head is:

- `$browser` is for local web surfaces I want to inspect and annotate
- `@chrome` is for signed-in browser state and multiple tabs
- `@computer` is for work that only exists as a GUI

If I am iterating on a local app, I want `$browser`. If I need to work inside a logged-in browser session, I want `@chrome`. If the only way to do the task is to click through a desktop app, I want `@computer`.

[Appshots](https://dub.sh/PbgvcAJ) is the lighter-weight version of this. Sometimes I do not want Codex to operate the app yet. I just want to show it the thing I am looking at. On macOS, you can press both Command keys and send the frontmost window into a Codex thread with a screenshot and whatever text the app makes available.

That is useful for the annoying middle category of context that is easier to show than describe: an error modal, a settings panel, an API reference page, an email, a calendar view, a design preview, or the weird state of an app that only makes sense when you see it. Instead of typing a long setup prompt, I can point Codex at the current window and say, "this is the thing I mean."

On my work machine, Twitter is logged into Safari. If I have `@computer` read Twitter there, I lose Safari while it works. `@chrome` is better when I want the agent to use several authenticated tabs in parallel without taking over the whole app I am using.

Connectors extend that reach into the rest of my actual work. The ones I use most are `$slack`, `$gmail`, and `$calendar`, because Slack threads, inboxes, and calendars are where a lot of work shows up before it ever becomes code.

Skills make repeated workflows reusable. Skill Creator and Skill Installer are a good place to start. Skill Installer lets you add OpenAI-recommended skills directly from the composer. After [Codex pets](https://developers.openai.com/codex/app/settings#codex-pets) launched, I used it to install the Hatch Pet skill, but the useful pattern is general: once you do something useful once, you can often package it so Codex can do it again without reteaching the workflow.

## Remote control

Remote control makes these longer loops feel portable.

Codex can keep working from the machine where your files, permissions, and local setup already live, while you check in from mobile, review what it found, answer a question, approve the next step, or change direction without being back at your desk. [OpenAI describes it as a way to work with Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere/).

This matters most when Codex is already doing something long-running and you want to preserve momentum. You can start a task, walk away, then steer it from your phone when it reaches a decision point.

That matters for the same reason pinned threads, voice, and Heartbeats matter. The work no longer has to pause just because I changed locations. A thread can keep going, and I can keep just enough attention on it to unblock the next move.

## Heartbeats

Pinned threads are useful, but they still wait for you to say something. Heartbeats are what make them recur.

!!! note "Heartbeats"

    Heartbeats
    : Recurring checks a thread can schedule for itself, like watching Slack or a pull request for new activity.

A Heartbeat is a thread-local automation. You can say, "keep an eye on this every few hours," and the thread can schedule itself. A thread can have multiple schedules, run until some condition is met, and adjust its cadence over time.

### Chief of Staff

My Chief of Staff thread runs every 30 minutes:

```text
Every 30 minutes, check Slack and Gmail for unanswered messages that need my attention.
Help me prioritize what matters most.
If someone asks me a question, research the answer as deeply as you can and draft a reply for me, but do not send it.
```

When I come back to Slack, replies are often already sitting in drafts. I still decide what gets sent, but the expensive part of gathering context is done.

### Monitor for feedback

The same pattern works for review loops. A Heartbeat can monitor Google Docs comments, pull request comments, or Slack replies and keep work moving as feedback arrives.

One of my favorite examples came from an animation project. I had posted a video in Slack and asked Codex to check the thread every 15 minutes for feedback, re-render a new version when comments came in, and reply back into the thread tagging the reviewer. The Slack MCP server could not upload files, so the agent used `@computer` to press the Add file button and post the revised render anyway.

The interesting part is not just that it checked Slack every 15 minutes. The loop crossed tool boundaries: Slack for feedback, Remotion for the render, `@computer` for the upload. That is when Heartbeats, connectors, and computer use stop feeling like separate features. Together they become a feedback loop that keeps running without me sitting there.

### Get a refund

Recently I had a package stolen. Amazon told me it would take about 25 minutes to talk to a person, so I created a thread with `@computer` and told it:

```text
Every 5 minutes, check whether the customer support agent has joined this thread.
If they have, do your best to get me a refund.
Once they reply, switch to checking every minute so you can respond faster.
```

By the time I got out of the shower, the refund was done.

Many of my Heartbeats also update my Obsidian vault as a kind of explicit memory.

## Goals

The newest thing I am still learning how to use well is Goals.

!!! note "Goals"

    Goals
    : Longer-running tasks with a real finish line Codex can keep pushing toward.

You should be ambitious with them. A weak goal is "implement the plan in this Markdown file." A strong goal has a real success criterion that the agent can keep pushing against.

Last week I tried to migrate the Python [Rich](https://github.com/Textualize/rich) library into Rust. Because the original project already had a large unit test suite, I could set a goal like: migrate Rich into Rust, but it must pass all the unit tests from the original library.

That test suite gave the run a real oracle: the Rust port was not done until it passed the same tests as the Python library.

This is different from having a long conversation with an AI, accumulating a Markdown plan, and then eventually saying, "implement this." Execution is only as good as the goal and the verification you give it. Ambition without verification is just a wish.

## The side panel

The part of Codex I am most excited about is the side panel.

It is easy to think of this as a place where previews happen. That undersells it. The side panel is where Codex stops being only a chat app and starts becoming the place the work happens.

For me it does three jobs: inspect artifacts, operate web surfaces, and review changes. In all three, I can look at and comment on the same object the agent is acting on.

### Inspect artifacts

Markdown, spreadsheets, CSVs, PDFs, and slides can all live there.

Markdown is commentable. Spreadsheets render formulas and support cell edits, which I use to manage Codex open-source plans. CSVs become tables instead of raw text. PDFs render directly, which is especially useful with LaTeX. Slides can be created and reviewed without leaving the app.

The important thing is not merely that Codex can generate artifacts. It is that I can inspect and annotate them without breaking the loop.

### Operate web surfaces

The in-app browser is even more interesting. The agent can see it, control it with JavaScript through `$browser`, and I can leave annotations directly on what I am looking at.

There are a few web surfaces I now use this way all the time:

- `index.html` for lightweight static artifacts
- Storybook for reviewing UI components
- Remotion Studio for programmatic animation
- [Slidev](https://sli.dev/guide/) for presentations
- Streamlit for data apps

The smallest version is often the best. You can ask the model to make a single `index.html` file with JavaScript and CSS, open it in the side panel, and start interacting with it immediately. No server required. I have been experimenting with using Heartbeats to update a static `index.html` over time so that whenever I return to a thread, there is already a fresh artifact waiting for me.

[Thariq has a very good post](https://x.com/trq212/status/2052809885763747935) about preferring HTML over Markdown as an output format. I think that instinct is right. Once the output is a small application instead of just a document, the relationship changes.

If I need something heavier, I can use a Vite app, but then I need to keep a server running. A plain `index.html` is much more durable.

For animation work, I often have Storybook and Remotion Studio open side by side. I can leave comments like "make this bounce" or "this should be larger," and the agent can inspect the same browser state I am looking at, including the current frame in the animation.

For presentations, I often use Slidev. Codex can inspect the slides, catch content that is cut off, switch between slides, and respond to annotations while I review.

I also expect this to become more useful for tools like Streamlit and Jupyter over time. Different people already live inside different applications. Codex can increasingly meet them there.

The more Codex gets places to remember, revisit, inspect, and act, the less my work dies between prompts. That is the change I care about. Not that an agent can write code for me, but that more of my work can keep moving after I leave.
