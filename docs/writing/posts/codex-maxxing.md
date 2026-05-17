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

I had already been using coding agents a lot before Codex. Mostly, though, I used them through interfaces built for coding work: making diffs, changing repos, and shipping code.

Around November, I started pushing them into knowledge work too. I made presentations in [Slidev](https://sli.dev/), used agents more like note-takers with voice inputs, and kept looking for other artifacts a coding agent could help me produce: an `index.html`, then `Ctrl-P` into a PDF.

The latest Codex app upgrades are the first thing I've used that makes that broader mode feel native for everyone. It's still excellent for coding, but the more interesting shift for me is that it gives all of my work somewhere to live.

What changed my behavior was learning to give work five things: a durable thread, a place to remember things, tools to act on my whole computer, a schedule that brings it back, and a surface where I can review any kind of work: websites, Markdown, PDFs, spreadsheets, and slides.

<!-- more -->

## Durable threads

The first of those was compaction.

I now keep a pinned thread for every important workstream I care about:

- my Chief of Staff thread
- [the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- [the OpenAI CLI](https://github.com/openai/openai-cli)
- [Codex for open source](https://openai.com/form/codex-for-oss)
- one just to monitor Twitter

These aren't short chats. They're megathreads that I've been compacting for months. They accumulate history, preferences, and old decisions that I don't want to recreate every time I come back.

!!! tip "Pinned thread shortcuts"

    You can jump directly to pinned threads with `Command-1` through `Command-9`.

There's a tradeoff here. Long-running threads aren't free. If you revisit them later, the conversation is probably no longer in cache, so you can incur more cost than you would in a fresh short thread. For workstreams I care about, I'll pay that to avoid starting over.

## Side chats

In a months-old megathread, every off-topic question is context I carry forever.

`/side` solves that. It opens a side chat with the same project context, history, and files, but as an ephemeral layer. I ask, get the answer, close it. The main thread never sees it. It's Codex's `/btw`. The tangent never touches the thread I care about.

## Voice input

I use voice because the agent gets the unedited version of my thinking, not because it's faster. Codex has built-in voice input, but I also use Wispr Flow because system-wide dictation changes how much context I can feed into everything else too. If I'm planning a piece of work, I might say, "I think there's some guy named Ben in Slack who mentioned this, I don't remember exactly what, just go look." That sentence is too vague and annoying to type, but completely natural to say.

The same thing applies to transcripts. If I want to write a post, I can call someone, record the conversation, or talk to them in person with Granola on my phone, then use the transcript as the starting material. A lot of plans get better when the model has access to the messy version of what I think, not just the polished one.

## Steering

Steering lets you inject the next message after a tool call. If I'm reviewing a website, I can keep talking while I look at it:

- make this smaller
- this copy is wrong
- the spacing between these two things feels off
- once this is done, open a PR
- wait for the preview deploy
- send the preview link to the person who needs to review it on Slack

I don't need to wait for each step to finish before deciding the next one. I can keep adding intent while the agent is still working, then walk away with the queue already shaped.

Later, Heartbeats can monitor the PR or the Slack thread after I leave. So one task runs across many prompts instead of one.

## Remote control

Remote Control splits the work from where I watch it.

Codex keeps working on the machine where your files, permissions, and setup already live. You check in from your phone: review what it found, answer a question, approve the next step, change direction. [OpenAI calls this working with Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere/).

It matters most when something long-running is already going and I don't want to wait until I'm back at my laptop. Start a task, walk away, steer it from my phone when it hits a decision point.

That matters for the same reason pinned threads, voice, and Heartbeats matter. The work no longer has to pause just because I changed locations. A thread can keep going, and I can keep just enough attention on it to unblock the next move.

## Memory

Once threads started lasting longer, they needed shared memory outside any one repo.

Most of my long-running threads start in an Obsidian vault:

```text
vault/
├── TODO.md
├── people/
├── projects/
├── agent/
└── notes/
```

At the top level, I keep `AGENTS.md` instructions that say things like: as you learn more about people or make progress on projects, update the relevant pages in the vault.

The vault is where the agent lives, separate from any project. Repos hold code. The vault holds rolling context: people, decisions, open loops, daily notes, project state, and the bits of understanding that would otherwise get lost between threads.

I also keep the vault as a GitHub repo. That buys me two things:

1. it can work in the cloud
2. diffs become a review surface for memory

When the agent updates the vault, I can read the diff and see what it thought was important enough to remember. Reviewing those diffs is effectively how I acknowledge that I've seen what the agent learned.

By then each pinned thread behaves like a separate coworker reading from the same notebook.

## Computer and Browser Use

Memory is useless if the thread can't act on anything.

I split it three ways:

- `$browser` is for local web surfaces I want to inspect and annotate
- `@chrome` is for signed-in browser state and multiple tabs
- `@computer` is for work that only exists as a GUI

If I'm iterating on a local app, I want `$browser`. If I need to work inside a logged-in browser session, I want `@chrome`. If the only way to do the task is to click through a desktop app, I want `@computer`.

On my work machine, Twitter is logged into Safari. If I have `@computer` read Twitter there, I lose Safari while it works. `@chrome` is better when I want the agent to use several authenticated tabs in parallel without taking over the whole app I'm using.

Connectors extend that reach into the rest of my actual work. The ones I use most are `$slack`, `$gmail`, and `$calendar`, because Slack threads, inboxes, and calendars are where a lot of work shows up before it ever becomes code.

Skills make repeated workflows reusable. Skill Creator and Skill Installer are a good place to start. Skill Installer lets you add OpenAI-recommended skills directly from the composer. After [Codex pets](https://developers.openai.com/codex/app/settings#codex-pets) launched, I used it to install the Hatch Pet skill, but the useful pattern is general: once you do something useful once, you can often package it so Codex can do it again without reteaching the workflow.

## Heartbeats

Pinned threads are useful, but they still wait for you to say something. Heartbeats are what make them recur.

A Heartbeat is a thread-local automation. You can say, "keep an eye on this every few hours," and the thread can schedule itself. A thread can have multiple schedules, run until some condition is met, and adjust its cadence over time.

### Chief of Staff

My Chief of Staff thread from earlier runs every 30 minutes:

```text
Every 30 minutes, check Slack and Gmail for unanswered messages that need my attention.
Help me prioritize what matters most.
If someone asks me a question, research the answer as deeply as you can and draft a reply for me, but do not send it.
```

When I come back to Slack, replies are often already sitting in drafts. I still decide what gets sent, but the expensive part of gathering context is done.

### Monitor for feedback

The same pattern works for review loops. A Heartbeat can monitor Google Docs comments, pull request comments, or Slack replies and keep work moving as feedback arrives.

One of my favorite examples came from an animation project. I had posted a video in Slack and asked Codex to check the thread every 15 minutes for feedback, re-render a new version when comments came in, and reply back into the thread tagging the reviewer. The Slack MCP server couldn't upload files, so the agent used `@computer` to press the Add file button and post the revised render anyway.

The interesting part isn't just that it checked Slack every 15 minutes. The loop crossed tool boundaries: Slack for feedback, Remotion for the render, `@computer` for the upload. That's when Heartbeats, connectors, and computer use stop feeling like separate features. Together they become a feedback loop that keeps running without me sitting there.

### Get a refund

Recently I had a package stolen. Amazon told me it would take about 25 minutes to talk to a person, so I created a thread with `@computer` and told it:

```text
Every 5 minutes, check whether the customer support agent has joined this thread.
If they have, do your best to get me a refund.
Once they reply, switch to checking every minute so you can respond faster.
```

By the time I got out of the shower, the refund was done.

Many of my Heartbeats also update my Obsidian vault as a kind of explicit memory. Separately, Codex now has memory features in `Settings > Personalization > Memories`, including [Memories](https://developers.openai.com/codex/memories) and [Chronicle](https://developers.openai.com/codex/memories/chronicle).

## Goals

The newest thing I'm still learning how to use well is Goals.

You should be ambitious with them. A weak goal is "implement the plan in this Markdown file." A strong goal has a real success criterion that the agent can keep pushing against.

Last week I tried to migrate the Python [Rich](https://github.com/Textualize/rich) library into Rust. Because the original project already had a large unit test suite, I could set a goal like: migrate Rich into Rust, but it must pass all the unit tests from the original library.

That test suite gave the run a real stopping point: the Rust port wasn't done until it passed the same tests as the Python library.

This is different from having a long conversation with an AI, accumulating a Markdown plan, and then eventually saying, "implement this." The execution is only as good as the goal and the test you give it.

## The side panel

The part of Codex I'm most excited about is the side panel.

It looks like a preview pane. It's actually where the work happens, not just where I talk about it.

It does three things: inspect artifacts, operate web surfaces, review changes. In all three I can look at and comment on the same object the agent is acting on.

### Inspect artifacts

Markdown, spreadsheets, CSVs, PDFs, and slides can all live there.

Markdown is commentable. Spreadsheets render formulas and support cell edits, which I use to manage Codex open-source plans. CSVs become tables instead of raw text. PDFs render directly, which is especially useful with LaTeX. Slides can be created and reviewed without leaving the app.

What matters is that I can inspect and annotate them without breaking the loop.

### Operate web surfaces

The agent can see the in-app browser, control it with JavaScript through `$browser`, and I can annotate directly on what I'm looking at.

There are a few web surfaces I now use this way all the time:

- `index.html` for lightweight static artifacts
- Storybook for reviewing UI components
- Remotion Studio for programmatic animation
- [Slidev](https://sli.dev/guide/) for presentations
- Streamlit for data apps

The smallest version is often the best. You can ask the model to make a single `index.html` file with JavaScript and CSS, open it in the side panel, and start interacting with it immediately. No server required. I've been experimenting with using Heartbeats to keep updating a static `index.html` over time so that whenever I return to a thread, there's already a fresh artifact waiting for me.

[Thariq has a very good post](https://x.com/trq212/status/2052809885763747935) about preferring HTML over Markdown as an output format. I think that instinct is right. Once the output is a small application instead of just a document, the relationship changes.

If I need something heavier, I can use a Vite app, but then I need to keep a server running. A plain `index.html` is much more durable.

For animation work, I often have Storybook and Remotion Studio open side by side. I can leave comments like "make this bounce" or "this should be larger," and the agent can inspect the same browser state I'm looking at, including the current frame in the animation.

For presentations, I often use Slidev. Codex can inspect the slides, catch content that is cut off, switch between slides, and respond to annotations while I review.

I also expect this to become more useful for tools like Streamlit and Jupyter over time. Different people already live inside different applications. Codex can increasingly meet them there.

### Review changes

The side panel also has a diff viewer. It can render the actual pull request diff and the GitHub comments attached to it. That matters because review is one of the few places where I still want the model and me to be looking at exactly the same object.

The more Codex gets places to remember, revisit, inspect, and act, the less my work dies between prompts. I don't care that an agent can write code for me. I care that my work keeps moving after I leave.
