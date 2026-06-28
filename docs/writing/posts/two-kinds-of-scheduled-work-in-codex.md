---
title: Two kinds of scheduled work in Codex
description: A simple rule for choosing between Scheduled Tasks and Scheduled Messages in Codex.
date: 2026-06-28
authors:
  - jxnl
categories:
  - Applied AI
  - Personal
comments: true
draft: false
slug: two-kinds-of-scheduled-work-in-codex
tags:
  - Codex
  - Workflows
  - Personal Software
---

# Two kinds of scheduled work in Codex

Most automation language is more complicated than the job.

You want Codex to do something later, or keep checking something until it changes. That sounds like one feature. It is actually two different kinds of work, and the difference is simple:

- **Scheduled Tasks** create a new thread every time they run.
- **Scheduled Messages** use the same existing thread every time they run.

That is the whole model.

<!-- more -->

## Use a Scheduled Task when every run can start fresh

A Scheduled Task is best when the job makes sense without the conversation that created it.

For example:

```text
Every morning at 9 AM, summarize what I need to catch up on from my email, calendar, and team messages.
```

Tomorrow's summary does not need to remember today's summary. It needs the same instructions, current information, and a fresh place to report the result.

This is also useful when one task should run across several projects, or when you want each run to appear separately in Triage. Each run is its own thread. The schedule is the thing that connects them.

## Use a Scheduled Message when the next check needs the thread

A Scheduled Message, sometimes called a thread automation, returns to the same existing thread each time it runs.

For example:

```text
Check this PR every 30 minutes. If there are comments, address them and keep CI green. Stop when the PR merges.
```

The next check depends on the work that already happened. The thread knows which PR you mean, which comments were addressed, what failed in CI, and what has changed since the last check.

This is the right shape for:

- polling for updates
- checking for a status change
- ongoing research or triage
- work with a clear stopping condition

The thread is the thing that connects the runs.

## The decision rule is context

Ask one question:

> If this ran tomorrow, would it need the earlier conversation?

If no, use a Scheduled Task. Give it a durable prompt and let each run start clean.

If yes, use a Scheduled Message. Keep the work in one thread so each check can build on the decisions and results that came before it.

The schedule matters, but it is not the main decision. The main decision is where the useful context should live.

## Make your own loop skill

I do not want to remember the setup questions every time, so I would make a small skill that turns a rough request into the right scheduled workflow.

Give Codex this prompt:

```text
Create a reusable loop skill for scheduled work.

When I give it a request, first decide whether each run can start fresh or whether the next check needs the current thread's context.

If each run can start fresh, help me create a Scheduled Task.
If the next check needs the current thread, help me create a Scheduled Message.

Infer what you can from the conversation. Ask only the missing questions that materially change the workflow:
- What should Codex do each time?
- How often should it run?
- What change is important enough to report?
- When should it stop?
- When should it ask me for input?

Then create the scheduled workflow with a short, durable prompt that will still make sense on a later run.
```

The best automations do not start with a complicated system. They start with knowing whether the next run needs a clean slate or the same thread.
