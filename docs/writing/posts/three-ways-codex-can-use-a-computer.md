---
title: Three Ways Codex Can Use a Computer
description: When to use Computer Use, Chrome, or the in-app browser in Codex.
date: 2026-06-16
authors:
  - jxnl
categories:
  - Applied AI
  - Personal
comments: true
draft: false
slug: three-ways-codex-can-use-a-computer
tags:
  - Codex
  - Computer Use
  - Workflows
  - Personal Software
---

# Three Ways Codex Can Use a Computer

Recently I had a package stolen. Amazon told me it would take about 25 minutes to connect me to a person, so I gave the thread Computer Use and told it to check every five minutes. Once someone joined, check every minute and do its best to get me a refund.

I went to take a shower. When I came back, the refund was done.

That was when Computer Use clicked for me. Codex is not just a coding agent. Most of my work is messages, forms, browser tabs, and apps that do not connect neatly to anything else.

<!-- more -->

Codex now has three ways to work there:

| Use | Best for | Start with |
| --- | --- | --- |
| Computer Use | Native apps and work across apps | `@Computer`, `@AppName`, an Appshot, or Remote Control |
| Chrome | Signed-in sites and multiple tabs | `@Chrome` |
| In-app browser | Pages, artifacts, and visual review | `@Browser` |

My rule is to use the narrowest tool that can finish the job. If a plugin works, use it. If the task needs a screen, choose among these three.

## 1. Computer Use: almost any app

[Computer Use](https://developers.openai.com/codex/app/computer-use) is the most powerful option and usually the slowest. It can operate Spotify, finance apps, System Settings, or iPhone Mirroring. But it has to look at the screen, click, wait, and look again.

On a Mac, it can work in the background while you keep using your computer. On Windows, it takes over the active desktop.

Install it from **Settings > Computer Use**. On macOS, grant Screen Recording and Accessibility permissions. Then mention `@Computer`, mention an app directly with `@AppName`, or just ask Codex to use Computer Use.

The stolen-package example also shows the difference between a Goal and a thread automation. The Goal was to get the refund. The automation woke the thread every five minutes, then every minute when the agent appeared. One supplied the finish line; the other let Codex wait without forgetting the job.

### People are already using it for stranger things

I asked people for [the most ambitious things they had done with Computer Use](https://x.com/jxnlco/status/2066547199983473013). Someone [applied for a Schengen visa](https://x.com/thevedlabs/status/2066577349273874617). Someone else [paid monthly Airbnb taxes through a county website](https://x.com/GabGarrett/status/2066584487161467090). One person [repaired a virus-filled PC through a reboot loop](https://x.com/craigsdennis/status/2066550916158009401). Another used iPhone Mirroring for [iOS Screen Time](https://x.com/ChristianInProd/status/2066682841249796481). I immediately wondered whether the same setup could [operate a dating app](https://x.com/jxnlco/status/2066618356958896428).

I have also used Computer Use as the last mile when another tool stopped short. One thread read feedback from Slack, changed a video, and rendered a new version. The Slack integration could not upload files, so Computer Use clicked **Add file** and posted it.

### Appshots let me point

An [Appshot](https://developers.openai.com/codex/appshots) sends the frontmost Mac window to a Codex thread. Press both Command keys, then say what you want.

I use this for emails, Slack messages, errors, designs, settings panels, and forms. Sometimes the Appshot is enough. If Codex needs to act, I tell the same thread to continue with Computer Use.

Appshots are how I point. Computer Use is how Codex acts.

### Remote Control lets me leave

[Remote Control](https://developers.openai.com/codex/remote-connections) lets me start or steer the same work from my phone. In the Codex app, click **Set up Codex mobile**, scan the QR code, and connect ChatGPT mobile. The host stays awake and online; the work still runs there with its projects, plugins, Chrome setup, and Computer Use permissions.

[Thomas Ricouard](https://x.com/Dimillian) has been pushing this part of Codex forward. He started with [Codex Monitor](https://x.com/Dimillian/status/2010330190510273016), where every active and past session was visible so you could jump back into the work. Codex Mobile now has [notifications when work finishes and better reconnection](https://x.com/Dimillian/status/2057452433777807486), followed by [`/side` conversations](https://x.com/Dimillian/status/2060215793971786098). Remote Control is becoming less like a status screen and more like Codex in your pocket.

I let Computer Use research and draft. I stay present for payments, credentials, account changes, and security settings. Follow [Ari Weinstein](https://x.com/AriX) for Computer Use and Appshots, and [Thomas](https://x.com/Dimillian) for Codex Mobile and Remote Control.

## 2. Chrome: your signed-in browser

Use the [Chrome extension](https://developers.openai.com/codex/app/chrome-extension) when Codex needs your Chrome profile, cookies, extensions, or an authenticated site. It can control several tabs in a thread and keep working in its tab group while you use Chrome elsewhere.

Open **Plugins**, add **Chrome**, and install the [Codex Chrome extension](https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg). Once it says **Connected**, mention `@Chrome`.

### Make the music more interesting

In one thread, I gave Codex an open Strudel Composer tab and told it to make the music more interesting. It rewrote the harmony and arrangement, changed the tempo, saved the track, and left it playing.

### A thread that watches Twitter

I also keep a Twitter thread that uses Chrome to check DMs, read news, and collect product feedback. It writes anything durable to my vault but does not post or send messages.

That is my default boundary for Chrome: research and draft freely; ask before sending, publishing, purchasing, or submitting.

## 3. The in-app browser: review and annotate

The [in-app browser](https://developers.openai.com/codex/app/browser) lives inside a Codex thread. I use it for public pages and visual artifacts I want to review with Codex. It does not carry your Chrome profile or login state.

Open **Plugins**, add **Browser**, and mention `@Browser`.

### The page becomes the specification

The annotation tools are my favorite part. I often ask Codex to create a single `index.html`, open it in the browser, and wait for comments. Then I can click an element and say “this hierarchy is backwards,” “make this less card-heavy,” or “these controls need more room.” The comment includes the screenshot and element context, so I do not have to describe the whole page again.

### Hand the work to another tool

The browser can also establish context and hand the job to another tool. I once opened an X post and asked Codex to investigate it. The page showed which post I meant; the Twitter CLI then retrieved 38 replies, including nested replies that were not visible on the page.

The Atlas browser team is working to make the in-app browser more powerful: not just a preview, but a place where you and Codex can work on the same thing together. They are cooking. Follow [James Sun](https://x.com/JamesZmSun) to see what they are working on.

## Put the routing rule in AGENTS.md

I do not want to remember this routing every time, so I put it in `AGENTS.md`:

```md
## Browser and desktop routing

- Prefer a plugin when one can finish the task.
- Use an Appshot when showing the frontmost Mac window is easier than describing it.
- Use `@Browser` for public pages, visual review, and annotations.
- Use `@Chrome` for signed-in sites, existing tabs, extensions, or multiple tabs.
- Use `@Computer` for native apps or work across apps.
- Use Remote Control to start or steer work from my phone.
- Ask before sending, publishing, purchasing, submitting, or changing account settings.
```

## Follow the work

Follow [me (@jxnlco)](https://x.com/jxnlco) for the ways I am using these tools, [Ari Weinstein](https://x.com/AriX) for Computer Use, [Thomas Ricouard](https://x.com/Dimillian) for Codex Mobile, [James Sun](https://x.com/JamesZmSun) for browser work, [Andrew Ambrosino](https://x.com/ajambrosino) for Codex app updates, and [OpenAI Developers](https://x.com/OpenAIDevs) for broader news.

The interesting part is not that Codex can click buttons. A thread can start with an Appshot, move across apps and browsers, wait for someone else, and keep working after I leave.

## What should I write about next?

If you want me to go deeper on Goals, thread automations, Appshots, Remote Control, or how I route work between these tools, leave a comment. Tell me what you are trying to do; I will use the best questions for the next post.
